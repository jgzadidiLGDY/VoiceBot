from __future__ import annotations

import argparse
import json
import sys

from app.call_runner import run_call_by_scenario_id, run_default_call
from app.config import Settings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scenario",
        type=str,
        default="schedule_new_patient",
        help="Scenario ID to run.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        settings = Settings.from_env()

        if args.scenario:
            result = run_call_by_scenario_id(settings, args.scenario)
        else:
            result = run_default_call(settings)

        print("\n=== Call Result ===")
        print(json.dumps(result, indent=2))
        return 0
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        return 130
    except Exception as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())