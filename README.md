Finance Playground
==============================
<br>

<blockquote><p class="quotation">
<span class="first-letter">U</span>ncertainty must be taken in a sense radically distinct from the familiar notion of Risk, from which it has never been properly separated.... The essential fact is that 'risk' means in some cases a quantity susceptible of measurement, while at other times it is something distinctly not of this character; and there are far-reaching and crucial differences in the bearings of the phenomena depending on which of the two is really present and operating.... It will appear that a measurable uncertainty, or 'risk' proper, as we shall use the term, is so far different from an unmeasurable one that it is not in effect an uncertainty at all <footer>— <b>Frank Knight</b></footer>
</blockquote>

<br>

Our aim with the Finance Playground is to explore and analyze financial instruments (particularly stocks and options) and develop profitable trading strategies. To that end, we focus on the relation between price time-series and other factors such as market volatility, interest rates, and various economic indicators.

We started this as a learning tool. As developers, we advocate a hands-on approach, we like trying out ideas and tinkering with models.

Collaboration is welcome: by all means, if you spot a mistake or just want to add an interesting analysis you've been playing with, please submit a pull request to the project's [Github repository](https://github.com/lambdaclass/finance_playground/).

<br>

## Setup

Requires Python >= 3.11. We use [Nix](https://nixos.org/) for the dev environment and [uv](https://docs.astral.sh/uv/) for Python dependencies.

```bash
# Enter the dev shell (provides Python 3.13, uv, make)
nix develop

# Install core dependencies
make setup

# Install competition dependencies (ML, Bayesian, deep learning)
make sync-all

# Run all self-contained analyses
make run

# Compile-check all Python files
make check
```

Without Nix, install Python >= 3.11 and uv manually, then use `uv sync` / `uv sync --extra competitions`.

<br>

## Research

Each topic lives in its own directory under `research/` with a `run.py` that reproduces all charts.

### Ergodicity Economics

- [Ergodicity and Insurance](research/ergodicity_and_insurance/) — Non-ergodic dynamics, the insurance puzzle, and time-average growth rates.
- [Evaluating Gambles](research/evaluating_gambles/) — Expected values, the St. Petersburg paradox, utility functions, and Kelly criterion.
- [Cooperation and Ergodicity](research/cooperation_and_ergodicity/) — Why cooperation emerges under evolutionary dynamics.
- [Wealth Redistribution (RGBM)](research/wealth_redistribution_rgbm/) — Wealth inequality simulation under re-allocating GBM.

### Portfolio & Options

- [Diversification — Holy Grail](research/diversification_holy_grail/) — Ray Dalio's insight on uncorrelated return streams.
- [Argentina ADR Volatility](research/argentina_adr_volatility/) — The August 2019 crash, return distributions, and volatility smiles.
- [Options Strategies](research/options_strategies/) — Straddle and iron butterfly backtests on SPX data.

### Competition Entries

- [Soy Futures Forecasting](research/soy_futures_forecasting/) — 2019 Metadata competition (3rd place). ARIMA, Prophet, Bayesian AR, and BSTS models.
- [Rainfall Forecasting](research/rainfall_forecasting/) — 2020 Metadata competition. LSTM, wavelet, and correlation analysis.

### Archived

- [Archive](archive/) — Notebooks that require unavailable private data or API keys.

<br>

## References

- [Investopedia: Ray Dalio breaks down his "Holy Grail".](https://www.investopedia.com/video/play/ray-dalio-his-portfolio-holy-grail/)
- [Insurance makes wealth grow faster.](https://arxiv.org/abs/1507.04655) - _Peters & Adamou_
- [An evolutionary advantage of cooperation.](https://arxiv.org/abs/1506.03414) - _Peters & Adamou_
- [Wealth Inequality and the Ergodic Hypothesis: Evidence from the United States.](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2794830) - _Berman, Peters & Adamou_
- [Ergodicity Economics: Lecture notes.](https://ergodicityeconomics.com/lecture-notes/) - _Ole Peters_

### Data sources

#### Exchanges
- [IEX](https://iextrading.com/developer/)
- [CBOE Options Data](http://www.cboe.com/delayedquote/quote-table-download)

#### Historical Data
- [Tiingo](https://api.tiingo.com/)
- [Sharadar](http://www.sharadar.com)
- [Quandl](https://www.quandl.com/)
- [Intrinio](https://intrinio.com/)
- [Xignite](http://www.xignite.com/)
- [Shiller's US Stocks, Dividends, Earnings, Inflation (CPI), and long term interest rates](http://www.econ.yale.edu/~shiller/data.htm)
- [Fama/French US Stock Index Data](http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html)
- [FRED CPI, Interest Rates, Trade Data](https://fred.stlouisfed.org)
- [REIT Data](https://www.reit.com/data-research/reit-market-data/reit-industry-financial-snapshot)
- [Historical Data: International monthly government bond returns](https://eur.figshare.com/articles/Data_Treasury_Bond_Return_Data_Starting_in_1962/8152748)
- [Treasury Bond Return Data Starting in 1962](https://www.mdpi.com/2306-5729/4/3/91)
- [The 2019 Global Investment Returns Yearbook](https://www.credit-suisse.com/about-us-news/en/articles/news-and-expertise/global-investment-returns-yearbook-201902.html)
- [Centro de Estadísticas de Mercado - ROFEX](https://www.rofex.com.ar/cem/Fyo.aspx)
