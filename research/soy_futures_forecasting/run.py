#!/usr/bin/env python3
"""Soy futures price forecasting — Metadata 2019 competition entry (3rd place).

Orchestrator that runs individual forecasting models. Each model can also
be run standalone.

Usage:
    python run.py              # run all models
    python run.py arima        # ARIMA only
    python run.py prophet      # Prophet only
    python run.py bayesian     # Bayesian AR only
    python run.py bsts         # BSTS only
"""

import sys
import importlib


MODELS = {
    "arima": "run_arima",
    "prophet": "run_prophet",
    "bayesian": "run_bayesian",
    "bsts": "run_bsts",
}


def main():
    args = sys.argv[1:]

    if not args or args[0] == "all":
        targets = list(MODELS.keys())
    else:
        targets = [a for a in args if a in MODELS]
        if not targets:
            print(f"Unknown model(s): {args}")
            print(f"Available: {', '.join(MODELS.keys())}, all")
            sys.exit(1)

    print("Soy Futures Forecasting")
    print("=" * 40)

    for name in targets:
        print(f"\n--- {name.upper()} ---")
        try:
            mod = importlib.import_module(MODELS[name])
            mod.main()
        except ImportError as e:
            print(f"  Skipping {name}: {e}")
        except Exception as e:
            print(f"  Error in {name}: {e}")

    print("\nAll done.")


if __name__ == "__main__":
    main()
