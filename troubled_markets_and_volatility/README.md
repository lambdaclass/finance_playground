# Troubled markets and volatility
### _Challenging financial models through an exploration on the crash of Argentina's ADRs_

[American Depositary Receipts](https://www.investopedia.com/terms/a/adr.asp) (ADRs) are financial instruments that allow US investors to purchase stocks in foreign companies. Argentina has a number of companies listed in US exchanges through ADRs.  
In this notebook, we will explore the performance of these ADRs with a focus on the period from January to August 2019, where political uncertainty sent markets into turmoil: the country’s Merval stock index fell 48% in dollar terms in a single day, the second-largest one-day drop in any of the 94 markets tracked by Bloomberg since 1950<sup>[1]</sup>, causing a 20% devaluation of the Argentine peso and a sharp drop in bond prices.  
We will be looking at the end-of-day data of the Argentine ADRs, and their corresponding put and call options, to examine whether the daily log returns of stocks are distributed normally, a conclusion that follows from the standard model due to [Bachelier](en.wikipedia.org/wiki/Louis_Bachelier).

[1]: https://www.ft.com/content/29764546-c821-11e9-a1f4-3669401ba76f


```python
%config InlineBackend.figure_format = 'retina'
%matplotlib inline

import os

import numpy as np
import pandas as pd
import warnings
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
import seaborn as sns

warnings.simplefilter('ignore')
register_matplotlib_converters()
```


```python
sns.set(rc={'figure.figsize': (12,8)})
```

## Data munging


```python
data_dir = 'data/'
```


```python
tickers = [
    'BMA', 'BFR', 'CEPU', 'CRESY', 'EDN', 'GGAL', 'SUPV', 'IRS',
    'IRCP', 'LOMA', 'NTL', 'MELI', 'PAM', 'PZE', 'TEO', 'TS', 'TX',
    'TGS', 'YPF'
]

dfs = [pd.read_csv(os.path.join(data_dir, ticker.lower() + '.csv')) for ticker in tickers]

adrs_df = pd.concat(dfs, axis=0, ignore_index=False)
adrs_df.to_csv(os.path.join(data_dir, 'adrs.csv'), index=False)
```

Next we'll concatenate all options daily files into a csv.


```python
dfs = []

for root, dirs, files in os.walk(data_dir):
    if root.endswith('daily'):
        for file in files:
            df = pd.read_csv(os.path.join(root, file))
            dfs.append(df)
            
adr_options = pd.concat(dfs, axis=0)
adr_options.to_csv(os.path.join(data_dir, 'adr_options.csv'), index=False)
```

## Exploration

We begin our exploration of the end-of-day (EOD) data for Argentina's ADRs.


```python
adrs_df = pd.read_csv(os.path.join(data_dir, 'adrs.csv'), index_col='date', parse_dates=['date'])
adrs_df.index = pd.DatetimeIndex(adrs_df.index.date, name='date')
adrs_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>symbol</th>
      <th>close</th>
      <th>high</th>
      <th>low</th>
      <th>open</th>
      <th>volume</th>
      <th>adjClose</th>
      <th>adjHigh</th>
      <th>adjLow</th>
      <th>adjOpen</th>
      <th>adjVolume</th>
      <th>divCash</th>
      <th>splitFactor</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2006-03-27</th>
      <td>BMA</td>
      <td>23.05</td>
      <td>23.05</td>
      <td>22.23</td>
      <td>22.89</td>
      <td>1065200</td>
      <td>15.524521</td>
      <td>15.524521</td>
      <td>14.972239</td>
      <td>15.416759</td>
      <td>1065200</td>
      <td>0.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>2006-03-28</th>
      <td>BMA</td>
      <td>22.38</td>
      <td>22.47</td>
      <td>21.90</td>
      <td>22.47</td>
      <td>1556100</td>
      <td>15.073266</td>
      <td>15.133883</td>
      <td>14.749979</td>
      <td>15.133883</td>
      <td>1556100</td>
      <td>0.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>2006-03-29</th>
      <td>BMA</td>
      <td>22.84</td>
      <td>23.14</td>
      <td>22.05</td>
      <td>22.10</td>
      <td>641300</td>
      <td>15.383083</td>
      <td>15.585138</td>
      <td>14.851006</td>
      <td>14.884682</td>
      <td>641300</td>
      <td>0.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>2006-03-30</th>
      <td>BMA</td>
      <td>22.75</td>
      <td>23.10</td>
      <td>22.70</td>
      <td>23.00</td>
      <td>293600</td>
      <td>15.322467</td>
      <td>15.558197</td>
      <td>15.288791</td>
      <td>15.490846</td>
      <td>293600</td>
      <td>0.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>2006-03-31</th>
      <td>BMA</td>
      <td>22.93</td>
      <td>22.93</td>
      <td>22.35</td>
      <td>22.83</td>
      <td>113600</td>
      <td>15.443700</td>
      <td>15.443700</td>
      <td>15.053061</td>
      <td>15.376348</td>
      <td>113600</td>
      <td>0.0</td>
      <td>1.0</td>
    </tr>
  </tbody>
</table>
</div>



The data is indexed by date, with the `symbol` column holding the ticker name, and columns for the `open` and `close` prices (the price of the symbol at the start/end of the market day) and the `high` and `low` prices seen for the symbol at that date.  
We'll begin plotting the [`adjusted close`](http://www.crsp.com/products/documentation/crsp-calculations) prices for each symbol (price adjusted for dividends payed and stock splits). The reset of the columns can be safely ingored for our purposes.


```python
g = sns.relplot(x='date', y='adjClose', col='symbol', hue='symbol',
            facet_kws=dict(sharey=False, sharex=False), col_wrap=3, legend=False,
            kind='line', data=adrs_df.reset_index())

g.fig.suptitle("Daily ajusted close prices for Argentina's ADRs (USD)", size=16)
g.fig.subplots_adjust(top=.96);
```


![png](img/0.6-troubled-markets-and-volatility_13_0.png)


Let's zoom in on the 2019 adjusted close prices.


```python
adrs_2019 = adrs_df.loc['2019']

g = sns.relplot(x='date', y='adjClose', col='symbol', hue='symbol',
            facet_kws=dict(sharey=False, sharex=False), col_wrap=3, legend=False,
            kind='line', data=adrs_2019.reset_index())

g.fig.suptitle("Daily ajusted close prices for Argentina's ADRs (USD) in 2019", size=16)
g.fig.subplots_adjust(top=.96);
```


![png](img/0.6-troubled-markets-and-volatility_15_0.png)


We can see most stocks experienced a sharp decline in August 2019, after a surprise result of the presidential primaries caused a market crash. We also see that \\$MELI (MercadoLibre) is less vulnerable to the volatility in the Argentine market because it operates in over a dozen countries in Latin America.


```python
adrs_df.groupby('symbol')['adjClose'].describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>count</th>
      <th>mean</th>
      <th>std</th>
      <th>min</th>
      <th>25%</th>
      <th>50%</th>
      <th>75%</th>
      <th>max</th>
    </tr>
    <tr>
      <th>symbol</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>BFR</th>
      <td>4936.0</td>
      <td>8.279068</td>
      <td>5.706390</td>
      <td>0.744824</td>
      <td>3.953318</td>
      <td>5.724786</td>
      <td>12.029480</td>
      <td>25.454491</td>
    </tr>
    <tr>
      <th>BMA</th>
      <td>3371.0</td>
      <td>35.178278</td>
      <td>25.470378</td>
      <td>4.999717</td>
      <td>15.792980</td>
      <td>24.600919</td>
      <td>48.906183</td>
      <td>125.424911</td>
    </tr>
    <tr>
      <th>CEPU</th>
      <td>386.0</td>
      <td>10.988264</td>
      <td>2.897472</td>
      <td>3.460000</td>
      <td>9.060000</td>
      <td>9.975000</td>
      <td>12.277500</td>
      <td>17.919462</td>
    </tr>
    <tr>
      <th>CRESY</th>
      <td>4936.0</td>
      <td>9.937665</td>
      <td>3.951959</td>
      <td>2.923092</td>
      <td>6.744933</td>
      <td>9.466466</td>
      <td>12.010526</td>
      <td>21.638971</td>
    </tr>
    <tr>
      <th>EDN</th>
      <td>3099.0</td>
      <td>15.310731</td>
      <td>12.471194</td>
      <td>1.710000</td>
      <td>6.330000</td>
      <td>12.110000</td>
      <td>20.245000</td>
      <td>62.550000</td>
    </tr>
    <tr>
      <th>GGAL</th>
      <td>4795.0</td>
      <td>13.551952</td>
      <td>13.195641</td>
      <td>0.211733</td>
      <td>5.404357</td>
      <td>7.966350</td>
      <td>16.436948</td>
      <td>71.458310</td>
    </tr>
    <tr>
      <th>IRCP</th>
      <td>3971.0</td>
      <td>15.634198</td>
      <td>14.424214</td>
      <td>1.293231</td>
      <td>4.377059</td>
      <td>10.018225</td>
      <td>21.425000</td>
      <td>62.224671</td>
    </tr>
    <tr>
      <th>IRS</th>
      <td>4936.0</td>
      <td>10.068860</td>
      <td>5.624760</td>
      <td>1.904546</td>
      <td>6.130128</td>
      <td>8.541985</td>
      <td>13.279294</td>
      <td>32.170000</td>
    </tr>
    <tr>
      <th>LOMA</th>
      <td>449.0</td>
      <td>14.069621</td>
      <td>5.356757</td>
      <td>5.400000</td>
      <td>10.340000</td>
      <td>11.740000</td>
      <td>21.120000</td>
      <td>25.020000</td>
    </tr>
    <tr>
      <th>MELI</th>
      <td>3025.0</td>
      <td>138.089838</td>
      <td>126.898120</td>
      <td>8.023763</td>
      <td>59.112264</td>
      <td>93.592940</td>
      <td>153.612638</td>
      <td>690.100000</td>
    </tr>
    <tr>
      <th>NTL</th>
      <td>4519.0</td>
      <td>13.146904</td>
      <td>8.402332</td>
      <td>0.392764</td>
      <td>6.546068</td>
      <td>12.756651</td>
      <td>18.681158</td>
      <td>51.700000</td>
    </tr>
    <tr>
      <th>PAM</th>
      <td>2479.0</td>
      <td>21.467967</td>
      <td>18.064011</td>
      <td>2.850000</td>
      <td>9.885292</td>
      <td>14.590000</td>
      <td>30.800000</td>
      <td>71.650000</td>
    </tr>
    <tr>
      <th>PZE</th>
      <td>4608.0</td>
      <td>5.865744</td>
      <td>2.463131</td>
      <td>1.515041</td>
      <td>4.362068</td>
      <td>5.365770</td>
      <td>6.720500</td>
      <td>14.550000</td>
    </tr>
    <tr>
      <th>SUPV</th>
      <td>816.0</td>
      <td>15.182065</td>
      <td>7.337212</td>
      <td>3.160000</td>
      <td>8.918750</td>
      <td>13.907507</td>
      <td>17.840770</td>
      <td>32.369630</td>
    </tr>
    <tr>
      <th>TEO</th>
      <td>4936.0</td>
      <td>12.194805</td>
      <td>6.370887</td>
      <td>0.380288</td>
      <td>7.642209</td>
      <td>12.427119</td>
      <td>16.013961</td>
      <td>35.963224</td>
    </tr>
    <tr>
      <th>TGS</th>
      <td>4936.0</td>
      <td>4.000758</td>
      <td>4.341288</td>
      <td>0.287635</td>
      <td>1.615702</td>
      <td>2.457407</td>
      <td>3.514175</td>
      <td>20.523048</td>
    </tr>
    <tr>
      <th>TS</th>
      <td>4195.0</td>
      <td>25.943267</td>
      <td>10.946160</td>
      <td>2.261653</td>
      <td>21.353160</td>
      <td>28.215679</td>
      <td>34.121053</td>
      <td>55.724628</td>
    </tr>
    <tr>
      <th>TX</th>
      <td>3408.0</td>
      <td>20.250514</td>
      <td>6.297409</td>
      <td>3.256623</td>
      <td>16.042294</td>
      <td>19.848379</td>
      <td>24.567725</td>
      <td>39.303918</td>
    </tr>
    <tr>
      <th>YPF</th>
      <td>4936.0</td>
      <td>21.578362</td>
      <td>9.696556</td>
      <td>3.164889</td>
      <td>14.031595</td>
      <td>21.594239</td>
      <td>29.665596</td>
      <td>47.309175</td>
    </tr>
  </tbody>
</table>
</div>



### Simple returns

Next we'll calculate the daily _simple returns_.  

$$R_t \equiv \frac{S_t - S_{t-1}}{S_{t-1}}  \%$$


```python
adrs_df['return'] = adrs_df.groupby('symbol')['adjClose'].pct_change() * 100
adrs_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>symbol</th>
      <th>close</th>
      <th>high</th>
      <th>low</th>
      <th>open</th>
      <th>volume</th>
      <th>adjClose</th>
      <th>adjHigh</th>
      <th>adjLow</th>
      <th>adjOpen</th>
      <th>adjVolume</th>
      <th>divCash</th>
      <th>splitFactor</th>
      <th>return</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2006-03-27</th>
      <td>BMA</td>
      <td>23.05</td>
      <td>23.05</td>
      <td>22.23</td>
      <td>22.89</td>
      <td>1065200</td>
      <td>15.524521</td>
      <td>15.524521</td>
      <td>14.972239</td>
      <td>15.416759</td>
      <td>1065200</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2006-03-28</th>
      <td>BMA</td>
      <td>22.38</td>
      <td>22.47</td>
      <td>21.90</td>
      <td>22.47</td>
      <td>1556100</td>
      <td>15.073266</td>
      <td>15.133883</td>
      <td>14.749979</td>
      <td>15.133883</td>
      <td>1556100</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>-2.906725</td>
    </tr>
    <tr>
      <th>2006-03-29</th>
      <td>BMA</td>
      <td>22.84</td>
      <td>23.14</td>
      <td>22.05</td>
      <td>22.10</td>
      <td>641300</td>
      <td>15.383083</td>
      <td>15.585138</td>
      <td>14.851006</td>
      <td>14.884682</td>
      <td>641300</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>2.055407</td>
    </tr>
    <tr>
      <th>2006-03-30</th>
      <td>BMA</td>
      <td>22.75</td>
      <td>23.10</td>
      <td>22.70</td>
      <td>23.00</td>
      <td>293600</td>
      <td>15.322467</td>
      <td>15.558197</td>
      <td>15.288791</td>
      <td>15.490846</td>
      <td>293600</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>-0.394046</td>
    </tr>
    <tr>
      <th>2006-03-31</th>
      <td>BMA</td>
      <td>22.93</td>
      <td>22.93</td>
      <td>22.35</td>
      <td>22.83</td>
      <td>113600</td>
      <td>15.443700</td>
      <td>15.443700</td>
      <td>15.053061</td>
      <td>15.376348</td>
      <td>113600</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.791209</td>
    </tr>
  </tbody>
</table>
</div>




```python
adrs_df.groupby('symbol')['return'].describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>count</th>
      <th>mean</th>
      <th>std</th>
      <th>min</th>
      <th>25%</th>
      <th>50%</th>
      <th>75%</th>
      <th>max</th>
    </tr>
    <tr>
      <th>symbol</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>BFR</th>
      <td>4935.0</td>
      <td>0.053087</td>
      <td>3.671496</td>
      <td>-55.850622</td>
      <td>-1.734230</td>
      <td>0.000000</td>
      <td>1.686544</td>
      <td>46.760563</td>
    </tr>
    <tr>
      <th>BMA</th>
      <td>3370.0</td>
      <td>0.083384</td>
      <td>3.282690</td>
      <td>-52.667364</td>
      <td>-1.489327</td>
      <td>0.000000</td>
      <td>1.647746</td>
      <td>27.008149</td>
    </tr>
    <tr>
      <th>CEPU</th>
      <td>385.0</td>
      <td>-0.265245</td>
      <td>4.306204</td>
      <td>-55.915179</td>
      <td>-1.913876</td>
      <td>-0.317460</td>
      <td>1.581028</td>
      <td>16.880093</td>
    </tr>
    <tr>
      <th>CRESY</th>
      <td>4935.0</td>
      <td>0.038327</td>
      <td>2.767597</td>
      <td>-38.090452</td>
      <td>-1.250890</td>
      <td>0.000000</td>
      <td>1.180099</td>
      <td>27.118644</td>
    </tr>
    <tr>
      <th>EDN</th>
      <td>3098.0</td>
      <td>0.051126</td>
      <td>3.888776</td>
      <td>-58.983957</td>
      <td>-1.690714</td>
      <td>-0.031217</td>
      <td>1.629187</td>
      <td>27.551020</td>
    </tr>
    <tr>
      <th>GGAL</th>
      <td>4794.0</td>
      <td>0.094611</td>
      <td>4.627147</td>
      <td>-56.117370</td>
      <td>-1.626710</td>
      <td>0.000000</td>
      <td>1.693722</td>
      <td>153.623188</td>
    </tr>
    <tr>
      <th>IRCP</th>
      <td>3970.0</td>
      <td>0.142312</td>
      <td>4.226301</td>
      <td>-32.424983</td>
      <td>-0.681957</td>
      <td>0.000000</td>
      <td>0.849814</td>
      <td>36.986301</td>
    </tr>
    <tr>
      <th>IRS</th>
      <td>4935.0</td>
      <td>0.015710</td>
      <td>2.675223</td>
      <td>-38.287402</td>
      <td>-1.250000</td>
      <td>0.000000</td>
      <td>1.214575</td>
      <td>18.083573</td>
    </tr>
    <tr>
      <th>LOMA</th>
      <td>448.0</td>
      <td>-0.166143</td>
      <td>4.533969</td>
      <td>-57.298137</td>
      <td>-1.875441</td>
      <td>-0.087351</td>
      <td>1.505056</td>
      <td>22.650602</td>
    </tr>
    <tr>
      <th>MELI</th>
      <td>3024.0</td>
      <td>0.165014</td>
      <td>3.566247</td>
      <td>-21.198668</td>
      <td>-1.400264</td>
      <td>0.083916</td>
      <td>1.589953</td>
      <td>36.000000</td>
    </tr>
    <tr>
      <th>NTL</th>
      <td>4518.0</td>
      <td>0.082807</td>
      <td>3.342394</td>
      <td>-46.188341</td>
      <td>-1.315789</td>
      <td>0.000000</td>
      <td>1.365299</td>
      <td>30.000000</td>
    </tr>
    <tr>
      <th>PAM</th>
      <td>2478.0</td>
      <td>0.060250</td>
      <td>2.964323</td>
      <td>-53.815490</td>
      <td>-1.415248</td>
      <td>0.000000</td>
      <td>1.411089</td>
      <td>16.941990</td>
    </tr>
    <tr>
      <th>PZE</th>
      <td>4607.0</td>
      <td>0.066024</td>
      <td>3.908461</td>
      <td>-19.221411</td>
      <td>-1.457769</td>
      <td>0.000000</td>
      <td>1.415805</td>
      <td>179.843750</td>
    </tr>
    <tr>
      <th>SUPV</th>
      <td>815.0</td>
      <td>-0.025345</td>
      <td>4.183604</td>
      <td>-58.746736</td>
      <td>-1.407739</td>
      <td>0.000000</td>
      <td>1.494714</td>
      <td>28.330206</td>
    </tr>
    <tr>
      <th>TEO</th>
      <td>4935.0</td>
      <td>0.035329</td>
      <td>3.079372</td>
      <td>-33.375796</td>
      <td>-1.419974</td>
      <td>0.000000</td>
      <td>1.450779</td>
      <td>23.076923</td>
    </tr>
    <tr>
      <th>TGS</th>
      <td>4935.0</td>
      <td>0.077615</td>
      <td>3.385825</td>
      <td>-48.035488</td>
      <td>-1.494490</td>
      <td>0.000000</td>
      <td>1.615534</td>
      <td>25.203252</td>
    </tr>
    <tr>
      <th>TS</th>
      <td>4194.0</td>
      <td>0.084939</td>
      <td>2.537497</td>
      <td>-21.309735</td>
      <td>-1.177830</td>
      <td>0.113344</td>
      <td>1.351878</td>
      <td>21.576763</td>
    </tr>
    <tr>
      <th>TX</th>
      <td>3407.0</td>
      <td>0.047116</td>
      <td>3.028683</td>
      <td>-19.678519</td>
      <td>-1.351580</td>
      <td>0.036819</td>
      <td>1.413508</td>
      <td>49.096099</td>
    </tr>
    <tr>
      <th>YPF</th>
      <td>4935.0</td>
      <td>0.033014</td>
      <td>2.563941</td>
      <td>-34.052758</td>
      <td>-1.121233</td>
      <td>0.000000</td>
      <td>1.123280</td>
      <td>37.254597</td>
    </tr>
  </tbody>
</table>
</div>



Let's plot a histogram of the daily returns for each symbol.


```python
g = sns.FacetGrid(adrs_df, col='symbol', col_wrap=5, hue='symbol', sharey=False, sharex=False)
g.map(plt.hist, 'return', bins=25, density=True)

g.fig.suptitle('Histogram of daily returns', size=16)
g.fig.subplots_adjust(top=.93);
```


![png](img/0.6-troubled-markets-and-volatility_23_0.png)


We see most returns cluster around 0, with a few outliers. Since we are interested particularly in the outliers, to see their quantity and magnitude, we can visualize them using a [boxenplot](https://vita.had.co.nz/papers/letter-value-plot.html).


```python
# Workaround to suppress matplotlib errors
from matplotlib.axes._axes import _log as matplotlib_axes_logger
matplotlib_axes_logger.setLevel('ERROR')
```


```python
sns.boxenplot(y='symbol', x='return', data=adrs_df, scale='area',
              orient='h').set_title('Daily returns per symbol', size=16);
```


![png](img/0.6-troubled-markets-and-volatility_26_0.png)


We can filter the days with 30% or larger movement in prices (either up or down).


```python
large_movements = adrs_df.loc[adrs_df['return'].abs() >= 30]
sns.scatterplot(x=large_movements.index,
                y='return',
                hue='symbol',
                data=large_movements).set_title(
                    'Large daily returns (+/- 30%)', size=16);
```


![png](img/0.6-troubled-markets-and-volatility_28_0.png)


Now if we remove outliers, say discard days where return was higher than 10% or lower than -10%:


```python
g = sns.FacetGrid(adrs_df, col='symbol', col_wrap=5, hue='symbol', sharex=False)
g.map(plt.hist, 'return', bins=25, density=True, range=(-10,10))

g.fig.suptitle('Histogram of daily returns (between -10% / +10%)', size=16)
g.fig.subplots_adjust(top=.93);
```


![png](img/0.6-troubled-markets-and-volatility_30_0.png)


### Log returns

In finance, it is common to look at the _log returns_ of an asset. They are defined as follows:

$$r_t \equiv \ln{\frac{S_t}{S_{t-1}}} = \ln{S_t} - \ln{S_{t-1}}$$

There is an equivalence between simple and log returns:

\begin{align}
r_t &= \ln{(R_t + 1)} \\
R_t &= \exp{r_t} - 1
\end{align}

You can find further information on the two return types in this [post](https://www.portfolioprobe.com/2010/10/04/a-tale-of-two-returns/).

Stock prices are assumed to follow a [log-normal](https://en.wikipedia.org/wiki/Log-normal_distribution) distribution, hence we should expect log returns to be distributed [normally](https://en.wikipedia.org/wiki/Normal_distribution).

$$ln(S_T)\sim N\big[ln(S_0)+(\mu-\frac{\sigma^2}{2})T,\;\sigma^2T\big] \\
ln(\frac{S_T}{S_0})\sim N\big[(\mu-\frac{\sigma^2}{2})T, \;\sigma^2T\big]$$

Where $S_T$ is the price of the underlying at time $T$.  
For a more detailed discussion on the assumptions of the [Black-Scholes-Merton](https://en.wikipedia.org/wiki/Black–Scholes_model) model, see chapter 15 of _Options, Futures and Other Derivatives_ (9th Ed) by John Hull.  
You can read more on the distribution of prices and returns [here](https://www.investopedia.com/articles/investing/102014/lognormal-and-normal-distribution.asp).


```python
adrs_df['log_return'] = np.log(adrs_df['return'] / 100 + 1.)
```

Now we can calculate the [volatility](https://en.wikipedia.org/wiki/Volatility_(finance)) $\sigma$ for each symbol, defined as the [standard deviation](https://en.wikipedia.org/wiki/Standard_deviation) of log returns.  
As a comparison, we'll add the daily volatility (from 2000 to 2019) for four of the so called [blue chip stocks](https://www.investopedia.com/terms/b/bluechipstock.asp), Coca-Cola (\\$KO), Goldman Sachs (\\$GS), IBM (\\$IBM) and Walmart (\\$WMT).


```python
blue_chip = pd.read_csv(os.path.join(data_dir, 'blue_chip.csv'),
                        index_col=['date', 'symbol'],
                        parse_dates=['date'])
blue_chip['log_return'] = blue_chip.groupby('symbol')['adjClose'].apply(
    lambda x: np.log(x) - np.log(x.shift(1)))
```


```python
adr_volatility = adrs_df.groupby('symbol')['log_return'].std()
adr_volatility = adr_volatility.append(blue_chip.groupby('symbol')['log_return'].std())

sns.barplot(x=adr_volatility.index, y=adr_volatility.values).set_title(
    'Daily volatility $\sigma_{daily}$ for each symbol (std of log returns)',
    size=16);
```


![png](img/0.6-troubled-markets-and-volatility_37_0.png)


We can see that Argentine stocks show much higher volatility than the blue chip stocks.

Let's plot the mean yearly returns for each symbol. Again, we'll add the mean daily return of the US blue chips.


```python
yearly_rets = np.exp(
    adrs_df.groupby('symbol')['log_return'].resample('Y',
                                                     label='right').sum()) - 1
yearly_rets = yearly_rets.reset_index()
yearly_rets['return %'] = yearly_rets['log_return'] * 100

blue_chip.reset_index(level='symbol', inplace=True)
blue_chip_rets = np.exp(
    blue_chip.groupby('symbol')['log_return'].resample(
        'Y', label='right').sum()) - 1
blue_chip_rets = blue_chip_rets.reset_index()
blue_chip_rets['return %'] = blue_chip_rets['log_return'] * 100
```


```python
mean_rets = yearly_rets.groupby('symbol')['return %'].mean()
mean_rets = mean_rets.append(blue_chip_rets.groupby('symbol')['return %'].mean())
sns.barplot(x=mean_rets.index, y=mean_rets.values).set_title(
    "Mean yearly returns of Argentina's ADRs", size=16);
```


![png](img/0.6-troubled-markets-and-volatility_41_0.png)


As expected, besides increased volatility, Argentine stocks, for the most part, exhibit higher yearly returns than the chosen US stocks.

### A closer look at outliers

Let's plot the returns that are at least $3\sigma$ away from the mean. If log returns were truly distributed normally, then we should expect this group to represent only $0.3\%$ of the data, while the remaining $99.7\%$ should lie in the interval $(\mu_r - 3\sigma_r, \mu_r + 3\sigma_r)$.


```python
def outlier_filter(symbol_df):
    symbol = symbol_df['symbol'].iloc[0]
    return symbol_df.loc[(symbol_df['log_return'] -
                          symbol_df['log_return'].mean()).abs() >= 3 *
                         adr_volatility[symbol]]

outliers = adrs_df.groupby('symbol').apply(outlier_filter).reset_index(
    level=0, drop=True)
```


```python
sns.scatterplot(x=outliers.index, y='log_return', hue='symbol',
                data=outliers).set_title('$3\sigma$ outlier daily returns',
                                         size=16);
```


![png](img/0.6-troubled-markets-and-volatility_46_0.png)


We see a large number of outlier return days. To put that in perspective, let's calculate the proportion of outlier returns for each symbol in the data, that is the number of days where $3\sigma$ returns where observed over the total number of observations.


```python
outlier_count = outliers.groupby('symbol')['log_return'].count()
ret_count = adrs_df.groupby('symbol')['log_return'].count()

outlier_pct = 100 * outlier_count / ret_count
ax = sns.barplot(x=outlier_pct.index, y=outlier_pct.values)
ax.axhline(0.3, alpha=0.6, linestyle='--', color='r', label='expected % of outliers')
ax.legend()
ax.set_title(
    'Outlier proportion (outlier daily return count / total daily returns)',
    size=16);
```


![png](img/0.6-troubled-markets-and-volatility_48_0.png)


We see many more outliers than the expected $0.3\%$. For example, \$MELI has almost 7 times more outlier return days than expected if we assumed normal log returns.

Finally, we'll look at the cumulative log returns over time.


```python
pivoted = adrs_df.pivot(columns='symbol', values='log_return')
pivoted.cumsum().apply(np.exp).plot(title='Cumulative log returns', colormap='Set1');
```


![png](img/0.6-troubled-markets-and-volatility_51_0.png)


If you had invested in \\$MELI's IPO in 2007, you've had have over 25 times your initial investment by August 2019. You would also have to stomach losing close to 60% at the end of 2008.

### ADR options and the volatility smile

We've observed ADRs experienced a very high volatility, and this leads us to question wether the prices of financial derivatives such as options were affected.

We will explore how volatility in the prices of the underlying assests impacted option prices during the crash.

To this end, we will examine the options end-of-day data for the ADRs. [Options](https://www.investopedia.com/terms/o/option.asp) are derivative contracts based on an underlying asset such as stocks. They offer the buyer the opportunity to buy or sell the underlying asset at a given price (or _strike price_ ). You can find more information on options in [this notebook](../intro-finance.ipynb).




```python
adr_options = pd.read_csv(os.path.join(data_dir, 'adr_options.csv'),
                          index_col='quotedate',
                          parse_dates=['quotedate', 'expiration'])
adr_options.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>underlying</th>
      <th>underlying_last</th>
      <th>exchange</th>
      <th>optionroot</th>
      <th>type</th>
      <th>expiration</th>
      <th>strike</th>
      <th>last</th>
      <th>net</th>
      <th>bid</th>
      <th>ask</th>
      <th>volume</th>
      <th>openinterest</th>
      <th>impliedvol</th>
      <th>delta</th>
      <th>gamma</th>
    </tr>
    <tr>
      <th>quotedate</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-07-03</th>
      <td>TEO</td>
      <td>17.79</td>
      <td>CBOE</td>
      <td>TEO190719C00002500</td>
      <td>call</td>
      <td>2019-07-19</td>
      <td>2.5</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>13.0</td>
      <td>17.8</td>
      <td>0</td>
      <td>0</td>
      <td>0.0200</td>
      <td>1.0000</td>
      <td>0.0000</td>
    </tr>
    <tr>
      <th>2019-07-03</th>
      <td>TEO</td>
      <td>17.79</td>
      <td>CBOE</td>
      <td>TEO190719C00005000</td>
      <td>call</td>
      <td>2019-07-19</td>
      <td>5.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>10.5</td>
      <td>15.2</td>
      <td>0</td>
      <td>0</td>
      <td>6.3229</td>
      <td>0.9446</td>
      <td>0.0045</td>
    </tr>
    <tr>
      <th>2019-07-03</th>
      <td>TEO</td>
      <td>17.79</td>
      <td>CBOE</td>
      <td>TEO190719C00007500</td>
      <td>call</td>
      <td>2019-07-19</td>
      <td>7.5</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>8.0</td>
      <td>12.8</td>
      <td>0</td>
      <td>0</td>
      <td>3.5717</td>
      <td>0.9336</td>
      <td>0.0093</td>
    </tr>
    <tr>
      <th>2019-07-03</th>
      <td>TEO</td>
      <td>17.79</td>
      <td>CBOE</td>
      <td>TEO190719C00010000</td>
      <td>call</td>
      <td>2019-07-19</td>
      <td>10.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>5.5</td>
      <td>10.2</td>
      <td>0</td>
      <td>0</td>
      <td>2.0354</td>
      <td>0.9375</td>
      <td>0.0156</td>
    </tr>
    <tr>
      <th>2019-07-03</th>
      <td>TEO</td>
      <td>17.79</td>
      <td>CBOE</td>
      <td>TEO190719C00012500</td>
      <td>call</td>
      <td>2019-07-19</td>
      <td>12.5</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>7.8</td>
      <td>0</td>
      <td>199</td>
      <td>1.2856</td>
      <td>0.9215</td>
      <td>0.0297</td>
    </tr>
  </tbody>
</table>
</div>



The options data is also indexed by date. These are the most important columns:
- `underlying`: The ticker of the underlying asset.
- `underlying_last`: The last quoted price of the underlying asset.
- `optionroot`: The name of the contract.
- `type`: Contract type (_put_ or _call_)
- `strike`: The price at which owner can execute (buy/sell underlying).
- `expiration`: Date of expiration of the option.
- `bid`: The price at which investor can _sell_ this contract.
- `ask`: The price at which investor can _buy_ this contract.
- `openinterest`: The total number of contract outstanding.
- `impliedvol`: Volatility of the underlying as implied by the option price (according to BSM model)

Let's plot the [volatility smile](https://www.investopedia.com/terms/v/volatilitysmile.asp) for each symbol at 2019-08-09, the Friday before the primaries.  
The volatility smile plots the [implied volatility](https://www.investopedia.com/terms/i/iv.asp) (IV, a measure of the volatility of an underlying security as _implied_ by the option prices) at the different strike levels.  
We'll plot the IV for puts and calls for each symbol. The dashed line represents the spot price.


```python
friday_9th = adr_options.loc['2019-08-9']

# Keep puts with K <= spot and calls with K > spot
friday_9th = friday_9th.query(
    '((type == "put") & (strike <= underlying_last)) | ((type == "call") & (strike > underlying_last))'
)

g = sns.relplot(x='strike', y='impliedvol', col='underlying',
            facet_kws=dict(sharey=False, sharex=False), col_wrap=3,
            kind='line', data=friday_9th, ci=None, color='coral')

for ax, symbol in zip(g.axes, g.col_names):
    spot_price = friday_9th.loc[friday_9th['underlying'] == symbol, 'underlying_last'].iloc[0]
    ax.axvline(spot_price, alpha=0.4, linestyle='--')
    
g.fig.suptitle('Volatility smiles - August 9th 2019', size=16)
g.fig.subplots_adjust(top=.94);
```


![png](img/0.6-troubled-markets-and-volatility_58_0.png)


We see that as options move more [at the money](https://www.investopedia.com/terms/a/atthemoney.asp) (ATM) their implied volatility drops. In contrast, options that are further [out of the money](https://www.investopedia.com/terms/o/outofthemoney.asp) (OTM) or in the money (ITM) have higher IVs.

Now let's try the same plot for the following Monday (2019-08-12). That day, the [MERVAL](https://en.wikipedia.org/wiki/MERVAL) (an index that tracks the biggest companies listed in the Buenos Aires Stock Exchange) crashed and lost close to 50% of its USD value.


```python
black_monday = adr_options.loc['2019-08-12']

# Keep puts with K <= spot and calls with K > spot
black_monday = black_monday.query(
    '((type == "put") & (strike <= underlying_last)) | ((type == "call") & (strike > underlying_last))'
)

g = sns.relplot(x='strike', y='impliedvol', col='underlying',
            facet_kws=dict(sharey=False, sharex=False), col_wrap=3,
            kind='line', data=black_monday, ci=None, color='coral')

for ax, symbol in zip(g.axes, g.col_names):
    spot_price = black_monday.loc[black_monday['underlying'] == symbol, 'underlying_last'].iloc[0]
    ax.axvline(spot_price, alpha=0.4, linestyle='--')
    
g.fig.suptitle('Volatility smiles - August 12th 2019', size=16)
g.fig.subplots_adjust(top=.94);
```


![png](img/0.6-troubled-markets-and-volatility_61_0.png)


As stock prices droped sharply, we find less put contracts were being offered. Again, we see IV getting higher as the strike priced moves away from the spot price.

### Option price evolution

Next, we'll analyze how option prices changed during the month of August, 2019.
Let's find the 10 most actively traded options (those with the highest open interest) for each symbol at the start of the month.


```python
august_options = adr_options.loc['2019-08']
```


```python
def filter_active(symbol_df, option_type='call'):
    return symbol_df.loc[symbol_df['type'] == option_type].nlargest(
        n=10, columns='openinterest')

month_start_date = august_options.index.min()
first_trading_day = august_options.loc[month_start_date]
most_active_calls = first_trading_day.groupby('underlying').apply(
    filter_active).reset_index(level=0, drop=True)
most_active_puts = first_trading_day.groupby('underlying').apply(
    lambda df: filter_active(df, 'put')).reset_index(level=0, drop=True)
```


```python
call_contracts = most_active_calls['optionroot']
put_contracts = most_active_puts['optionroot']
```


```python
august_active_calls = august_options.loc[august_options['optionroot'].isin(call_contracts)]
august_active_puts = august_options.loc[august_options['optionroot'].isin(put_contracts)]

august_active_calls['day'] = august_active_calls.index.strftime('%d')
august_active_puts['day'] = august_active_puts.index.strftime('%d')
```

#### August 2019

We'll plot the evolution of the ask price for the actively traded calls through August 2019.


```python
g = sns.relplot(x='day', y='ask', col='underlying', hue='optionroot',
            facet_kws=dict(sharey=False, sharex=False), col_wrap=3, legend=None,
            kind='line', data=august_active_calls, ci=None)

g.fig.suptitle('Ask price for most actively traded calls in August 2019', size=16)
g.fig.subplots_adjust(top=0.94);
```


![png](img/0.6-troubled-markets-and-volatility_71_0.png)


Note that the \\$BFR plot shows all calls with an `ask` price of 0.0. In June 2019, Banco Frances SA [announced](https://finance.yahoo.com/news/bbva-banco-franc-change-ticker-165400264.html) it would  change its ticker symbol from \\$BFR to \\$BBAR. We will update the plots when we get the correct data for the missing months.


```python
g = sns.relplot(x='day', y='ask', col='underlying', hue='optionroot',
            facet_kws=dict(sharey=False, sharex=False), col_wrap=3, legend=None,
            kind='line', data=august_active_puts, ci=None)

g.fig.suptitle('Ask price for most actively traded puts in August 2019', size=16)
g.fig.subplots_adjust(top=0.94);
```


![png](img/0.6-troubled-markets-and-volatility_73_0.png)


This plots reveal a huge drop in prices for the calls, and, conversely, a large increase in the price of puts, between Friday 9th and Monday 12th.

#### June 2019

As a comparison, let's try plotting the option prices for June 2019, a more uneventful month for the Argentine market.


```python
june_options = adr_options.loc['2019-06']
```


```python
month_start_date = june_options.index.min()
first_trading_day = june_options.loc[month_start_date]
most_active_calls = first_trading_day.groupby('underlying').apply(
    filter_active).reset_index(level=0, drop=True)
most_active_puts = first_trading_day.groupby('underlying').apply(
    lambda df: filter_active(df, 'put')).reset_index(level=0, drop=True)
```


```python
call_contracts = most_active_calls['optionroot']
put_contracts = most_active_puts['optionroot']
```


```python
june_active_calls = june_options.loc[june_options['optionroot'].isin(call_contracts)]
june_active_puts = june_options.loc[june_options['optionroot'].isin(put_contracts)]

june_active_calls['day'] = june_active_calls.index.strftime('%d')
june_active_puts['day'] = june_active_puts.index.strftime('%d')
```


```python
g = sns.relplot(x='day', y='ask', col='underlying', hue='optionroot',
            facet_kws=dict(sharey=False, sharex=False), col_wrap=3, legend=None,
            kind='line', data=june_active_calls, ci=None)

g.fig.suptitle('Ask price for most actively traded calls in June 2019', size=16)
g.fig.subplots_adjust(top=0.94);
```


![png](img/0.6-troubled-markets-and-volatility_81_0.png)


Next we'll have a look the the actively traded puts for June 2019.


```python
g = sns.relplot(x='day', y='ask', col='underlying', hue='optionroot',
            facet_kws=dict(sharey=False, sharex=False), col_wrap=3, legend=None,
            kind='line', data=june_active_puts, ci=None)

g.fig.suptitle('Ask price for most actively traded puts in June 2019', size=16)
g.fig.subplots_adjust(top=0.94);
```


![png](img/0.6-troubled-markets-and-volatility_83_0.png)


#### October 2015

Let's have a look at the options data from October, November and December 2015.  
During those months, the Argentine elections took place, which marked the beginning of a bull market. In the following four years, the MERVAL index increased four-fold its value in Pesos.


```python
october_2015_options = pd.read_csv(os.path.join(data_dir, 'adr_options_October_2015.csv'),
                                   index_col='quotedate',
                                   parse_dates=['quotedate', 'expiration'])
```


```python
month_start_date = october_2015_options.index.min()
first_trading_day = october_2015_options.loc[month_start_date]
most_active_calls = first_trading_day.groupby('underlying').apply(
    filter_active).reset_index(level=0, drop=True)
most_active_puts = first_trading_day.groupby('underlying').apply(
    lambda df: filter_active(df, 'put')).reset_index(level=0, drop=True)
```


```python
call_contracts = most_active_calls['optionroot']
put_contracts = most_active_puts['optionroot']
```


```python
october2015_active_calls = october_2015_options.loc[october_2015_options['optionroot'].isin(call_contracts)]
october2015_active_puts = october_2015_options.loc[october_2015_options['optionroot'].isin(put_contracts)]

october2015_active_calls['day'] = october2015_active_calls.index.strftime('%d')
october2015_active_puts['day'] = october2015_active_puts.index.strftime('%d')
```


```python
g = sns.relplot(x='day', y='ask', col='underlying', hue='optionroot',
            facet_kws=dict(sharey=False, sharex=False), col_wrap=3, legend=None,
            kind='line', data=october2015_active_calls, ci=None)

g.fig.suptitle('Ask price for most actively traded calls in October 2015', size=16)
g.fig.subplots_adjust(top=0.94);
```


![png](img/0.6-troubled-markets-and-volatility_90_0.png)


Now let's plot the actively traded puts for October 2015


```python
g = sns.relplot(x='day', y='ask', col='underlying', hue='optionroot',
            facet_kws=dict(sharey=False, sharex=False), col_wrap=3, legend=None,
            kind='line', data=october2015_active_puts, ci=None)

g.fig.suptitle('Ask price for most actively traded puts in October 2015', size=16)
g.fig.subplots_adjust(top=0.94);
```


![png](img/0.6-troubled-markets-and-volatility_92_0.png)


#### November 2015


```python
november_2015_options = pd.read_csv(os.path.join(data_dir, 'adr_options_november_2015.csv'),
                                   index_col='quotedate',
                                   parse_dates=['quotedate', 'expiration'])
```


```python
month_start_date = november_2015_options.index.min()
first_trading_day = november_2015_options.loc[month_start_date]
most_active_calls = first_trading_day.groupby('underlying').apply(
    filter_active).reset_index(level=0, drop=True)
most_active_puts = first_trading_day.groupby('underlying').apply(
    lambda df: filter_active(df, 'put')).reset_index(level=0, drop=True)
```


```python
call_contracts = most_active_calls['optionroot']
put_contracts = most_active_puts['optionroot']
```


```python
november2015_active_calls = november_2015_options.loc[november_2015_options['optionroot'].isin(call_contracts)]
november2015_active_puts = november_2015_options.loc[november_2015_options['optionroot'].isin(put_contracts)]

november2015_active_calls['day'] = november2015_active_calls.index.strftime('%d')
november2015_active_puts['day'] = november2015_active_puts.index.strftime('%d')
```


```python
g = sns.relplot(x='day', y='ask', col='underlying', hue='optionroot',
            facet_kws=dict(sharey=False, sharex=False), col_wrap=3, legend=None,
            kind='line', data=october2015_active_calls, ci=None)

g.fig.suptitle('Ask price for most actively traded calls in November 2015', size=16)
g.fig.subplots_adjust(top=0.94);
```


![png](img/0.6-troubled-markets-and-volatility_98_0.png)



```python
g = sns.relplot(x='day', y='ask', col='underlying', hue='optionroot',
            facet_kws=dict(sharey=False, sharex=False), col_wrap=3, legend=None,
            kind='line', data=october2015_active_puts, ci=None)

g.fig.suptitle('Ask price for most actively traded puts in November 2015', size=16)
g.fig.subplots_adjust(top=0.94);
```


![png](img/0.6-troubled-markets-and-volatility_99_0.png)


#### December 2015


```python
december_2015_options = pd.read_csv(os.path.join(data_dir, 'adr_options_December_2015.csv'),
                                   index_col='quotedate',
                                   parse_dates=['quotedate', 'expiration'])
```


```python
month_start_date = december_2015_options.index.min()
first_trading_day = december_2015_options.loc[month_start_date]
most_active_calls = first_trading_day.groupby('underlying').apply(
    filter_active).reset_index(level=0, drop=True)
most_active_puts = first_trading_day.groupby('underlying').apply(
    lambda df: filter_active(df, 'put')).reset_index(level=0, drop=True)
```


```python
call_contracts = most_active_calls['optionroot']
put_contracts = most_active_puts['optionroot']
```


```python
december2015_active_calls = december_2015_options.loc[december_2015_options['optionroot'].isin(call_contracts)]
december2015_active_puts = december_2015_options.loc[december_2015_options['optionroot'].isin(put_contracts)]

december2015_active_calls['day'] = december2015_active_calls.index.strftime('%d')
december2015_active_puts['day'] = december2015_active_puts.index.strftime('%d')
```


```python
g = sns.relplot(x='day', y='ask', col='underlying', hue='optionroot',
            facet_kws=dict(sharey=False, sharex=False), col_wrap=3, legend=None,
            kind='line', data=october2015_active_calls, ci=None)

g.fig.suptitle('Ask price for most actively traded calls in December 2015', size=16)
g.fig.subplots_adjust(top=0.94);
```


![png](img/0.6-troubled-markets-and-volatility_105_0.png)



```python
g = sns.relplot(x='day', y='ask', col='underlying', hue='optionroot',
            facet_kws=dict(sharey=False, sharex=False), col_wrap=3, legend=None,
            kind='line', data=october2015_active_puts, ci=None)

g.fig.suptitle('Ask price for most actively traded puts in December 2015', size=16)
g.fig.subplots_adjust(top=0.94);
```


![png](img/0.6-troubled-markets-and-volatility_106_0.png)


#### January 2008

We'll examine the Argentine ADR options data for January 2008, the beginning of the US mortgage crisis, which had global effects. We only have data for 3 companies: \\$MELI, \\$TS and \\$TX


```python
january_2008_options = pd.read_csv(os.path.join(data_dir, 'adr_options_january_2008.csv'),
                                   index_col='quotedate',
                                   parse_dates=['quotedate', 'expiration'])
```


```python
month_start_date = january_2008_options.index.min()
first_trading_day = january_2008_options.loc[month_start_date]
most_active_calls = first_trading_day.groupby('underlying').apply(
    filter_active).reset_index(level=0, drop=True)
most_active_puts = first_trading_day.groupby('underlying').apply(
    lambda df: filter_active(df, 'put')).reset_index(level=0, drop=True)
```


```python
call_contracts = most_active_calls['optionroot']
put_contracts = most_active_puts['optionroot']
```


```python
january2008_active_calls = january_2008_options.loc[january_2008_options['optionroot'].isin(call_contracts)]
january2008_active_puts = january_2008_options.loc[january_2008_options['optionroot'].isin(put_contracts)]

january2008_active_calls['day'] = january2008_active_calls.index.strftime('%d')
january2008_active_puts['day'] = january2008_active_puts.index.strftime('%d')
```


```python
g = sns.relplot(x='day', y='ask', col='underlying', hue='optionroot',
            facet_kws=dict(sharey=False, sharex=False), col_wrap=3, legend=None,
            kind='line', data=january2008_active_calls, ci=None)

g.fig.suptitle('Ask price for most actively traded calls in January 2008', size=16)
g.fig.subplots_adjust(top=0.88);
```


![png](img/0.6-troubled-markets-and-volatility_113_0.png)



```python
g = sns.relplot(x='day', y='ask', col='underlying', hue='optionroot',
            facet_kws=dict(sharey=False, sharex=False), col_wrap=3, legend=None,
            kind='line', data=january2008_active_puts, ci=None)

g.fig.suptitle('Ask price for most actively traded puts in January 2008', size=16)
g.fig.subplots_adjust(top=0.88);
```


![png](img/0.6-troubled-markets-and-volatility_114_0.png)


As the market went bearish, calls decreased in value and puts became more expensive.

## Final notes

Countries such as Argentina exhibit high [political beta](https://www.fa-mag.com/news/political-beta-44530.html): stocks show extreme sensitivity to political events. The MERVAL index nearly quadrupled its value in Pesos since December 2015, only to drop by 40% in a single day in August 2019.  
Investors tend to exacerbate bull runs, discounting future growth in the current stock prices. At the prospect of regulatory changes and political turnover, they panic sell and seek less risky assets. There remains to be seen whether savvy traders can exploit both the overconfident bulls and the panicking bears, buying volatility from the former to sell it at a profit to the latter.
