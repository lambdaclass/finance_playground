# Troubled markets and volatility
### _Challenging financial models through an exploration on the crash of Argentina's ADRs_

</br>

[American Depositary Receipts](https://www.investopedia.com/terms/a/adr.asp) (ADRs) are financial instruments that allow US investors to purchase stocks in foreign companies. Argentina has a number of companies listed in US exchanges through ADRs.  

In this notebook, we will explore the performance of these ADRs with a focus on the period from January to August 2019, where political uncertainty sent markets into turmoil: the country’s Merval stock index fell 48% in dollar terms in a single day, the second-largest one-day drop in any of the 94 markets tracked by Bloomberg since 1950<sup>[1]</sup>, causing a 20% devaluation of the Argentine peso and a sharp drop in bond prices.  

We will be looking at the end-of-day data of the Argentine ADRs, and their corresponding put and call options, to examine whether the daily log returns of stocks are distributed normally, a conclusion that follows from the standard model due to [Bachelier](en.wikipedia.org/wiki/Louis_Bachelier).

[1]: https://www.ft.com/content/29764546-c821-11e9-a1f4-3669401ba76f

</br>

## Exploration


We begin our exploration of the end-of-day (EOD) data for Argentina's ADRs.

</br>
<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;border-color:#93a1a1;}
.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#93a1a1;color:#002b36;background-color:#fdf6e3;}
.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#93a1a1;color:#fdf6e3;background-color:#657b83;}
.tg .tg-ttiq{background-color:#002b36;color:#fffff8;border-color:#fffff8;text-align:center;vertical-align:top}
.tg .tg-664r{background-color:#fffff8;border-color:inherit;text-align:center;vertical-align:top}
.tg .tg-lkkz{background-color:#fffff8;border-color:#000000;text-align:center;vertical-align:top}
.tg .tg-zlpi{background-color:#fffff8;border-color:#002b36;text-align:center;vertical-align:top}
</style>
<table class="tg" style="undefined;table-layout: fixed; width: 896px">
<colgroup>
<col style="width: 83px">
<col style="width: 58px">
<col style="width: 47px">
<col style="width: 46px">
<col style="width: 52px">
<col style="width: 46px">
<col style="width: 65px">
<col style="width: 65px">
<col style="width: 62px">
<col style="width: 76px">
<col style="width: 71px">
<col style="width: 81px">
<col style="width: 64px">
<col style="width: 80px">
</colgroup>
  <tr>
    <th class="tg-ttiq">Date<br></th>
    <th class="tg-ttiq">Symbol</th>
    <th class="tg-ttiq">Close<br></th>
    <th class="tg-ttiq">High<br></th>
    <th class="tg-ttiq">Low<br></th>
    <th class="tg-ttiq">Open<br></th>
    <th class="tg-ttiq">Volume<br></th>
    <th class="tg-ttiq">adjClose</th>
    <th class="tg-ttiq">adjHigh</th>
    <th class="tg-ttiq">adjLow</th>
    <th class="tg-ttiq">adjOpen</th>
    <th class="tg-ttiq">adjVolume</th>
    <th class="tg-ttiq">divCash</th>
    <th class="tg-ttiq">splitFactor</th>
  </tr>
  <tr>
    <td class="tg-ttiq">2006-03-27</td>
    <td class="tg-664r">BMA</td>
    <td class="tg-664r">$23.05$</td>
    <td class="tg-664r">$23.05$<br></td>
    <td class="tg-664r">$22.23$</td>
    <td class="tg-lkkz">$22.89$<br></td>
    <td class="tg-lkkz">$1065200$<br></td>
    <td class="tg-lkkz">$15.52$</td>
    <td class="tg-lkkz">$15.52$</td>
    <td class="tg-lkkz">$14.08$</td>
    <td class="tg-zlpi">$15.42$</td>
    <td class="tg-zlpi">$1065200$</td>
    <td class="tg-zlpi">$0$</td>
    <td class="tg-zlpi">$1$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">2006-03-28</td>
    <td class="tg-lkkz">BMA</td>
    <td class="tg-lkkz">$22.38$</td>
    <td class="tg-lkkz">$22.47$</td>
    <td class="tg-lkkz">$21.90$</td>
    <td class="tg-lkkz">$22.47$</td>
    <td class="tg-lkkz">$1556100$</td>
    <td class="tg-lkkz">$15.07$</td>
    <td class="tg-lkkz">$15.13$</td>
    <td class="tg-lkkz">$14.75$</td>
    <td class="tg-zlpi">$15.13$</td>
    <td class="tg-zlpi">$1556100$</td>
    <td class="tg-zlpi">$0$</td>
    <td class="tg-zlpi">$1$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">2006-03-29</td>
    <td class="tg-lkkz">BMA</td>
    <td class="tg-lkkz">$22.84$</td>
    <td class="tg-lkkz">$23.14$</td>
    <td class="tg-lkkz">$22.05$</td>
    <td class="tg-lkkz">$22.10$</td>
    <td class="tg-lkkz">$641300$</td>
    <td class="tg-lkkz">$15.38$</td>
    <td class="tg-lkkz">$15.59$</td>
    <td class="tg-lkkz">$14.85$</td>
    <td class="tg-zlpi">$14.88$</td>
    <td class="tg-zlpi">$641300$</td>
    <td class="tg-zlpi">$0$</td>
    <td class="tg-zlpi">$1$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">2006-03-30</td>
    <td class="tg-lkkz">BMA</td>
    <td class="tg-lkkz">$22.75$</td>
    <td class="tg-lkkz">$23.10$</td>
    <td class="tg-lkkz">$22.70$</td>
    <td class="tg-lkkz">$23.00$</td>
    <td class="tg-lkkz">$293600$</td>
    <td class="tg-lkkz">$15.32$</td>
    <td class="tg-lkkz">$15.56$</td>
    <td class="tg-lkkz">$15.29$</td>
    <td class="tg-zlpi">$15.49$</td>
    <td class="tg-zlpi">$293600$</td>
    <td class="tg-zlpi">$0$</td>
    <td class="tg-zlpi">$1$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">2006-03-31</td>
    <td class="tg-lkkz">BMA</td>
    <td class="tg-lkkz">$22.93$</td>
    <td class="tg-lkkz">$22.93$</td>
    <td class="tg-lkkz">$22.35$</td>
    <td class="tg-lkkz">$22.83$</td>
    <td class="tg-lkkz">$113600$</td>
    <td class="tg-lkkz">$15.44$</td>
    <td class="tg-lkkz">$15.44$</td>
    <td class="tg-lkkz">$15.05$</td>
    <td class="tg-zlpi">$15.38$</td>
    <td class="tg-zlpi">$113600$</td>
    <td class="tg-zlpi">$0$</td>
    <td class="tg-zlpi">$1$</td>
  </tr>
</table>

</br>

The data is indexed by date, with the `symbol` column holding the ticker name, and columns for the `open` and `close` prices (the price of the symbol at the start/end of the market day) and the `high` and `low` prices seen for the symbol at that date.  
We'll begin plotting the [`adjusted close`](http://www.crsp.com/products/documentation/crsp-calculations) prices for each symbol (price adjusted for dividends payed and stock splits). The reset of the columns can be safely ingored for our purposes.

</br>

![](img/0.6-troubled-markets-and-volatility_13_0.png)


Let's zoom in on the 2019 adjusted close prices.

</br>

![](img/0.6-troubled-markets-and-volatility_15_0.png)


We can see most stocks experienced a sharp decline in August 2019, after a surprise result of the presidential primaries caused a market crash. We also see that \$MELI (MercadoLibre) is less vulnerable to the volatility in the Argentine market because it operates in over a dozen countries in Latin America.

</br>

<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;}
.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;}
.tg .tg-ttiq{background-color:#002b36;color:#fffff8;border-color:#fffff8;text-align:center;vertical-align:top}
.tg .tg-664r{background-color:#fffff8;border-color:inherit;text-align:center;vertical-align:top}
.tg .tg-lkkz{background-color:#fffff8;border-color:#000000;text-align:center;vertical-align:top}
.tg .tg-zlpi{background-color:#fffff8;border-color:#002b36;text-align:center;vertical-align:top}
</style>
<table class="tg" style="undefined;table-layout: fixed; width: 793px">
<colgroup>
<col style="width: 125px">
<col style="width: 88px">
<col style="width: 71px">
<col style="width: 70px">
<col style="width: 79px">
<col style="width: 70px">
<col style="width: 98px">
<col style="width: 98px">
<col style="width: 94px">
</colgroup>
  <tr>
    <th class="tg-ttiq">Symbol</th>
    <th class="tg-ttiq">Count</th>
    <th class="tg-ttiq">Mean<br></th>
    <th class="tg-ttiq">Std<br></th>
    <th class="tg-ttiq">Min</th>
    <th class="tg-ttiq">25%</th>
    <th class="tg-ttiq">50%</th>
    <th class="tg-ttiq">75%<br></th>
    <th class="tg-ttiq">Max<br></th>
  </tr>
  <tr>
    <td class="tg-ttiq">BFR<br></td>
    <td class="tg-664r">$4936$</td>
    <td class="tg-664r">$8.28$</td>
    <td class="tg-664r">$5.71$</td>
    <td class="tg-664r">$0.75$</td>
    <td class="tg-lkkz">$3.95$</td>
    <td class="tg-lkkz">$5.72$</td>
    <td class="tg-lkkz">$12.03$</td>
    <td class="tg-zlpi">$25.45$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">BMA<br></td>
    <td class="tg-lkkz">$3371$</td>
    <td class="tg-lkkz">$31.18$</td>
    <td class="tg-lkkz">$25.47$</td>
    <td class="tg-lkkz">$5.00$</td>
    <td class="tg-lkkz">$15.79$</td>
    <td class="tg-lkkz">$24.6$</td>
    <td class="tg-lkkz">$48.91$</td>
    <td class="tg-zlpi">$125.43$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">CEPU<br></td>
    <td class="tg-lkkz">$386$</td>
    <td class="tg-lkkz">$10.99$</td>
    <td class="tg-lkkz">$2.89$</td>
    <td class="tg-lkkz">$3.46$</td>
    <td class="tg-lkkz">$9.06$</td>
    <td class="tg-lkkz">$9.97$</td>
    <td class="tg-lkkz">$12.28$</td>
    <td class="tg-zlpi">$17.92$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">CRESY</td>
    <td class="tg-lkkz">$4936$</td>
    <td class="tg-lkkz">$9.94$</td>
    <td class="tg-lkkz">$3.95$</td>
    <td class="tg-lkkz">$2.92$</td>
    <td class="tg-lkkz">$6.75$</td>
    <td class="tg-lkkz">$9.47$</td>
    <td class="tg-lkkz">$12.01$</td>
    <td class="tg-zlpi">$21.64$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">EDN<br></td>
    <td class="tg-lkkz">$3099$</td>
    <td class="tg-lkkz">$15.31$</td>
    <td class="tg-lkkz">$12.47$</td>
    <td class="tg-lkkz">$1.71$</td>
    <td class="tg-lkkz">$6.33$</td>
    <td class="tg-lkkz">$12.11$</td>
    <td class="tg-lkkz">$20.25$</td>
    <td class="tg-zlpi">$62.55$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">GGAL</td>
    <td class="tg-zlpi">$4795$</td>
    <td class="tg-zlpi">$13.55$</td>
    <td class="tg-zlpi">$13.20$</td>
    <td class="tg-zlpi">$0.21$</td>
    <td class="tg-zlpi">$5.40$</td>
    <td class="tg-zlpi">$7.97$</td>
    <td class="tg-zlpi">$16.44$</td>
    <td class="tg-zlpi">$71.46$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">IRCP</td>
    <td class="tg-zlpi">$3971$</td>
    <td class="tg-zlpi">$15.63$</td>
    <td class="tg-zlpi">$14.42$</td>
    <td class="tg-zlpi">$1.29$</td>
    <td class="tg-zlpi">$4.38$</td>
    <td class="tg-zlpi">$10.02$</td>
    <td class="tg-zlpi">$21.43$</td>
    <td class="tg-zlpi">$62.22$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">IRS<br></td>
    <td class="tg-zlpi">$4936$</td>
    <td class="tg-zlpi">$10.07$</td>
    <td class="tg-zlpi">$5.63$</td>
    <td class="tg-zlpi">$1.90$</td>
    <td class="tg-zlpi">$6.13$</td>
    <td class="tg-zlpi">$8.54$</td>
    <td class="tg-zlpi">$13.28$</td>
    <td class="tg-zlpi">$32.17$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">LOMA<br></td>
    <td class="tg-zlpi">$449$</td>
    <td class="tg-zlpi">$14.07$</td>
    <td class="tg-zlpi">$5.36$</td>
    <td class="tg-zlpi">$5.40$</td>
    <td class="tg-zlpi">$10.34$</td>
    <td class="tg-zlpi">$11.74$</td>
    <td class="tg-zlpi">$21.12$</td>
    <td class="tg-zlpi">$25.02$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">MELI<br></td>
    <td class="tg-zlpi">$3025$</td>
    <td class="tg-zlpi">$138.09$</td>
    <td class="tg-zlpi">$126.90$</td>
    <td class="tg-zlpi">$8.02$</td>
    <td class="tg-zlpi">$59.11$</td>
    <td class="tg-zlpi">$93.59$</td>
    <td class="tg-zlpi">$153.61$</td>
    <td class="tg-zlpi">$69.01$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">NTL<br></td>
    <td class="tg-zlpi">$4519$</td>
    <td class="tg-zlpi">$13.15$</td>
    <td class="tg-zlpi">$8.40$</td>
    <td class="tg-zlpi">$0.39$</td>
    <td class="tg-zlpi">$6.55$</td>
    <td class="tg-zlpi">$12.76$</td>
    <td class="tg-zlpi">$18.68$</td>
    <td class="tg-zlpi">$51.70$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">PAM</td>
    <td class="tg-zlpi">$2479$</td>
    <td class="tg-zlpi">$21.47$</td>
    <td class="tg-zlpi">$18.06$</td>
    <td class="tg-zlpi">$2.85$</td>
    <td class="tg-zlpi">$9.89$</td>
    <td class="tg-zlpi">$14.59$</td>
    <td class="tg-zlpi">$30.80$</td>
    <td class="tg-zlpi">$71.65$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">PZE</td>
    <td class="tg-zlpi">$4608$</td>
    <td class="tg-zlpi">$5.87$</td>
    <td class="tg-zlpi">$2.46$</td>
    <td class="tg-zlpi">$1.52$</td>
    <td class="tg-zlpi">$4.36$</td>
    <td class="tg-zlpi">$5.37$</td>
    <td class="tg-zlpi">$6.72$</td>
    <td class="tg-zlpi">$14.55$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">SUPV<br></td>
    <td class="tg-zlpi">$816$</td>
    <td class="tg-zlpi">$15.18$</td>
    <td class="tg-zlpi">$7.34$</td>
    <td class="tg-zlpi">$3.16$</td>
    <td class="tg-zlpi">$8.92$</td>
    <td class="tg-zlpi">$13.91$</td>
    <td class="tg-zlpi">$17.84$</td>
    <td class="tg-zlpi">$32.37$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">TEO</td>
    <td class="tg-zlpi">$4936$</td>
    <td class="tg-zlpi">$12.20$</td>
    <td class="tg-zlpi">$6.37$</td>
    <td class="tg-zlpi">$0.38$</td>
    <td class="tg-zlpi">$7.64$</td>
    <td class="tg-zlpi">$12.43$</td>
    <td class="tg-zlpi">$16.01$</td>
    <td class="tg-zlpi">$35.96$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">TGS</td>
    <td class="tg-zlpi">$4936$</td>
    <td class="tg-zlpi">$4.00$</td>
    <td class="tg-zlpi">$4.34$</td>
    <td class="tg-zlpi">$0.29$</td>
    <td class="tg-zlpi">$1.62$</td>
    <td class="tg-zlpi">$2.46$</td>
    <td class="tg-zlpi">$3.51$</td>
    <td class="tg-zlpi">$20.52$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">TS</td>
    <td class="tg-zlpi">$4195$</td>
    <td class="tg-zlpi">$25.94$</td>
    <td class="tg-zlpi">$10.95$</td>
    <td class="tg-zlpi">$2.26$</td>
    <td class="tg-zlpi">$21.35$</td>
    <td class="tg-zlpi">$28.22$</td>
    <td class="tg-zlpi">$34.12$</td>
    <td class="tg-zlpi">$55.72$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">TX<br></td>
    <td class="tg-zlpi">$3408$</td>
    <td class="tg-zlpi">$20.25$</td>
    <td class="tg-zlpi">$6.30$</td>
    <td class="tg-zlpi">$3.27$</td>
    <td class="tg-zlpi">$16.04$</td>
    <td class="tg-zlpi">$19.85$</td>
    <td class="tg-zlpi">$24.57$</td>
    <td class="tg-zlpi">$39.30$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">YPF</td>
    <td class="tg-zlpi">$4936$</td>
    <td class="tg-zlpi">$21.58$</td>
    <td class="tg-zlpi">$9.67$</td>
    <td class="tg-zlpi">$3.16$</td>
    <td class="tg-zlpi">$14.03$</td>
    <td class="tg-zlpi">$21.59$</td>
    <td class="tg-zlpi">$29.67$</td>
    <td class="tg-zlpi">$47.31$</td>
  </tr>
</table>
</br>

### Simple returns

Next we'll calculate the daily _simple returns_.  

</br>

$$R_t \equiv \frac{S_t - S_{t-1}}{S_{t-1}}  \%$$

</br>

<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;border-color:#93a1a1;}
.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#93a1a1;color:#002b36;background-color:#fdf6e3;}
.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#93a1a1;color:#fdf6e3;background-color:#657b83;}
.tg .tg-8a3j{background-color:#fffff8;color:#002b36;border-color:#002b36;text-align:center;vertical-align:top}
.tg .tg-ttiq{background-color:#002b36;color:#fffff8;border-color:#fffff8;text-align:center;vertical-align:top}
.tg .tg-fq4g{background-color:#002b36;color:#fffff8;border-color:#fffff8;text-align:center;vertical-align:top}
.tg .tg-664r{background-color:#fffff8;border-color:inherit;text-align:center;vertical-align:top}
.tg .tg-lkkz{background-color:#fffff8;border-color:#000000;text-align:center;vertical-align:top}
.tg .tg-zlpi{background-color:#fffff8;border-color:#002b36;text-align:center;vertical-align:top}
</style>
<table class="tg" style="undefined;table-layout: fixed; width: 966px">
<colgroup>
<col style="width: 83px">
<col style="width: 58px">
<col style="width: 47px">
<col style="width: 46px">
<col style="width: 51px">
<col style="width: 46px">
<col style="width: 65px">
<col style="width: 65px">
<col style="width: 62px">
<col style="width: 74px">
<col style="width: 70px">
<col style="width: 80px">
<col style="width: 64px">
<col style="width: 80px">
<col style="width: 75px">
</colgroup>
  <tr>
    <th class="tg-ttiq">Date<br></th>
    <th class="tg-ttiq">Symbol</th>
    <th class="tg-ttiq">Close<br></th>
    <th class="tg-ttiq">High<br></th>
    <th class="tg-ttiq">Low<br></th>
    <th class="tg-ttiq">Open<br></th>
    <th class="tg-ttiq">Volume<br></th>
    <th class="tg-ttiq">adjClose</th>
    <th class="tg-ttiq">adjHigh</th>
    <th class="tg-ttiq">adjLow</th>
    <th class="tg-ttiq">adjOpen</th>
    <th class="tg-ttiq">adjVolume</th>
    <th class="tg-ttiq">divCash</th>
    <th class="tg-ttiq">splitFactor</th>
    <th class="tg-fq4g">Return</th>
  </tr>
  <tr>
    <td class="tg-ttiq">2006-03-27</td>
    <td class="tg-664r">BMA</td>
    <td class="tg-664r">$23.05$</td>
    <td class="tg-664r">$23.05$<br></td>
    <td class="tg-664r">$22.23$</td>
    <td class="tg-lkkz">$22.89$<br></td>
    <td class="tg-lkkz">$1065200$<br></td>
    <td class="tg-lkkz">$15.52$</td>
    <td class="tg-lkkz">$15.52$</td>
    <td class="tg-lkkz">$14.08$</td>
    <td class="tg-zlpi">$15.42$</td>
    <td class="tg-zlpi">$1065200$</td>
    <td class="tg-zlpi">$0$</td>
    <td class="tg-zlpi">$1$</td>
    <td class="tg-8a3j">NaN<br></td>
  </tr>
  <tr>
    <td class="tg-ttiq">2006-03-28</td>
    <td class="tg-lkkz">BMA</td>
    <td class="tg-lkkz">$22.38$</td>
    <td class="tg-lkkz">$22.47$</td>
    <td class="tg-lkkz">$21.90$</td>
    <td class="tg-lkkz">$22.47$</td>
    <td class="tg-lkkz">$1556100$</td>
    <td class="tg-lkkz">$15.07$</td>
    <td class="tg-lkkz">$15.13$</td>
    <td class="tg-lkkz">$14.75$</td>
    <td class="tg-zlpi">$15.13$</td>
    <td class="tg-zlpi">$1556100$</td>
    <td class="tg-zlpi">$0$</td>
    <td class="tg-zlpi">$1$</td>
    <td class="tg-8a3j">$-2.91$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">2006-03-29</td>
    <td class="tg-lkkz">BMA</td>
    <td class="tg-lkkz">$22.84$</td>
    <td class="tg-lkkz">$23.14$</td>
    <td class="tg-lkkz">$22.05$</td>
    <td class="tg-lkkz">$22.10$</td>
    <td class="tg-lkkz">$641300$</td>
    <td class="tg-lkkz">$15.38$</td>
    <td class="tg-lkkz">$15.59$</td>
    <td class="tg-lkkz">$14.85$</td>
    <td class="tg-zlpi">$14.88$</td>
    <td class="tg-zlpi">$641300$</td>
    <td class="tg-zlpi">$0$</td>
    <td class="tg-zlpi">$1$</td>
    <td class="tg-8a3j">$2.06$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">2006-03-30</td>
    <td class="tg-lkkz">BMA</td>
    <td class="tg-lkkz">$22.75$</td>
    <td class="tg-lkkz">$23.10$</td>
    <td class="tg-lkkz">$22.70$</td>
    <td class="tg-lkkz">$23.00$</td>
    <td class="tg-lkkz">$293600$</td>
    <td class="tg-lkkz">$15.32$</td>
    <td class="tg-lkkz">$15.56$</td>
    <td class="tg-lkkz">$15.29$</td>
    <td class="tg-zlpi">$15.49$</td>
    <td class="tg-zlpi">$293600$</td>
    <td class="tg-zlpi">$0$</td>
    <td class="tg-zlpi">$1$</td>
    <td class="tg-8a3j">$-0.39$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">2006-03-31</td>
    <td class="tg-lkkz">BMA</td>
    <td class="tg-lkkz">$22.93$</td>
    <td class="tg-lkkz">$22.93$</td>
    <td class="tg-lkkz">$22.35$</td>
    <td class="tg-lkkz">$22.83$</td>
    <td class="tg-lkkz">$113600$</td>
    <td class="tg-lkkz">$15.44$</td>
    <td class="tg-lkkz">$15.44$</td>
    <td class="tg-lkkz">$15.05$</td>
    <td class="tg-zlpi">$15.38$</td>
    <td class="tg-zlpi">$113600$</td>
    <td class="tg-zlpi">$0$</td>
    <td class="tg-zlpi">$1$</td>
    <td class="tg-8a3j">$0.79$</td>
  </tr>
</table>

</br>
<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;}
.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;}
.tg .tg-ttiq{background-color:#002b36;color:#fffff8;border-color:#fffff8;text-align:center;vertical-align:top}
.tg .tg-664r{background-color:#fffff8;border-color:inherit;text-align:center;vertical-align:top}
.tg .tg-lkkz{background-color:#fffff8;border-color:#000000;text-align:center;vertical-align:top}
.tg .tg-zlpi{background-color:#fffff8;border-color:#002b36;text-align:center;vertical-align:top}
</style>
<table class="tg" style="undefined;table-layout: fixed; width: 804px">
<colgroup>
<col style="width: 126.166667px">
<col style="width: 89.166667px">
<col style="width: 72.166667px">
<col style="width: 71.166667px">
<col style="width: 80.166667px">
<col style="width: 71.166667px">
<col style="width: 99.166667px">
<col style="width: 99.166667px">
<col style="width: 95.166667px">
</colgroup>
  <tr>
    <th class="tg-ttiq">Symbol</th>
    <th class="tg-ttiq">Count</th>
    <th class="tg-ttiq">Mean<br></th>
    <th class="tg-ttiq">Std<br></th>
    <th class="tg-ttiq">Min</th>
    <th class="tg-ttiq">25%</th>
    <th class="tg-ttiq">50%</th>
    <th class="tg-ttiq">75%<br></th>
    <th class="tg-ttiq">Max<br></th>
  </tr>
  <tr>
    <td class="tg-ttiq">BFR<br></td>
    <td class="tg-664r">$4936$</td>
    <td class="tg-664r">$0.053$</td>
    <td class="tg-664r">$3.67$</td>
    <td class="tg-664r">$-55.85$</td>
    <td class="tg-lkkz">$-1.73$</td>
    <td class="tg-lkkz">$0$<br></td>
    <td class="tg-lkkz">$1.69$</td>
    <td class="tg-zlpi">$46.76$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">BMA<br></td>
    <td class="tg-lkkz">$3371$</td>
    <td class="tg-lkkz">$0.08$</td>
    <td class="tg-lkkz">$3.28$</td>
    <td class="tg-lkkz">$-52.67$</td>
    <td class="tg-lkkz">$-1.49$</td>
    <td class="tg-lkkz">$0$</td>
    <td class="tg-lkkz">$1.65$</td>
    <td class="tg-zlpi">$27.01$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">CEPU<br></td>
    <td class="tg-lkkz">$386$</td>
    <td class="tg-lkkz">$-0.26$</td>
    <td class="tg-lkkz">$4.31$</td>
    <td class="tg-lkkz">$-55.92$</td>
    <td class="tg-lkkz">$-1.91$</td>
    <td class="tg-lkkz">$-0.32$</td>
    <td class="tg-lkkz">$1.58$</td>
    <td class="tg-zlpi">$16.88$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">CRESY</td>
    <td class="tg-lkkz">$4936$</td>
    <td class="tg-lkkz">$0.038$</td>
    <td class="tg-lkkz">$2.77$</td>
    <td class="tg-lkkz">$-38.09$</td>
    <td class="tg-lkkz">$-1.25$</td>
    <td class="tg-lkkz">$0$</td>
    <td class="tg-lkkz">$1.184$</td>
    <td class="tg-zlpi">$27.19$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">EDN<br></td>
    <td class="tg-lkkz">$3099$</td>
    <td class="tg-lkkz">$0.051$</td>
    <td class="tg-lkkz">$3.88$</td>
    <td class="tg-lkkz">$-58.98$</td>
    <td class="tg-lkkz">$-1.69$</td>
    <td class="tg-lkkz">$-0.031$</td>
    <td class="tg-lkkz">$1.63$</td>
    <td class="tg-zlpi">$27.55$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">GGAL</td>
    <td class="tg-zlpi">$4795$</td>
    <td class="tg-zlpi">$0.095$</td>
    <td class="tg-zlpi">$4.63$</td>
    <td class="tg-zlpi">$-56.12$</td>
    <td class="tg-zlpi">$-1.63$</td>
    <td class="tg-zlpi">$0$</td>
    <td class="tg-zlpi">$1.69$</td>
    <td class="tg-zlpi">$153.6$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">IRCP</td>
    <td class="tg-zlpi">$3971$</td>
    <td class="tg-zlpi">$0.14$</td>
    <td class="tg-zlpi">$4.23$</td>
    <td class="tg-zlpi">$-32.42$</td>
    <td class="tg-zlpi">$-0.68$</td>
    <td class="tg-zlpi">$0$</td>
    <td class="tg-zlpi">$0.85$</td>
    <td class="tg-zlpi">$36.99$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">IRS<br></td>
    <td class="tg-zlpi">$4936$</td>
    <td class="tg-zlpi">$0.016$</td>
    <td class="tg-zlpi">$2.68$</td>
    <td class="tg-zlpi">$-38.29$</td>
    <td class="tg-zlpi">$-1.25$</td>
    <td class="tg-zlpi">$0$</td>
    <td class="tg-zlpi">$1.21$</td>
    <td class="tg-zlpi">$18.08$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">LOMA<br></td>
    <td class="tg-zlpi">$449$</td>
    <td class="tg-zlpi">$-0.166$</td>
    <td class="tg-zlpi">$4.53$</td>
    <td class="tg-zlpi">$-57.30$</td>
    <td class="tg-zlpi">$-1.88$</td>
    <td class="tg-zlpi">$-0.087$</td>
    <td class="tg-zlpi">$1.51$</td>
    <td class="tg-zlpi">$22.65$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">MELI<br></td>
    <td class="tg-zlpi">$3025$</td>
    <td class="tg-zlpi">$0.16$</td>
    <td class="tg-zlpi">$3.57$</td>
    <td class="tg-zlpi">$-21.20$</td>
    <td class="tg-zlpi">$-1.40$</td>
    <td class="tg-zlpi">$0.084$</td>
    <td class="tg-zlpi">$1.59$</td>
    <td class="tg-zlpi">$36.00$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">NTL<br></td>
    <td class="tg-zlpi">$4519$</td>
    <td class="tg-zlpi">$0.082$</td>
    <td class="tg-zlpi">$3.34$</td>
    <td class="tg-zlpi">$-46.19$</td>
    <td class="tg-zlpi">$-1.32$</td>
    <td class="tg-zlpi">$0$</td>
    <td class="tg-zlpi">$1.37$</td>
    <td class="tg-zlpi">$30.00$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">PAM</td>
    <td class="tg-zlpi">$2479$</td>
    <td class="tg-zlpi">$0.06$</td>
    <td class="tg-zlpi">$2.96$</td>
    <td class="tg-zlpi">$-53.82$</td>
    <td class="tg-zlpi">$-1.42$</td>
    <td class="tg-zlpi">$0$</td>
    <td class="tg-zlpi">$1.41$</td>
    <td class="tg-zlpi">$16.94$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">PZE</td>
    <td class="tg-zlpi">$4608$</td>
    <td class="tg-zlpi">$0.066$</td>
    <td class="tg-zlpi">$3.91$</td>
    <td class="tg-zlpi">$-19.22$</td>
    <td class="tg-zlpi">$-1.46$</td>
    <td class="tg-zlpi">$0$</td>
    <td class="tg-zlpi">$1.42$</td>
    <td class="tg-zlpi">$179.84$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">SUPV<br></td>
    <td class="tg-zlpi">$816$</td>
    <td class="tg-zlpi">$-0.025$</td>
    <td class="tg-zlpi">$4.18$</td>
    <td class="tg-zlpi">$-58.75$</td>
    <td class="tg-zlpi">$-1.41$</td>
    <td class="tg-zlpi">$0$</td>
    <td class="tg-zlpi">$1.49$</td>
    <td class="tg-zlpi">$28.33$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">TEO</td>
    <td class="tg-zlpi">$4936$</td>
    <td class="tg-zlpi">$0.035$</td>
    <td class="tg-zlpi">$3.08$</td>
    <td class="tg-zlpi">$-33.38$</td>
    <td class="tg-zlpi">$-1.42$</td>
    <td class="tg-zlpi">$0$</td>
    <td class="tg-zlpi">$1.45$</td>
    <td class="tg-zlpi">$23.07$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">TGS</td>
    <td class="tg-zlpi">$4936$</td>
    <td class="tg-zlpi">$0.078$</td>
    <td class="tg-zlpi">$3.39$</td>
    <td class="tg-zlpi">$-48.03$</td>
    <td class="tg-zlpi">$-1.49$</td>
    <td class="tg-zlpi">$0$</td>
    <td class="tg-zlpi">$1.62$</td>
    <td class="tg-zlpi">$25.20$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">TS</td>
    <td class="tg-zlpi">$4195$</td>
    <td class="tg-zlpi">$0.085$</td>
    <td class="tg-zlpi">$2.53$</td>
    <td class="tg-zlpi">$-21.31$</td>
    <td class="tg-zlpi">$-1.18$</td>
    <td class="tg-zlpi">$0.11$</td>
    <td class="tg-zlpi">$1.35$</td>
    <td class="tg-zlpi">$21.57$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">TX<br></td>
    <td class="tg-zlpi">$3408$</td>
    <td class="tg-zlpi">$0.047$</td>
    <td class="tg-zlpi">$3.02$</td>
    <td class="tg-zlpi">$-19.68$</td>
    <td class="tg-zlpi">$-1.35$</td>
    <td class="tg-zlpi">$0.037$</td>
    <td class="tg-zlpi">$1.41$</td>
    <td class="tg-zlpi">$49.09$</td>
  </tr>
  <tr>
    <td class="tg-ttiq">YPF</td>
    <td class="tg-zlpi">$4936$</td>
    <td class="tg-zlpi">$0.033$</td>
    <td class="tg-zlpi">$2.56$</td>
    <td class="tg-zlpi">$-34.05$</td>
    <td class="tg-zlpi">$-1.12$</td>
    <td class="tg-zlpi">$0$</td>
    <td class="tg-zlpi">$1.12$</td>
    <td class="tg-zlpi">$37.25$</td>
  </tr>
</table>
</br>

Let's plot a histogram of the daily returns for each symbol.

</br>

![](img/0.6-troubled-markets-and-volatility_23_0.png)


We see most returns cluster around 0, with a few outliers. Since we are interested particularly in the outliers, to see their quantity and magnitude, we can visualize them using a [boxenplot](https://vita.had.co.nz/papers/letter-value-plot.html).

</br>

![](img/0.6-troubled-markets-and-volatility_26_0.png)


We can filter the days with 30% or larger movement in prices (either up or down).

</br>

![](img/0.6-troubled-markets-and-volatility_28_0.png)


Now if we remove outliers, say discard days where return was higher than 10% or lower than -10%:

</br>

![](img/0.6-troubled-markets-and-volatility_30_0.png)

</br>

### Log returns

In finance, it is common to look at the _log returns_ of an asset. They are defined as follows:

</br>

$$r_t \equiv \ln{\frac{S_t}{S_{t-1}}} = \ln{S_t} - \ln{S_{t-1}}$$

</br>

There is an equivalence between simple and log returns:

</br>

\begin{align}
r_t &= \ln{(R_t + 1)} \
R_t &= \exp{r_t} - 1
\end{align}

</br>

You can find further information on the two return types in this [post](https://www.portfolioprobe.com/2010/10/04/a-tale-of-two-returns/).

Stock prices are assumed to follow a [log-normal](https://en.wikipedia.org/wiki/Log-normal_distribution) distribution, hence we should expect log returns to be distributed [normally](https://en.wikipedia.org/wiki/Normal_distribution).

</br>

$$ln(S_T)\sim N\big[ln(S_0)+(\mu-\frac{\sigma^2}{2})T,\;\sigma^2T\big] \
ln(\frac{S_T}{S_0})\sim N\big[(\mu-\frac{\sigma^2}{2})T, \;\sigma^2T\big]$$

</br>

Where $S_T$ is the price of the underlying at time $T$.  
For a more detailed discussion on the assumptions of the [Black-Scholes-Merton](https://en.wikipedia.org/wiki/Black–Scholes_model) model, see chapter 15 of _Options, Futures and Other Derivatives_ (9th Ed) by John Hull.  
You can read more on the distribution of prices and returns [here](https://www.investopedia.com/articles/investing/102014/lognormal-and-normal-distribution.asp).


Now we can calculate the [volatility](https://en.wikipedia.org/wiki/Volatility_(finance)) $\sigma$ for each symbol, defined as the [standard deviation](https://en.wikipedia.org/wiki/Standard_deviation) of log returns.  
As a comparison, we'll add the daily volatility (from 2000 to 2019) for four of the so called [blue chip stocks](https://www.investopedia.com/terms/b/bluechipstock.asp), Coca-Cola (\$KO), Goldman Sachs (\$GS), IBM (\$IBM) and Walmart (\$WMT).

</br>

![](img/0.6-troubled-markets-and-volatility_37_0.png)


We can see that Argentine stocks show much higher volatility than the blue chip stocks.

Let's plot the mean yearly returns for each symbol. Again, we'll add the mean daily return of the US blue chips.

</br>

![](img/0.6-troubled-markets-and-volatility_41_0.png)


As expected, besides increased volatility, Argentine stocks, for the most part, exhibit higher yearly returns than the chosen US stocks.

</br>

### A closer look at outliers

Let's plot the returns that are at least $3\sigma$ away from the mean. If log returns were truly distributed normally, then we should expect this group to represent only $0.3\%$ of the data, while the remaining $99.7\%$ should lie in the interval $(\mu_r - 3\sigma_r, \mu_r + 3\sigma_r)$.

</br>

![](img/0.6-troubled-markets-and-volatility_46_0.png)


We see a large number of outlier return days. To put that in perspective, let's calculate the proportion of outlier returns for each symbol in the data, that is the number of days where $3\sigma$ returns where observed over the total number of observations.

</br>

![](img/0.6-troubled-markets-and-volatility_48_0.png)


We see many more outliers than the expected $0.3\%$. For example, \$MELI has almost 7 times more outlier return days than expected if we assumed normal log returns.

Finally, we'll look at the cumulative log returns over time.

</br>

![](img/0.6-troubled-markets-and-volatility_51_0.png)


If you had invested in \$MELI's IPO in 2007, you've had have over 25 times your initial investment by August 2019. You would also have to stomach losing close to 60% at the end of 2008.

</br>

### ADR options and the volatility smile

We've observed ADRs experienced a very high volatility, and this leads us to question wether the prices of financial derivatives such as options were affected.

We will explore how volatility in the prices of the underlying assests impacted option prices during the crash.

To this end, we will examine the options end-of-day data for the ADRs. [Options](https://www.investopedia.com/terms/o/option.asp) are derivative contracts based on an underlying asset such as stocks. They offer the buyer the opportunity to buy or sell the underlying asset at a given price (or _strike price_). You can find more information on options in [this article](../intro-finance.index.html).

</br>
<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;border-color:#93a1a1;}
.tg td{font-family:Arial, sans-serif;font-size:12px;padding:8px 4px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#93a1a1;color:#002b36;background-color:#fdf6e3;}
.tg th{font-family:Arial, sans-serif;font-size:12px;font-weight:normal;padding:8px 4px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#93a1a1;color:#fdf6e3;background-color:#657b83;}
.tg .tg-ttiq{background-color:#002b36;color:#fffff8;border-color:#fffff8;text-align:center;vertical-align:top}
.tg .tg-6uqc{background-color:#002b36;color:#fffff8;border-color:inherit;text-align:center;vertical-align:top}
.tg .tg-664r{background-color:#fffff8;border-color:inherit;text-align:center;vertical-align:top}
.tg .tg-lkkz{background-color:#fffff8;border-color:#000000;text-align:center;vertical-align:top}
.tg .tg-zlpi{background-color:#fffff8;border-color:#002b36;text-align:center;vertical-align:top}
</style>
<table class="tg" style="undefined;table-layout: fixed; width: 1185px">
<colgroup>
<col style="width: 80px">
<col style="width: 65px">
<col style="width: 80px">
<col style="width: 54px">
<col style="width: 120px">
<col style="width: 35px">
<col style="width: 80px">
<col style="width: 46px">
<col style="width: 35px">
<col style="width: 30px">
<col style="width: 30px">
<col style="width: 41px">
<col style="width: 44px">
<col style="width: 64px">
<col style="width: 60px">
<col style="width: 52px">
<col style="width: 61px">
</colgroup>
  <tr>
    <th class="tg-ttiq">quotedate</th>
    <th class="tg-ttiq">underlying</th>
    <th class="tg-ttiq">underlying_last</th>
    <th class="tg-ttiq">exchange</th>
    <th class="tg-ttiq">optionroot</th>
    <th class="tg-ttiq">type</th>
    <th class="tg-ttiq">expiration</th>
    <th class="tg-ttiq">strike</th>
    <th class="tg-ttiq">last</th>
    <th class="tg-ttiq">net</th>
    <th class="tg-ttiq">bid</th>
    <th class="tg-ttiq">ask</th>
    <th class="tg-ttiq">volume</th>
    <th class="tg-ttiq">openinterest</th>
    <th class="tg-6uqc">impliedvol</th>
    <th class="tg-6uqc">delta</th>
    <th class="tg-6uqc">gamma</th>
  </tr>
  <tr>
    <td class="tg-ttiq">2019-07-03</td>
    <td class="tg-664r">TEO</td>
    <td class="tg-664r">17.79</td>
    <td class="tg-664r">CBOE</td>
    <td class="tg-664r">TEO190719C00002500</td>
    <td class="tg-lkkz">call</td>
    <td class="tg-lkkz">2019-07-19</td>
    <td class="tg-lkkz">2.5</td>
    <td class="tg-lkkz">0</td>
    <td class="tg-lkkz">0</td>
    <td class="tg-zlpi">13.0</td>
    <td class="tg-zlpi">17.8</td>
    <td class="tg-zlpi">0</td>
    <td class="tg-zlpi">0</td>
    <td class="tg-664r">0.02</td>
    <td class="tg-664r">1.28</td>
    <td class="tg-664r">0.0000</td>
  </tr>
  <tr>
    <td class="tg-ttiq">2019-07-03</td>
    <td class="tg-lkkz">TEO</td>
    <td class="tg-lkkz">17.79</td>
    <td class="tg-lkkz">CBOE</td>
    <td class="tg-lkkz">TEO190719C00005000</td>
    <td class="tg-lkkz">call</td>
    <td class="tg-lkkz">2019-07-19</td>
    <td class="tg-lkkz">5.0</td>
    <td class="tg-lkkz">0</td>
    <td class="tg-lkkz">0</td>
    <td class="tg-zlpi">10.5</td>
    <td class="tg-zlpi">15.2</td>
    <td class="tg-zlpi">0</td>
    <td class="tg-zlpi">0</td>
    <td class="tg-664r">6.32</td>
    <td class="tg-664r">0.94</td>
    <td class="tg-664r">0.0045</td>
  </tr>
  <tr>
    <td class="tg-ttiq">2019-07-03</td>
    <td class="tg-lkkz">TEO</td>
    <td class="tg-lkkz">17.79</td>
    <td class="tg-lkkz">CBOE</td>
    <td class="tg-lkkz">TEO190719C00007500</td>
    <td class="tg-lkkz">call</td>
    <td class="tg-lkkz">2019-07-19</td>
    <td class="tg-lkkz">7.5</td>
    <td class="tg-lkkz">0</td>
    <td class="tg-lkkz">0</td>
    <td class="tg-zlpi">8.0</td>
    <td class="tg-zlpi">12.8</td>
    <td class="tg-zlpi">0</td>
    <td class="tg-zlpi">0</td>
    <td class="tg-664r">3.57</td>
    <td class="tg-664r">0.93</td>
    <td class="tg-664r">0.0093</td>
  </tr>
  <tr>
    <td class="tg-ttiq">2019-07-03</td>
    <td class="tg-lkkz">TEO</td>
    <td class="tg-lkkz">17.79</td>
    <td class="tg-lkkz">CBOE</td>
    <td class="tg-lkkz">TEO190719C00010000</td>
    <td class="tg-lkkz">call</td>
    <td class="tg-lkkz">2019-07-19</td>
    <td class="tg-lkkz">10</td>
    <td class="tg-lkkz">0</td>
    <td class="tg-lkkz">0</td>
    <td class="tg-zlpi">5.5</td>
    <td class="tg-zlpi">10.2</td>
    <td class="tg-zlpi">0</td>
    <td class="tg-zlpi">1</td>
    <td class="tg-664r">2.04</td>
    <td class="tg-664r">0.94</td>
    <td class="tg-664r">0.0156</td>
  </tr>
  <tr>
    <td class="tg-ttiq">2019-07-03</td>
    <td class="tg-lkkz">TEO</td>
    <td class="tg-lkkz">17.79</td>
    <td class="tg-lkkz">CBOE</td>
    <td class="tg-lkkz">TEO190719C00012500</td>
    <td class="tg-lkkz">call</td>
    <td class="tg-lkkz">2019-07-19</td>
    <td class="tg-lkkz">12.5</td>
    <td class="tg-lkkz">0</td>
    <td class="tg-lkkz">0</td>
    <td class="tg-zlpi">3.0</td>
    <td class="tg-zlpi">7.8</td>
    <td class="tg-zlpi">0</td>
    <td class="tg-zlpi">199</td>
    <td class="tg-664r">1.28</td>
    <td class="tg-664r">0.92</td>
    <td class="tg-664r">0.0297</td>
  </tr>
</table>

</br>

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

</br>

![](img/0.6-troubled-markets-and-volatility_58_0.png)


We see that as options move more [at the money](https://www.investopedia.com/terms/a/atthemoney.asp) (ATM) their implied volatility drops. In contrast, options that are further [out of the money](https://www.investopedia.com/terms/o/outofthemoney.asp) (OTM) or in the money (ITM) have higher IVs.

Now let's try the same plot for the following Monday (2019-08-12). That day, the [MERVAL](https://en.wikipedia.org/wiki/MERVAL) (an index that tracks the biggest companies listed in the Buenos Aires Stock Exchange) crashed and lost close to 50% of its USD value.

</br>

![](img/0.6-troubled-markets-and-volatility_61_0.png)


As stock prices droped sharply, we find less put contracts were being offered. Again, we see IV getting higher as the strike priced moves away from the spot price.

</br>

### Option price evolution

Next, we'll analyze how option prices changed during the month of August, 2019.
Let's find the 10 most actively traded options (those with the highest open interest) for each symbol at the start of the month.

</br>

![](img/0.6-troubled-markets-and-volatility_71_0.png)


Note that the \$BFR plot shows all calls with an `ask` price of 0.0. In June 2019, Banco Francés SA [announced](https://finance.yahoo.com/news/bbva-banco-franc-change-ticker-165400264.html) it would  change its ticker symbol from \$BFR to \$BBAR. We will update the plots when we get the correct data for the missing months.

</br>

![](img/0.6-troubled-markets-and-volatility_73_0.png)


This plots reveal a huge drop in prices for the calls, and, conversely, a large increase in the price of puts, between Friday 9th and Monday 12th.

</br>

**June 2019**

As a comparison, let's try plotting the option prices for June 2019, a more uneventful month for the Argentine market.


![](img/0.6-troubled-markets-and-volatility_81_0.png)


Next we'll have a look the the actively traded puts for June 2019.

</br>

![](img/0.6-troubled-markets-and-volatility_83_0.png)

</br>

**October 2015**

Let's have a look at the options data from October, November and December 2015.  
During those months, the Argentine elections took place, which marked the beginning of a bull market. In the following four years, the MERVAL index increased four-fold its value in Pesos.

</br>

![](img/0.6-troubled-markets-and-volatility_90_0.png)


Now let's plot the actively traded puts for October 2015

</br>

![](img/0.6-troubled-markets-and-volatility_92_0.png)


**November 2015**

</br>

![](img/0.6-troubled-markets-and-volatility_98_0.png)

</br>

![](img/0.6-troubled-markets-and-volatility_99_0.png)

</br>

**December 2015**

</br>

![](img/0.6-troubled-markets-and-volatility_105_0.png)

</br>

![](img/0.6-troubled-markets-and-volatility_106_0.png)

</br>

**January 2008**

We'll examine the Argentine ADR options data for January 2008, the beginning of the US mortgage crisis, which had global effects. We only have data for 3 companies: \$MELI, \$TS and \$TX.

</br>

![](img/0.6-troubled-markets-and-volatility_113_0.png)


![](img/0.6-troubled-markets-and-volatility_114_0.png)


As the market went bearish, calls decreased in value and puts became more expensive.

</br>

## Final notes

Countries such as Argentina exhibit high [political beta](https://www.fa-mag.com/news/political-beta-44530.html): stocks show extreme sensitivity to political events. The MERVAL index nearly quadrupled its value in Pesos since December 2015, only to drop by 40% in a single day in August 2019.  
Investors tend to exacerbate bull runs, discounting future growth in the current stock prices. At the prospect of regulatory changes and political turnover, they panic sell and seek less risky assets. There remains to be seen whether savvy traders can exploit both the overconfident bulls and the panicking bears, buying volatility from the former to sell it at a profit to the latter.
