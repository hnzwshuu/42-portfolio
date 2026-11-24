"""Select a function name by scoring complete candidates with the model."""

import json
from typing import Any

import numpy as np

from src.decoding import encode


def _encode_candidates(
    model: Any,
    choices: list[str],
    max_tokens: int,
) -> list[list[int]]:
    """Encode candidate names as quoted JSON strings.

    Args:
        model: SDK model providing tokenization.
        choices: Function names to encode.
        max_tokens: Maximum token count per encoded candidate.

    Returns:
        Candidate token lists in the same order as choices.

    Raises:
        ValueError: If candidates are missing, an encoding is empty, or a
            candidate exceeds the token budget.
    """
    candidate_token_lists: list[list[int]] = []
    for function_name in choices:
        json_name = json.dumps(function_name, ensure_ascii=False)
        token_ids = encode(model, json_name)
        candidate_token_lists.append(token_ids)

    if not candidate_token_lists:
        raise ValueError('Function selection requires candidates.')
    if any(not token_ids for token_ids in candidate_token_lists):
        raise ValueError('Function names must not be empty.')
    if any(
        len(token_ids) > max_tokens
        for token_ids in candidate_token_lists
    ):
        raise ValueError('A function name exceeds the token budget.')
    return candidate_token_lists


def _average_log_probability(
    model: Any,
    model_input_ids: list[int],
    candidate_token_ids: list[int],
) -> float:
    """Compute a candidate's mean conditional log probability.

    Args:
        model: SDK model providing next-token logits.
        model_input_ids: Context tokens preceding the candidate.
        candidate_token_ids: Nonempty token sequence to score.

    Returns:
        Mean log probability, or negative infinity if a candidate token
        is unavailable or has a non-finite score.

    Raises:
        ValueError: If the SDK returns invalid logits or no finite scores.
    """
    current_input_ids = list(model_input_ids)
    total_log_probability = 0.0

    for token_id in candidate_token_ids:
        logits = np.asarray(
            model.get_logits_from_input_ids(current_input_ids),
            dtype=np.float64,
        )
        if logits.ndim != 1 or not logits.size:
            raise ValueError('The SDK returned invalid selection logits.')

        logits[~np.isfinite(logits)] = -np.inf
        if not np.isfinite(logits).any():
            raise ValueError('The SDK returned no finite logits.')

        if token_id >= len(logits) or not np.isfinite(logits[token_id]):
            return -np.inf

        normalizer = float(np.logaddexp.reduce(logits))
        total_log_probability += float(logits[token_id]) - normalizer
        current_input_ids.append(token_id)

    return total_log_probability / len(candidate_token_ids)


def select_json_string(
    model: Any,
    model_input_ids: list[int],
    choices: list[str],
    max_tokens: int,
) -> str:
    """Select the candidate with the highest mean log probability.

    Args:
        model: SDK model providing tokenization and logits.
        model_input_ids: Context tokens preceding the candidate.
        choices: Candidate names, each scored as a complete JSON string.
        max_tokens: Maximum token count per candidate.

    Returns:
        The selected name without JSON quotes. Ties favor the first name.

    Raises:
        ValueError: If candidates or logits are invalid, a candidate
            exceeds the token budget, or no candidate has a finite score.
    """
    candidate_token_lists = _encode_candidates(
        model,
        choices,
        max_tokens,
    )

    best_choice: str | None = None
    best_score = -np.inf

    for choice, token_ids in zip(choices, candidate_token_lists):
        score = _average_log_probability(
            model,
            model_input_ids,
            token_ids,
        )
        if score > best_score:
            best_choice = choice
            best_score = score

    if best_choice is None:
        raise ValueError(
            'No available function name has a finite model score.'
        )
    return best_choice
