#!/usr/bin/env python3
"""Rainfall maxima forecasting — Metadata 2020 competition entry.

Orchestrator for the three analysis scripts. Each can also be run standalone.

Usage:
    python run.py                   # run all
    python run.py exploration       # data exploration only
    python run.py neural_networks   # LSTM models only
    python run.py model_analysis    # correlation analysis only
"""

import sys
import importlib

MODULES = {
    "exploration": "run_exploration",
    "neural_networks": "run_neural_networks",
    "model_analysis": "run_model_analysis",
}


def main():
    args = sys.argv[1:]

    if not args or args[0] == "all":
        targets = list(MODULES.keys())
    else:
        targets = [a for a in args if a in MODULES]
        if not targets:
            print(f"Unknown module(s): {args}")
            print(f"Available: {', '.join(MODULES.keys())}, all")
            sys.exit(1)

    print("Rainfall Forecasting")
    print("=" * 40)

    for name in targets:
        print(f"\n--- {name.upper()} ---")
        try:
            mod = importlib.import_module(MODULES[name])
            mod.main()
        except ImportError as e:
            print(f"  Skipping {name}: {e}")
        except Exception as e:
            print(f"  Error in {name}: {e}")

    print("\nAll done.")


if __name__ == "__main__":
    main()
