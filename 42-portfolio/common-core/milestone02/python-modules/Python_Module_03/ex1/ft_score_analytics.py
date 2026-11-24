#!/usr/bin/env python3
import sys


def parse_scores(argv: list[str]) -> list[int]:
    index = 1
    scores: list[int] = []
    while index < len(argv):
        try:
            score = int(argv[index])
            scores = scores + [score]
        except ValueError:
            print(f"Invalid parameter: '{argv[index]}'")
        index += 1
    return scores


def main() -> None:
    print("=== Player Score Analytics ===")
    scores = parse_scores(sys.argv)
    if len(scores) == 0:
        print("No scores provided. \
Usage: python3 ft_score_analytics.py <score1> <score2> ...")
    else:
        print(f"Scores processed: {scores}")
        print(f"Total player: {len(scores)}")
        print(f"Total score: {sum(scores)}")
        print(f"Average score: {(sum(scores) / len(scores)):.1f}")
        print(f"High score: {max(scores)}")
        print(f"Low score: {min(scores)}")
        print(f"Score range: {max(scores) - min(scores)}")


if __name__ == "__main__":
    main()
