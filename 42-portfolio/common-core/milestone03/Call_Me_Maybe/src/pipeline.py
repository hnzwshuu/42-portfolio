"""Select functions and generate their arguments with a local LLM."""

import json
import sys
from typing import Any

from src.decoding import Vocabulary, encode, generate_json_value
from src.schema import FunctionDefinition, Prompt, validate_parameters
from src.selection import select_json_string

MODEL_NAME = 'Qwen/Qwen3-0.6B'
MAX_GENERATION_TOKENS = 256


def chat_prompt(instructions: str, request: str) -> str:
    """Format a Qwen3 chat prompt with a completed empty thinking block.

    Args:
        instructions: System instructions for the model.
        request: Original user request.

    Returns:
        Chat text ending at the start of the assistant's final response.
    """
    return (
        '<|im_start|>system\n' + instructions + '<|im_end|>\n'
        '<|im_start|>user\n' + request + '<|im_end|>\n'
        '<|im_start|>assistant\n<think>\n\n</think>\n\n'
    )


def build_function_call_format(
    function_name: str,
    parameter_names: list[str],
) -> str:
    """Format a function name and parameter names as a call signature.

    Args:
        function_name: Function name to display.
        parameter_names: Parameter names in definition order.

    Returns:
        A signature such as name(a, b), or name() without parameters.
    """
    return f'{function_name}({", ".join(parameter_names)})'


def _selection_instructions(
    functions: list[FunctionDefinition],
) -> str:
    """Build selection instructions containing the function catalogue.

    Args:
        functions: Available validated function definitions.

    Returns:
        Instructions asking the model for one exact function name.
    """
    catalogue: list[dict[str, Any]] = []
    for definition in functions:
        catalogue.append({
            'name': definition.name,
            'description': definition.description,
            'parameters': definition.parameters,
        })
    return (
        'Select the single function that best fulfills the user request. '
        'Choose by the operation requested, not by the answer to it. '
        'Return only the exact function name as a JSON string.\n'
        'Available functions:\n' + json.dumps(catalogue, ensure_ascii=False)
    )


def choose_function(
    model: Any, functions: list[FunctionDefinition], prompt: str,
    max_tokens: int,
) -> FunctionDefinition:
    """Choose an available function using model scores.

    Args:
        model: SDK model providing tokenization and logits.
        functions: Nonempty catalogue with unique function names.
        prompt: Original user request.
        max_tokens: Maximum token count per function-name candidate.

    Returns:
        The definition whose name receives the highest candidate score.

    Raises:
        ValueError: If candidate encoding or model scoring fails.
    """
    functions_by_name: dict[str, FunctionDefinition] = {}
    for definition in functions:
        functions_by_name[definition.name] = definition

    instructions = _selection_instructions(functions)
    context = encode(model, chat_prompt(instructions, prompt))
    choices = list(functions_by_name)
    selected = select_json_string(
        model, context, choices, max_tokens,
    )
    return functions_by_name[str(selected)]


def _argument_instructions(definition: FunctionDefinition) -> str:
    """Build argument extraction instructions in definition order.

    Args:
        definition: Selected function and its required parameters.

    Returns:
        Instructions for extracting input values without executing a call.
    """
    argument_lines: list[str] = []
    for name, schema in definition.parameters.items():
        schema_text = json.dumps(schema, ensure_ascii=False)
        argument_lines.append(f'- {name}: {schema_text}')
    arguments = '\n'.join(argument_lines)
    call_format = build_function_call_format(
        definition.name,
        list(definition.parameters),
    )
    return (
        'Extract the input argument values for the function below from '
        'the user request. Return only a JSON object mapping argument names '
        'to their values. Do not execute the function or return its result. '
        'Values must come from the request, not from function metadata. '
        'Preserve the original text, spelling, case and punctuation of '
        'string inputs. Use JSON escapes inside strings. '
        'Use numbers for number parameters and true/false for booleans. '
        'Infer a necessary argument from the operation when it is described '
        'in words. All arguments are required.\n'
        f'Function to call: {definition.name}\n'
        f'Function call format: {call_format}\n'
        f'Purpose: {definition.description}\n'
        f'Argument definitions (in output order):\n{arguments}'
    )


