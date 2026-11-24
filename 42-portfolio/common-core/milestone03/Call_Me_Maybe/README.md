*This project has been created as part of the 42 curriculum by shanazaw.*

# Call Me Maybe

## Description

Call Me Maybe translates natural-language requests into function names and
typed arguments using `Qwen/Qwen3-0.6B`. It produces function calls; it does
not execute the functions or calculate their results.

Run the commands below from the directory containing this README,
`pyproject.toml`, and `src/`. In this development checkout, that directory is
`made_by_llm/`. For submission, its contents belong at the Git repository root.

## Instructions

Requirements: Python 3.10–3.13, `uv`, and enough memory for the local model.
Dependency installation and the first model download require network access
unless the required files are already cached.

From this directory:

```sh
uv sync
uv run python -m src
```

The default inputs are `data/input/functions_definition.json` and
`data/input/function_calling_tests.json`. The output is
`data/output/function_calling_results.json`. Missing output directories are
created when results are saved. Generated output is excluded by `.gitignore`.

To specify paths explicitly:

```sh
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/review_results.json
```

Available Makefile targets:

| Target | Action |
| --- | --- |
| `make install` | Install dependencies with `uv sync`. |
| `make run` | Run `uv run python -m src`. |
| `make debug` | Run the application under Python's `pdb` debugger. |
| `make lint` | Run flake8 and mypy with the subject's required flags. |
| `make lint-strict` | Run flake8 and mypy with `--strict`. |
| `make clean` | Remove source bytecode caches and mypy/pytest caches. |

`make run ARGS="--input path/to/prompts.json"` passes custom arguments.

### Input and output

Function definitions use the subject's format:

```json
[
  {
    "name": "fn_add_numbers",
    "description": "Add two numbers together and return their sum.",
    "parameters": {
      "a": {
        "type": "number"
      },
      "b": {
        "type": "number"
      }
    },
    "returns": {
      "type": "number"
    }
  }
]
```

Input prompts are a JSON array of objects containing exactly a string-valued
`prompt` field, for example:

```json
[{"prompt": "Add 2 and 3"}]
```

The function catalogue must be nonempty, with unique, nonblank names.
Each parameter definition accepts only a `type` field. Supported argument
types are `number`, `integer`, `string`, and `boolean`. Every declared
parameter is required. A function with `"parameters": {}` is supported.
Nested arguments and extra schema fields such as `enum`, `minimum`, or
`description` are rejected. Return types are metadata because the program
never executes functions; accepted return types are the four scalar types
above, `object`, and `array`.

For `{"prompt": "Add 2 and 3"}`, the corresponding output element is:

```json
{"prompt": "Add 2 and 3", "name": "fn_add_numbers", "parameters": {"a": 2, "b": 3}}
```

The output file is an array whose entries contain exactly `prompt`, `name`,
and `parameters`. Requests retain their original text and order. Progress
and errors go to stderr; the completion message goes to stdout. An empty
prompt array produces `[]` without loading the model, provided the function
catalogue is valid.

Missing files, malformed JSON, invalid input schemas, and generation errors
are reported with a nonzero exit status. Results are saved only after all
requests succeed. Failures before saving leave any existing output intact,
but saving directly overwrites the file: a write failure or interruption
during saving can leave it incomplete. Output paths resolving to either
input file are rejected.

## Algorithm explanation

### Function selection

The model sees the available names, descriptions, and argument definitions.
Available function names are encoded as JSON strings. `selection.py` scores
every candidate from beginning to end and calculates its mean conditional
log probability. The candidate with the
highest score is selected. Selection depends on the LLM's scores, with no
keyword routing or lookup of known prompts. There is no no-match candidate
or relevance threshold: if selection succeeds, it returns an available
function even when none is appropriate for the request.

### Constrained argument decoding

1. Read the vocabulary through `get_path_to_vocab_file()` and invert the
   byte-level BPE alphabet. Build a trie of token byte sequences once.
2. Process each parameter separately and compile its scalar schema and
   terminator into a byte automaton, reusing cached grammars when possible.
3. Walk viable branches of that trie to determine which complete tokens
   preserve a valid JSON prefix. Cache the result for each automaton state.
4. Obtain logits through `get_logits_from_input_ids()`. Initialize a mask
   to negative infinity and retain logits only for permitted tokens.
5. Select the highest-scoring permitted token, append its ID to the model
   context, and advance the automaton. Stop when the scalar and its
   terminator are complete. Bytes with only one possible continuation are
   appended directly without a model call.
6. Put each parsed value into a Python dictionary under the parameter name,
   then validate the complete dictionary before writing the output file.

