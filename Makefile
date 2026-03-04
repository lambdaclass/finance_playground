.PHONY: setup sync check run clean
.PHONY: run-ergodicity run-gambles run-cooperation run-rgbm run-diversification run-adr
.PHONY: run-options run-soy run-rainfall

# ── Setup ────────────────────────────────────────────────────────────
setup: sync

sync:
	uv sync

sync-all:
	uv sync --extra competitions

# ── Quality ──────────────────────────────────────────────────────────
check:
	@echo "Compile-checking all Python files..."
	@find scripts research -name '*.py' | while read f; do \
		python -m py_compile "$$f" || exit 1; \
	done
	@echo "All .py files compile successfully."

# ── Run all self-contained scripts ───────────────────────────────────
run: run-ergodicity run-gambles run-cooperation run-rgbm run-diversification run-adr

run-ergodicity:
	uv run python research/ergodicity_and_insurance/run.py

run-gambles:
	uv run python research/evaluating_gambles/run.py

run-cooperation:
	uv run python research/cooperation_and_ergodicity/run.py

run-rgbm:
	uv run python research/wealth_redistribution_rgbm/run.py

run-diversification:
	uv run python research/diversification_holy_grail/run.py

run-adr:
	uv run python research/argentina_adr_volatility/run.py

# ── Competition scripts (need extra deps) ────────────────────────────
run-options:
	uv run python research/options_strategies/run.py

run-soy:
	uv run python research/soy_futures_forecasting/run.py

run-rainfall:
	uv run python research/rainfall_forecasting/run.py

# ── Clean ────────────────────────────────────────────────────────────
clean:
	find research -type d -name charts -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
