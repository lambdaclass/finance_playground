Finance Playground
==============================
<br>

<blockquote><p class="quotation">
<span class="first-letter">U</span>ncertainty must be taken in a sense radically distinct from the familiar notion of Risk, from which it has never been properly separated.... The essential fact is that 'risk' means in some cases a quantity susceptible of measurement, while at other times it is something distinctly not of this character; and there are far-reaching and crucial differences in the bearings of the phenomena depending on which of the two is really present and operating.... It will appear that a measurable uncertainty, or 'risk' proper, as we shall use the term, is so far different from an unmeasurable one that it is not in effect an uncertainty at all <footer>— <b>Frank Knight</b></footer>
</blockquote>

<br>

Our aim with the Finance Playground is to explore and analyze financial instruments (particularly stocks and options) and develop profitable trading strategies. To that end, we focus on the relation between price time-series and other factors such as market volatility, interest rates, and various economic indicators.

We started this as a learning tool. As developers, we advocate a hands-on approach, we like trying out ideas and tinkering with models.

Collaboration is welcome: by all means, if you spot a mistake or just want to add an interesting notebook you've been playing with, please submit a pull request to the project's [Github repository](https://github.com/lambdaclass/finance_playground/).

<br>

## Setup

Requires Python >= 3.11. We use [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Install uv (if you haven't already)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Launch JupyterLab
uv run jupyter lab
```

<br>

## Notebooks

- [Introduction to Finance](notebooks/intro-finance.ipynb) - Basic concepts in Finance (stocks, ETFs, options)
- [The Holy Grail of Investing](notebooks/diversification-dalio-holy-grail.ipynb) - On Ray Dalio's insights into the benefits of diversification.
- [Ergodicity Explorations](notebooks/ergodicity/ergodicity-explorations.ipynb) - Based on a research by Professor Ole Peters regarding insurance contracts, expectation values and time averages.
- [Evaluating Gambles](notebooks/ergodicity/evaluating-gambles-presentation.ipynb) - Continuing on our explorations on how to evaluate gambles and optimal betting criteria.
- [Emergence of Cooperation in Evolutionary Systems](notebooks/ergodicity/emergence-of-cooperation.ipynb) - An ergodic explanation for the advantage of cooperation under evolutionary dynamics.
- [Re-allocating GBM wealth distribution model](notebooks/ergodicity/RGBM.ipynb) - Model simulation based on a paper by Adamou, Berman and Peters 2019.
- [Troubled Markets](notebooks/options/0.6-troubled-markets-and-volatility.ipynb) - An exploration on Argentina's ADRs recent performance (2019).
- [2019 Metadata Forecasting Competition](notebooks/metadata-2019/soy-price-prediction.ipynb) - Our entry to the 2019 soybean futures forecasting competition organized by Fundación Sadosky and MATBA ROFEX, which ranked third.

### Options
- [Exploring Visualizations](notebooks/options/0.1-exploring-visualizations.ipynb)
- [Exploring Options Strategies](notebooks/options/0.2-exploring-options-strategies.ipynb)
- [HDF5 Store](notebooks/options/0.3-hdf5-store.ipynb)
- [Dask DataFrames](notebooks/options/0.4-dask-dataframes.ipynb)
- [Iron Butterfly](notebooks/options/0.5-iron-butterfly.ipynb)

### Rain Forecast
- [Rain Forecast](notebooks/metadata-2020/rain-forecast/rain-forecast.ipynb)
- [Neural Networks](notebooks/metadata-2020/rain-forecast/neural_networks.ipynb)
- [Model Analysis](notebooks/metadata-2020/rain-forecast/model_analysis.ipynb)

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