The program constructs parameter names and the outer JSON structure instead
of asking the model to generate them. It shows the model the completed JSON
prefix and generates one scalar value. Between values, the fixed terminator
contains the comma, the next parameter name, the colon, and the opening quote
when the next value is a string. The final value uses `}` as its terminator.
Numbers reject leading zeros and incomplete fractions or exponents. Strings
handle ASCII characters and JSON escapes, including `\uXXXX`. Raw UTF-8
bytes for Japanese or accented characters are not accepted by the string
grammar; the model must generate Unicode escapes to represent them. Input
files themselves are read as UTF-8, and the original prompt is preserved.
Tokens may contain several characters; the automaton checks every byte.
Generated non-finite floats cannot be written.

The generation budget is 256 new tokens per argument, including forced
tokens and the terminator. Each function-name candidate is also limited
to 256 tokens. Exhausting a generation budget or having no valid token
with a finite score produces an error rather than a partial result file.

## Design decisions

- `schema.py`: Pydantic input validation and explicit output type checks.
- `selection.py`: straightforward complete-name model scoring.
- `grammar.py`: JSON/schema byte automata.
- `decoding.py`: vocabulary trie, logit masks, and generation limits.
- `pipeline.py`: model loading and ordered prompt processing.
- `__main__.py`: CLI, error reporting, and direct JSON file writing.

All application classes in `src/` inherit from Pydantic `BaseModel`.
Generated argument types are checked without coercion: booleans are not
accepted as numbers, and floats must be finite. The application uses
only public SDK methods. It does not import torch, transformers, or an
external constrained-decoding framework. Those inference dependencies are
installed as dependencies of the supplied SDK. The lint tools check the
application and exclude the SDK and generated caches.

The model and vocabulary load once per batch. Each argument value is generated
after a JSON prefix that reaches the beginning of that value. The returned
model context continues into the next argument, while each parsed value is
stored separately in a Python dictionary. Output is written with `json.dump()`
and `allow_nan=False` after the whole batch succeeds.

## Performance analysis

A local review on 2026-09-18 ran `Qwen/Qwen3-0.6B` on the 11 supplied prompts.
All 11 outputs parsed as JSON, matched their parameter schemas, and selected
the expected functions and arguments. Regex arguments were checked by the
replacement results they produced, allowing equivalent patterns.

This single run does not establish accuracy on unseen catalogues or
repeatability across runs. Runtime was not measured, so the subject's
five-minute target remains unverified. The private Moulinette evaluation
has not been run. JSON/schema validity and semantic accuracy are separate:
constraints can enforce a string type, but the model must still extract the
correct string. A generation failure aborts the batch before saving.

Vocabulary construction is linear in the total token-byte length. A new
grammar state's allowed-token calculation visits viable trie branches;
repeated states reuse the mask. Per-token masking is linear in vocabulary
size. Candidate selection evaluates every token in every function-name
candidate. Argument values are decoded one after another in one continuing
model context. Model inference dominates runtime; the public SDK recomputes
the context and exposes no reusable key/value cache. Time and memory increase
with catalogue size, request length, argument count, and generated length.

## Challenges faced

Function names can have different token lengths and shared prefixes. The
selector compares complete names using mean log probability, at the cost
of additional model calls for every candidate.

Argument extraction must distinguish a function's name from an argument
named `name`. The argument prompt separates the call signature, purpose,
and parameter definitions and asks for input values rather than results.

A token can span several JSON characters, so checking only its first byte
is insufficient. The decoder validates the full token against the state
machine and parses the completed value with `json.loads()`. Raw non-ASCII
string generation remains unsupported; Unicode escapes are the available
representation. Generation limits and finite-score checks turn dead ends
into explicit failures.

## Testing strategy

The repository contains demonstration inputs but no automated test suite.
The local review used temporary checks outside the submitted source files.

To check code quality and run the supplied examples:

```sh
make lint
uv run python -m src
uv run python -m json.tool data/output/function_calling_results.json > /dev/null
```

The final command checks JSON parsing only. Also inspect that every input
has one output in the same order, each entry has exactly the required keys,
and each name and parameter matches its function definition and request.

The local review confirmed clear error messages without tracebacks for
missing files, malformed JSON, invalid UTF-8, wrong prompt types, an empty
function catalogue, an output path pointing to a directory, and identical
input/output paths. An empty prompt array produced `[]` and created the
requested output directory. `enum` rejection, raw non-ASCII grammar rejection, and
partial output after a simulated write failure were also confirmed.

## Resources

- [Hands-On Large Language Models, Japanese edition (直感 LLM)](https://www.oreilly.co.jp/books/9784814401154/),
  by Jay Alammar and Maarten Grootendorst: background on tokenization,
  Transformers, text generation, and constrained sampling.
- [ゼロから作るDeep Learning (Deep learning from scratch, in Japanese)](https://www.oreilly.co.jp/books/9784873117584/),
  by Koki Saito: neural network fundamentals and their Python implementation.

AI assistance was used to read the subject, diagnose
failed model outputs, and review consistency between code and documentation.
The input data and SDK were supplied beforehand. 
