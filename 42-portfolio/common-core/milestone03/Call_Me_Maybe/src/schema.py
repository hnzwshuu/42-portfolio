"""Validate input JSON files and generated function arguments."""

import json
import math
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator

SCALAR_TYPES = {'string', 'number', 'integer', 'boolean'}


def matches_type(value: Any, kind: str) -> bool:
    """Check a value against a supported JSON scalar type.

    Args:
        value: Value to check without type coercion.
        kind: Expected JSON type name.

    Returns:
        Whether the value matches. Booleans are not numbers, and numeric
        floats must be finite. Unsupported type names return False.
    """
    if kind == 'string':
        return isinstance(value, str)
    if kind == 'boolean':
        return type(value) is bool
    if kind == 'integer':
        return type(value) is int
    if kind == 'number':
        if type(value) is int:
            return True
        if type(value) is float:
            return math.isfinite(value)
    return False


def check_parameter_schema(name: str, schema: dict[str, Any]) -> None:
    """Validate a parameter schema containing only a scalar type.

    Args:
        name: Parameter name used in error messages.
        schema: Parameter definition to validate.

    Raises:
        ValueError: If the type is missing or unsupported, or extra schema
            fields are present.
    """
    parameter_type = schema.get('type')
    if (
        not isinstance(parameter_type, str)
        or parameter_type not in SCALAR_TYPES
    ):
        raise ValueError(
            f'Parameter {name!r} has unsupported type {parameter_type!r}. '
            'Supported: string, number, integer, boolean.'
        )

    allowed_fields = {'type'}
    unknown_fields = []
    for field in schema:
        if field not in allowed_fields:
            unknown_fields.append(field)
    if unknown_fields:
        raise ValueError(
            f'Parameter {name!r}: unsupported schema fields '
            f'{sorted(unknown_fields)}.'
        )


class FunctionDefinition(BaseModel):
    """A validated function definition with required scalar parameters.

    Attributes:
        model_config: Validation settings that reject extra fields.
        name: Nonempty function name.
        description: Description used by the model to select the function.
        parameters: Required argument names mapped to their schemas.
        returns: Return type metadata; the function is not executed.
    """

    model_config = ConfigDict(extra='forbid')
    name: str
    description: str
    parameters: dict[str, dict[str, Any]]
    returns: dict[str, Any]

    @model_validator(mode='after')
    def validate_definition(self) -> 'FunctionDefinition':
        """Validate the definition after Pydantic checks its field types.

        Returns:
            This validated definition.

        Raises:
            ValueError: If the name is blank or a schema is unsupported.
        """
        if not self.name.strip():
            raise ValueError('Function names must not be empty.')
        for name, schema in self.parameters.items():
            check_parameter_schema(name, schema)

        return_type = self.returns.get('type')
        allowed_return_types = SCALAR_TYPES | {'object', 'array'}
        if not isinstance(return_type, str):
            raise ValueError('returns must contain a supported JSON type.')
        if return_type not in allowed_return_types:
            raise ValueError('returns must contain a supported JSON type.')
        return self


class Prompt(BaseModel):
    """A user request whose original text is preserved in the output.

    Attributes:
        model_config: Validation settings that reject extra fields.
        prompt: Original request text, which may be empty.
    """

    model_config = ConfigDict(extra='forbid')
    prompt: str


def reject_constant(value: str) -> Any:
    """Reject a nonstandard numeric constant during JSON parsing.

    Args:
        value: Constant text supplied by the JSON parser.

    Raises:
        ValueError: Always, because NaN and Infinity are not valid JSON.
    """
    raise ValueError(f'{value} is not a valid JSON constant.')


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Build a JSON object while rejecting duplicate keys.

    Args:
        pairs: Key-value pairs in their original order.

    Returns:
        A dictionary containing each key exactly once.

    Raises:
        ValueError: If a key occurs more than once.
    """
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate JSON key: {key!r}.')
        result[key] = value
    return result


def load_array(path: Path) -> list[Any]:
    """Read a UTF-8 JSON file whose top-level value is an array.

    Args:
        path: Input JSON file path.

    Returns:
        Array elements in their original order.

    Raises:
        ValueError: If reading fails, the JSON is invalid, keys repeat,
            nonstandard constants occur, or the top-level value is not
            an array.
    """
    try:
        with path.open(encoding='utf-8') as input_file:
            data = json.load(
                input_file,
                parse_constant=reject_constant,
                object_pairs_hook=unique_object,
            )
    except (OSError, ValueError, UnicodeError) as error:
        raise ValueError(f'Cannot read {path}: {error}') from error
    if not isinstance(data, list):
        raise ValueError(f'{path}: expected a JSON array.')
    return data


def load_functions(path: Path) -> list[FunctionDefinition]:
    """Load a nonempty catalogue of uniquely named functions.

    Args:
        path: Function definitions JSON file path.

    Returns:
        Validated function definitions in file order.

    Raises:
        ValueError: If reading or validation fails, the catalogue is empty,
            or function names repeat.
    """
    functions: list[FunctionDefinition] = []
    for value in load_array(path):
        definition = FunctionDefinition.model_validate(value)
        functions.append(definition)

    if not functions:
        raise ValueError(f'{path}: the function catalogue must not be empty.')

    seen_names: set[str] = set()
    for definition in functions:
        if definition.name in seen_names:
            raise ValueError(f'{path}: function names must be unique.')
        seen_names.add(definition.name)
    return functions


def load_prompts(path: Path) -> list[Prompt]:
    """Load requests in input order without modifying their text.

    Args:
        path: Prompts JSON file path.

    Returns:
        Validated prompts, preserving empty strings and an empty array.

    Raises:
        ValueError: If reading or prompt validation fails.
    """
    prompts: list[Prompt] = []
    for value in load_array(path):
        prompt = Prompt.model_validate(value)
        prompts.append(prompt)
    return prompts


def validate_parameters(
    definition: FunctionDefinition,
    value: Any,
) -> dict[str, Any]:
    """Validate generated argument names and scalar types.

    Args:
        definition: Function definition describing required arguments.
        value: Generated parameter object to validate.

    Returns:
        A shallow copy of the validated parameter dictionary.

    Raises:
        ValueError: If the value is not an object, argument names differ,
            or a value has the wrong type.
    """
    if not isinstance(value, dict):
        raise ValueError('Generated parameters must be a JSON object.')

    actual_names = set(value)
    expected_names = set(definition.parameters)
    if actual_names != expected_names:
        raise ValueError('Generated parameter names do not match the schema.')

    for name, schema in definition.parameters.items():
        argument_value = value[name]
        expected_type = schema['type']
        if not matches_type(argument_value, expected_type):
            raise ValueError(
                f'Parameter {name!r} must have type {expected_type!r}.'
            )
    return dict(value)