def generate_parameters(
    model: Any, vocabulary: Vocabulary, definition: FunctionDefinition,
    prompt: str, max_tokens: int,
) -> dict[str, Any]:
    """Generate and validate scalar arguments in one continuing context.

    Args:
        model: SDK model providing tokenization and logits.
        vocabulary: Token vocabulary and reusable decoding caches.
        definition: Selected function with validated parameter schemas.
        prompt: Original user request from which to extract arguments.
        max_tokens: Generation token budget per parameter value.

    Returns:
        A validated parameter dictionary, empty for a parameterless call.

    Raises:
        ValueError: If decoding fails, a token budget is exceeded, or
            generated arguments do not match the definition.
    """
    instructions = _argument_instructions(definition)
    context = encode(model, chat_prompt(instructions, prompt))
    parameters: dict[str, Any] = {}
    parameter_items = list(definition.parameters.items())
    if not parameter_items:
        return parameters

    first_name, first_schema = parameter_items[0]
    first_key = json.dumps(first_name, ensure_ascii=True)
    first_start = '{' + first_key + ':'
    initial_bytes = b''
    if first_schema['type'] == 'string':
        first_start += '"'
        initial_bytes = b'"'
    context.extend(encode(model, first_start))

    for index, (name, schema) in enumerate(parameter_items):
        if index == len(parameter_items) - 1:
            terminator = b'}'
            next_initial_bytes = b''
        else:
            next_name, next_schema = parameter_items[index + 1]
            next_key = json.dumps(next_name, ensure_ascii=True)
            terminator_text = ',' + next_key + ':'
            next_initial_bytes = b''
            if next_schema['type'] == 'string':
                terminator_text += '"'
                next_initial_bytes = b'"'
            terminator = terminator_text.encode('ascii')
        value, context = generate_json_value(
            model, context, schema, vocabulary, terminator,
            initial_bytes=initial_bytes,
            max_tokens=max_tokens,
        )
        parameters[name] = value
        initial_bytes = next_initial_bytes
    return validate_parameters(definition, parameters)


def run(
    functions: list[FunctionDefinition], prompts: list[Prompt],
) -> list[dict[str, Any]]:
    """Process requests in order, loading the model once for the batch.

    Progress is written to stderr. Results are returned only after all
    requests succeed; file output is handled by the caller.

    Args:
        functions: Nonempty validated catalogue with unique names.
        prompts: Validated requests whose original text is preserved.

    Returns:
        Function call objects with prompt, name, and parameters keys.
        An empty request list returns an empty list without model loading.

    Raises:
        ValueError: If a request fails, with its one-based index included
            in the message, or the SDK vocabulary is invalid.
    """
    if not prompts:
        return []
    from llm_sdk import Small_LLM_Model

    print(f'Loading {MODEL_NAME}...', file=sys.stderr)
    model = Small_LLM_Model(MODEL_NAME)
    vocabulary = Vocabulary.from_model(model)
    results: list[dict[str, Any]] = []
    for index, item in enumerate(prompts, 1):
        prompt_text = item.prompt
        print(f'[{index}/{len(prompts)}] {prompt_text}', file=sys.stderr)

        try:
            definition = choose_function(
                model, functions, prompt_text, MAX_GENERATION_TOKENS,
            )
            parameters = generate_parameters(
                model, vocabulary, definition, prompt_text,
                MAX_GENERATION_TOKENS,
            )
        except Exception as error:
            raise ValueError(f'Prompt {index}: {error}') from error
        result = {
            'prompt': prompt_text,
            'name': definition.name,
            'parameters': parameters,
        }
        results.append(result)
    return results
