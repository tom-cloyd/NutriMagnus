#!/usr/bin/env python3
"""numa.py — CLI entry point for the numa nutritional analysis program.
version 2026-04-03 - 18:00
"""

import argparse

from numa_app.main import run_app


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="numa — nutritional analysis")
    parser.add_argument(
        "--theme",
        choices=["dark", "light", "neutral", "auto"],
        help="Set color theme: dark, light, neutral, auto",
    )
    parser.add_argument(
        "--api-key",
        help="Set USDA FoodData Central API key and exit",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_app(theme=args.theme, api_key=args.api_key)
