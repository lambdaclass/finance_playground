[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/lambdaclass/finance_playground/master)
[![Build Status](https://travis-ci.org/lambdaclass/finance_playground.svg?branch=master)](https://travis-ci.org/lambdaclass/finance_playground)

Finance Playground
==============================

> In God we trust, all others bring data - William Edwards Deming

> I am not interested in proofs, but only in what nature does - Paul Dirac

> Uncertainty must be taken in a sense radically distinct from the familiar notion of Risk, from which it has never been properly separated.... The essential fact is that 'risk' means in some cases a quantity susceptible of measurement, while at other times it is something distinctly not of this character; and there are far-reaching and crucial differences in the bearings of the phenomena depending on which of the two is really present and operating.... It will appear that a measurable uncertainty, or 'risk' proper, as we shall use the term, is so far different from an unmeasurable one that it is not in effect an uncertainty at all - Frank Knight

In this project our aim is to explore and analyse financial instruments (stocks and options in particular) and to develop profitable trading strategies. To that end, we focused on the relation between price time series and factors such as market volatility, interest rates, and various economic indicators.  
We started this as a learning tool. As developers, we advocate a hands on approach, we like trying out ideas and tinkering with models. If that sounds at all interesting, you can follow our progress which will be documented in Jupyter notebooks [here](https://mybinder.org/v2/gh/lambdaclass/finance_playground/master).

Collaboration is welcome: by all means, if you spot a mistake or just want to add an interesting notebook you've been playing with, please submit a pull request.


## Notebooks

- [Introduction to Finance](https://lambdaclass.com/finance_playground/intro-finance.html) - Basic concepts in Finance (stocks, ETFs, options) \[[slides](https://lambdaclass.com/finance_playground/intro-finance.slides.html)\]
- [The Holy Grail of Investing](https://lambdaclass.com/finance_playground/diversification-dalio-holy-grail.html) - On Ray Dalio's insights into the benefits of [diversification](https://www.investopedia.com/video/play/ray-dalio-his-portfolio-holy-grail/).
- [Ergodicity Explorations](https://lambdaclass.com/finance_playground/ergodicity/ergodicity-explorations.html) - Based on the [research](https://ergodicityeconomics.com/lecture-notes/) from Professor Ole Peters regarding [insurance](https://arxiv.org/abs/1507.04655) contracts, expectation values and time averages.
- [Evaluating Gambles](https://lambdaclass.com/finance_playground/ergodicity/evaluating-gambles-presentation.html) - Continuing on our explorations on how to evaluate gambles and optimal betting criteria. \[[slides](https://lambdaclass.com/finance_playground/ergodicity/evaluating-gambles-presentation.slides.html)\]
- [Emergence of Cooperation in Evolutionary Systems](https://lambdaclass.com/finance_playground/ergodicity/emergence-of-cooperation.html) - An ergodic explanation for the advantage of [cooperation](https://arxiv.org/abs/1506.03414) under evolutionary dynamics.
- [Re-allocating GBM wealth distribution model](https://lambdaclass.com/finance_playground/ergodicity/RGBM.html) - Model simulation based on a [paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2794830) by Adamou, Bernam and Peters 2019. You can also try out this [interactive animation](https://lambdaclass.com/finance_playground/rgbm_animation/index.html).
- [Troubled Markets](https://lambdaclass.com/finance_playground/options/0.6-troubled-markets-and-volatility.html) - An exploration on Argentina's ADRs recent performance (2019) \[[slides](https://lambdaclass.com/finance_playground/options/0.6-troubled-markets-and-volatility.slides.html)\]


## Requirements

- Python >= 3.6
- pipenv
- [Node](https://nodejs.org) (to build interactive animations)

## Usage

If you want to view the notebooks locally, simply install the dependencies with:

```shell
$ pipenv --three && pipenv install
```

Then start Jupyter Lab

```shell
$ cd notebooks && jupyter lab
```

# Mathematics, science and engineering
Before diving into the notebooks we recommend you read this great quote by Emanuel Derman in his book The Volatility Smile:

>Mathematics requires axioms and postulates, from which mathematicians then derive the logical consequences. In geometry, for example, Euclid's axioms are meant to describe self-evident relationships of parts of things to the whole, and his postulates further describe supposedly self-evident properties of points and lines. One Euclidean axiom is that things that are equal to
the same thing are equal to each other. One Euclidean postulate, for example, is that it is always possible to draw a straight line between any two points.
Euclid's points and lines are abstracted from those of nature. When you get familiar enough with the abstractions, they seem almost tangible. Even more esoteric abstractions—infinite-dimensional Hilbert spaces that
form the mathematical basis of quantum mechanics, for example—seem real and visualizable to mathematicians. Nevertheless, the theorems of mathematics are relations between abstractions, not between the realities
that inspired them.
Science, in contradistinction to mathematics, formulates laws. Laws are about observable behavior. They describe the way the universe works. Newton's laws allow us to guide rockets to the moon. Maxwell's equations enable the construction of radios and TV sets. The laws of thermodynamics make possible the construction of combustion engines that convert heat into mechanical energy.
>
>Finance is concerned with the relations between the values of securities and their risk, and with the behavior of those values. It aspires to be a practical field, like physics or chemistry or electrical engineering. As John Maynard Keynes once remarked about economics, "If economists could manage to get themselves thought of as humble, competent people on a level with dentists, that would be splendid." Dentists rely on science, engineering, empirical knowledge, and heuristics, and there are no theorems in dentistry. Similarly, one would hope that finance would be concerned with laws rather than theo-
rems, with behavior rather than assumptions. One doesn't seriously describe the behavior of a market with theorems
>
>Engineering is concerned with building machines or devices. A device is a little part of the universe, more or less isolated, that, starting from the constructed initial conditions, obeys the laws of its field and, while doing so,
performs something we regard as useful.
Let's start by thinking about more familiar types of engineering. Mechanical engineering is concerned with building devices based on the principles of mechanics (i.e., Newton's laws), suitably combined with empirical rules about more complex forces that are too difficult to derive from first principles (friction, for example). Electrical engineering is the study of how to create useful electrical devices based on Maxwell's equations and quantum mechanics. Bioengineering is the art of building prosthetics and
biologically active devices based on the principles of biochemistry, physiology, and molecular biology.
Science—mechanics, electrodynamics, molecular biology, and so on seeks to discover the fundamental principles that describe the world, and is usually reductive. Engineering is about using those principles, constructively,
to create functional devices.
What about financial engineering? In a logically consistent world, financial engineering, layered above a solid base of financial science, would be the study of how to create useful financial devices (convertible bonds, warrants, volatility swaps, etc.) that perform in desired ways. This brings us to financial science, the putative study of the fundamental laws of financial objects, be
they stocks, interest rates, or whatever else your theory uses as constituents. Here, unfortunately, be dragons.
>
>Financial engineering rests upon the mathematical fields of calculus, probability theory, stochastic processes, simulation, and Brownian motion. These fields can capture some of the essential features of the uncertainty we deal with in markets, but they don't accurately describe the characteristic behavior of financial objects. Markets are plagued with anomalies that violate standard financial theories (or, more accurately, theories are plagued by their inability to systematically account for the actual behavior of markets). For example, the negative return on a single day during the crash of 1987 was so many historical standard deviations away from the mean that it should never have occurred in our lifetime if returns were normally distributed. More recently, JPMorgan called the events of the "London Whale" an eight-standard-deviation event (JPMorgan Chase & Co. 2013). 
>
>Stock evolution, to take just one of many examples, isn't Brownian. So, while financial engineers are rich in mathematical techniques, we don't have the right laws of science to exploit—not now, and maybe not ever.
Because we don't have the right laws, the axiomatic approach to finance is problematic. Axiomatization is appropriate in a field like geometry, where one can postulate any set of axioms not internally inconsistent, or even in Newtonian mechanics, where there are scientific laws that hold with such great precision that they can be effectively regarded as axioms. But in finance, as all practitioners know, our "axioms" are not nearly as good. As Paul Wilmott wrote, "every financial axiom ... ever seen is demonstrably wrong. The real question is how wrong" (Wilmott 1998). Teaching by axiomatization is therefore even less appropriate in finance than it is in real science.
If finance is about anything, it is about the messy world we inhabit. It's best to learn axioms only after you've acquired intuition.
Mathematics is important, and the more mathematics you know the better off you're going to be. But don't fall too in love with mathematics. The problems of financial modeling are less mathematical than they are conceptual. In this book, we want to first concentrate on understanding concepts and their implementation, and then use mathematics as a tool. We're less interested here in great numerical accuracy or computational efficiency than in making the ideas we're using clear.
We know so little that is absolutely right about the fundamental behavior of assets. Are there really strict laws they satisfy? Are those laws stationary? It's best to assume as little as possible and rely on models as little as possible. And when we do rely on models, simpler is better. With that in mind, we proceed to a brief overview of the principles of financial modeling.

## Recommended reading

For complete novices in finance and economics, this [post](https://notamonadtutorial.com/how-to-earn-your-macroeconomics-and-finance-white-belt-as-a-software-developer-136e7454866f) gives a comprehensive introduction.

### Papers and Posts
- [Dennis Rodman and the Art of Portfolio Optimization](https://www.artemiscm.com/s/Artemis-Research_Dennis-Rodman-and-Portfolio-Optimization_April2016-efr3.pdf)
- [Doing a Laplace](https://ergodicityeconomics.com/2017/07/18/doing-a-laplace/)
- [What’s a growth rate, really?](https://ergodicityeconomics.com/2019/03/13/whats-a-growth-rate-really/)
- [Volatility: A New Return Driver?](http://static.squarespace.com/static/53974e3ae4b0039937edb698/t/53da6400e4b0d5d5360f4918/1406821376095/Directional%20Volatility%20Research.pdf) - Greggory Flinn, Roger J. Schreiner
- [Easy Volatility Investing](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2255327) - Tony Cooper (2013)
- [Everybody’s Doing It: Short Volatility Strategies and Shadow Financial Insurers](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3071457) - Vineer Bhansali, Lawrence Harris (2018)
- [Volatility-of-Volatility Risk](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2497759)- Darien Huang, Christian Schlag, Ivan Shaliastovich, Julian Thimme (2018)
- [Four Points Beginner Risk Managers Should Learn from Jeff Holman’s Mistakes in the Discussion of Antifragile - Taleb](https://arxiv.org/pdf/1401.2524.pdf)
- [The Distribution of Returns](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2828744) - David E. Harris (2017)
- [Safe Haven Investing Part I - Not all risk mitigation is created equal](https://www.universa.net/UniversaResearch_SafeHavenPart1_RiskMitigation.pdf) - Universa Investments (2017)
- [Safe Haven Investing Part II - Not all risk is created equal](https://www.universa.net/UniversaResearch_SafeHavenPart2_NotAllRisk.pdf) - Universa Investments (2017)
- [Safe Haven Investing Part III - Those wonderful tenbaggers](https://www.universa.net/UniversaResearch_SafeHavenPart3_Tenbaggers.pdf) - Universa Investments (2017)
- [Insurance makes wealth grow faster](https://arxiv.org/abs/1507.04655) - Ole Peters, Alexander Adamou (2017)
- [Ergodicity economics](https://ergodicityeconomics.files.wordpress.com/2018/06/ergodicity_economics.pdf) - Ole Peters (2018)
- [The Rate of Return on Everything, 1870–2015](https://economics.harvard.edu/files/economics/files/ms28533.pdf) - Oscar Jorda, Katharina Knoll, Dmitry Kuvshinov, Moritz Schularick, Alan M. Taylor (2019)
- [Volatility and the Alchemy of Risk](https://static1.squarespace.com/static/5581f17ee4b01f59c2b1513a/t/59ea16dbbe42d6ff1cae589f/1508513505640/Artemis_Volatility+and+the+Alchemy+of+Risk_2017.pdf) - Artemis Capital Management (2017)
- [Trading Volatility](https://inference-review.com/article/trading-volatility) - Emanuel Derman
- [Trends Everywhere](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3386035) - Abhilash Babu, Ari Levine, Yao Hua Ooi, Lasse Heje Pedersen, Erik Stamelos (2018)
- [A Century of Evidence on Trend-Following Investing - AQR](https://www.aqr.com/Insights/Research/Journal-Article/A-Century-of-Evidence-on-Trend-Following-Investing)
- [Why Not 100% Equities - AQR](https://www.aqr.com/Insights/Research/Journal-Article/Why-Not--Equities)
- [Risk premia: asymmetric tail risks and excess returns - Bouchaud](https://www.tandfonline.com/doi/full/10.1080/14697688.2016.1183035)
- [Black Scholes and the normal distribution](https://mathbabe.org/2013/03/12/black-scholes-and-the-normal-distribution/)
- [Why log returns?](https://mathbabe.org/2011/08/30/why-log-returns/)
- [The Variation of Some Other Speculative Prices - Benoit Mandelbrot](https://web.williams.edu/Mathematics/sjmiller/public_html/341Fa09/econ/Mandelbroit_VariationCertainSpeculativePrices.pdf)
- [A New Heuristic Measure of Fragility and Tail Risks : Application to Stress Testing -  Schmieder, Kinda, Taleb, Loukoianova, Canetti ](https://www.imf.org/en/Publications/WP/Issues/2016/12/31/A-New-Heuristic-Measure-of-Fragility-and-Tail-Risks-Application-to-Stress-Testing-26222)
- [Fallibility, Reflexivity, and the Human Uncertainty Principle - George Soros](https://www.georgesoros.com/2014/01/13/fallibility-reflexivity-and-the-human-uncertainty-principle-2/)
- [Option Pricing Under Power Laws: A Robust Heuristic - Taleb](https://arxiv.org/pdf/1908.02347)

### Books

#### Introductory
- Option Volatility and Pricing 2nd Ed. - Natemberg (2014)
- Options, Futures, and Other Derivatives 10th Ed. - Hull (2017)
- Trading Options Greeks: How Time, Volatility, and Other Pricing Factors Drive Profits 2nd Ed. - Passarelli (2012)

#### Intermediate
- Trading Volatility - Bennet (2014)
- Volatility Trading 2nd Ed. - Sinclair (2013)

#### Advanced
- Dynamic Hedging - Taleb (1997)
- The Volatility Surface: A Practitioner's Guide - Gatheral (2006)
- The Volatility Smile - Derman & Miller (2016)

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
