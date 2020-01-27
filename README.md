[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/lambdaclass/finance_playground/master)
[![Build Status](https://travis-ci.org/lambdaclass/finance_playground.svg?branch=master)](https://travis-ci.org/lambdaclass/finance_playground)

Finance Playground
==============================
<br></br>

<blockquote><p class="quotation"> 
<span class="first-letter">U</span>ncertainty must be taken in a sense radically distinct from the familiar notion of Risk, from which it has never been properly separated.... The essential fact is that 'risk' means in some cases a quantity susceptible of measurement, while at other times it is something distinctly not of this character; and there are far-reaching and crucial differences in the bearings of the phenomena depending on which of the two is really present and operating.... It will appear that a measurable uncertainty, or 'risk' proper, as we shall use the term, is so far different from an unmeasurable one that it is not in effect an uncertainty at all <footer>— <b>Frank Knight</b></footer>
</blockquote>

In this project our aim is to explore and analyse financial instruments (stocks and options in particular) and to develop profitable trading strategies. To that end, we focused on the relation between price time series and factors such as market volatility, interest rates, and various economic indicators.  
We started this as a learning tool. As developers, we advocate a hands on approach, we like trying out ideas and tinkering with models. If that sounds at all interesting, you can follow our progress which will be documented in Jupyter notebooks [here](https://mybinder.org/v2/gh/lambdaclass/finance_playground/master).

Collaboration is welcome: by all means, if you spot a mistake or just want to add an interesting notebook you've been playing with, please submit a pull request.

## Notebooks

- [Introduction to Finance](https://lambdaclass.com/finance_playground/intro_finance) -Basic concepts in Finance (stocks, ETFs, options) \[[slides](https://lambdaclass.com/finance_playground/intro-finance.slides.html)\]
- [The Holy Grail of Investing](https://lambdaclass.com/finance_playground/diversification_dalio_holy_grail) - On Ray Dalio's insights into the benefits of [diversification](https://www.investopedia.com/video/play/ray-dalio-his-portfolio-holy-grail/).
- [Ergodicity Explorations](https://lambdaclass.com/finance_playground/ergodicity_explorations) - Based on the [research](https://ergodicityeconomics.com/lecture-notes/) from Professor Ole Peters regarding [insurance](https://arxiv.org/abs/1507.04655) contracts, expectation values and time averages.
- [Evaluating Gambles](https://lambdaclass.com/finance_playground/evaluating_gambles) - Continuing on our explorations on how to evaluate gambles and optimal betting criteria. \[[slides](https://lambdaclass.com/finance_playground/ergodicity/evaluating-gambles-presentation.slides.html)\]
- [Emergence of Cooperation in Evolutionary Systems](https://lambdaclass.com/finance_playground/emergence_of_cooperation) - An ergodic explanation for the advantage of [cooperation](https://arxiv.org/abs/1506.03414) under evolutionary dynamics.
- [Re-allocating GBM wealth distribution model](https://lambdaclass.com/finance_playground/ergodicity/RGBM.html) - Model simulation based on a [paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2794830) by Adamou, Bernam and Peters 2019. You can also try out this [interactive animation](https://lambdaclass.com/finance_playground/rgbm_animation/index.html).
- [Troubled Markets](https://lambdaclass.com/finance_playground/troubled_markets_and_volatility) - An exploration on Argentina's ADRs recent performance (2019) \[[slides](https://lambdaclass.com/finance_playground/options/0.6-troubled-markets-and-volatility.slides.html)\]
- [2019 Metadata Forcasting Competition](https://lambdaclass.com/finance_playground/metadata-2019/soy-price-prediction.html) - Our entry to the 2019 soy price forecasting competition organized by [Fundación Sadosky](http://www.fundacionsadosky.org.ar).

## Data sources

### Exchanges

- [IEX](https://iextrading.com/developer/)
- [CBOE Options Data](http://www.cboe.com/delayedquote/quote-table-download)

### Historical Data

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
- [The 2019 Global lnvestment Returns Yearbook: 119 years of financial history and analysis](https://www.credit-suisse.com/about-us-news/en/articles/news-and-expertise/global-investment-returns-yearbook-201902.html)
- [Centro de Estadísticas de Mercado - ROFEX](https://www.rofex.com.ar/cem/Fyo.aspx)
