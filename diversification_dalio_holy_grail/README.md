# Ray Dalio's Holy Grail
<br>

### _Reducing return/risk ratio through diversification._

From _Principles: Life and Work_ by Ray Dalio.

> From my earlier failures, I knew that no matter how confident I was in making any one bet I could still be wrong—and that proper diversification was the key to reducing risks without reducing returns. If I could build a portfolio filled with high-quality return streams that were properly diversified (they zigged and zagged in ways that balanced each other out), I could offer clients an overall portfolio return much more consistent and reliable than what they could get elsewhere.”

In this notebook, we'll explore what Ray Dalio referrs to as the _Holy Grail of Investing_, how increasing diversification we are able to reduce overall risk, as measured by the standard deviation of portfolio returns.  
The idea is to show that, if we can find a basket of uncorrelated return streams (in practice we allow for low correlation), we can reduce the portfolio risk significantly by increasing the number of streams in our portfolio.

We begin by creating a function that simulates `n` return streams with a given mean (`mean`) and standard deviation (`risk`), and a given average correlation (`corr`) between them. We set $n=5$, $mean=10$, $std=15$ and $corr=0.6$.
Just to make sure, let's do a sanity check calculating the mean, std and correlation coefficient of the data obtained with the simulation.

$streams$ $mean =$ 


<table class="matrix" style="margin-top:-55px; margin-left:210px;" >
  <tr>
    <th class="tg-hq8v">$10.12$, <br></th>
    <th class="tg-hq8v">$9.91$, </th>
    <th class="tg-hq8v">$9.95$, <br></th>
    <th class="tg-hq8v">$10.06$, </th>
    <th class="tg-hq8v">$9.95$</th>
  </tr>
</table>

$streams$ $std =$ 


<table class="matrix" style="margin-top:-55px; margin-left:210px;">
  <tr>
    <th class="tg-hq8v">$15.07$, </th>
    <th class="tg-hq8v">$15.05$, <br></th>
    <th class="tg-hq8v">$15.09$, <br></th>
    <th class="tg-hq8v">$15.25$, </th>
    <th class="tg-hq8v">$15.19$</th>
  </tr>
</table>

<br>
</br>
$streams$ $correlation =$

<table  class="matrix" style="margin-top:-90px; margin-left:210px;" >

  <tr>
    <th class="tg-hq8v">$1$, </th>
    <th class="tg-hq8v">$0.607$, </th>
    <th class="tg-hq8v">$0.606$, </th>
    <th class="tg-hq8v">$0.613$, </th>
    <th class="tg-1wza">$0.608$</th>
  </tr>
  <tr>
    <td class="tg-hq8v">$0.607$, </td>
    <td class="tg-hq8v">$1$, </td>
    <td class="tg-hq8v">$0.613$, </td>
    <td class="tg-hq8v">$0.607$, </td>
    <td class="tg-1wza">$0.612$, </td>
  </tr>
  <tr>
    <td class="tg-hq8v">$0.606$, </td>
    <td class="tg-hq8v">$0.613$, </td>
    <td class="tg-hq8v">$1$, </td>
    <td class="tg-ymju">$0.610$, </td>
    <td class="tg-1wza">$0.613$, <br></td>
  </tr>
  <tr>
    <td class="tg-hq8v">$0.613$, <br></td>
    <td class="tg-hq8v">$0.607$, </td>
    <td class="tg-hq8v">$0.610$, </td>
    <td class="tg-hq8v">$1$, </td>
    <td class="tg-1wza">$0.609$</td>
  </tr>
  <tr>
    <td class="tg-1wza">$0.608$, </td>
    <td class="tg-1wza">$0.612$, </td>
    <td class="tg-1wza">$0.613$, </td>
    <td class="tg-1wza">$0.609$, </td>
    <td class="tg-1wza">$1$</td>
  </tr>
  
</table>
 </div>
</div>



This is the simplest way to construct such a portfolio. We make each pariwise correlation between assets equal to a given level `corr`. The important point is that the average of all the pairwise correlations should be equal to `corr`.

We'll create a helper function to calculate the pooled risk of a given number of return streams in the porfolio.


Next, we'll build our simulated dataset. We'll analyse return streams with risk levels in the range $1\%$ - $14\%$, for varying number of streams ranging from 1 to 20.  
We'll plot the risk levels for different average correlation, ranging from $0$ to $0.7$.


<style type="text/css">
.tg1  {border-collapse:collapse;border-spacing:0;border-color:#93a1a1;}
.tg1 td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#93a1a1;color:#002b36;background-color:#fffff8;}
.tg1 th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#93a1a1;color:#fffff8;background-color:#657b83;}
.tg1 .tg1-3ggi{background-color:#002b36;border-color:#fffff8;text-align:center;vertical-align:top}
.tg1 .tg1-5xqe{background-color:#000000;text-align:center;vertical-align:top}
.tg1 .tg1-c3ow{border-color:inherit;text-align:center;vertical-align:top}
.tg1 .tg1-wp8o{border-color:#000000;text-align:center;vertical-align:top}
.tg1 .tg1-67im{background-color:#002b36;color:#fffff8;border-color:#fffff8;text-align:center;vertical-align:top}
.tg1 .tg1-lduz{border-color:#002b36;text-align:center;vertical-align:top}
</style>
<table class="tg1" style="margin-left:60px;">
  <tr>
    <th class="tg1-5xqe"></th>
    <th class="tg1-3ggi">Correlation</th>
    <th class="tg1-3ggi">$0.0$</th>
    <th class="tg1-3ggi">$0.1$</th>
    <th class="tg1-3ggi">$0.2$</th>
    <th class="tg1-3ggi">$0.3$</th>
    <th class="tg1-3ggi">$0.4$</th>
    <th class="tg1-3ggi">$0.5$</th>
    <th class="tg1-3ggi">$0.6$</th>
    <th class="tg1-3ggi">$0.7$</th>
  </tr>
  <tr>
    <td class="tg1-67im">Risk level</td>
    <td class="tg1-wp8o">Num assets</td>
    <td class="tg1-wp8o"></td>
    <td class="tg1-wp8o"></td>
    <td class="tg1-wp8o"></td>
    <td class="tg1-wp8o"></td>
    <td class="tg1-wp8o"></td>
    <td class="tg1-wp8o"></td>
    <td class="tg1-wp8o"></td>
    <td class="tg1-wp8o"></td>
  </tr>
  <tr>
    <td class="tg1-67im" rowspan="20">$14$</td>
    <td class="tg1-c3ow">$1$</td>
    <td class="tg1-c3ow">$14.14$</td>
    <td class="tg1-c3ow">$13.95$</td>
    <td class="tg1-c3ow">$14.07$</td>
    <td class="tg1-wp8o">$13.87$</td>
    <td class="tg1-wp8o">$14.04$</td>
    <td class="tg1-wp8o">$14.17$</td>
    <td class="tg1-wp8o">$13.97$</td>
    <td class="tg1-wp8o">$14.08$</td>
  </tr>
  <tr>
    <td class="tg1-wp8o">$2$</td>
    <td class="tg1-wp8o">$9.97$</td>
    <td class="tg1-wp8o">$10.42$</td>
    <td class="tg1-wp8o">$10.73$</td>
    <td class="tg1-wp8o">$11.29$</td>
    <td class="tg1-wp8o">$11.76$</td>
    <td class="tg1-wp8o">$12.29$</td>
    <td class="tg1-wp8o">$12.46$</td>
    <td class="tg1-wp8o">$13.00$</td>
  </tr>
  <tr>
    <td class="tg1-wp8o">$3$</td>
    <td class="tg1-wp8o">$8.11$</td>
    <td class="tg1-wp8o">$8.88$</td>
    <td class="tg1-wp8o">$9.53$</td>
    <td class="tg1-wp8o">$10.16$</td>
    <td class="tg1-wp8o">$10.95$</td>
    <td class="tg1-wp8o">$11.61$</td>
    <td class="tg1-wp8o">$11.94$</td>
    <td class="tg1-wp8o">$12.06$</td>
  </tr>
  <tr>
    <td class="tg1-wp8o">$4$</td>
    <td class="tg1-wp8o">$6.99$</td>
    <td class="tg1-wp8o">$7.99$</td>
    <td class="tg1-wp8o">$8.86$</td>
    <td class="tg1-wp8o">$9.59$</td>
    <td class="tg1-wp8o">$10.47$<br></td>
    <td class="tg1-wp8o">$11.21$</td>
    <td class="tg1-wp8o">$11.66$</td>
    <td class="tg1-wp8o">$12.41$</td>
  </tr>
  <tr>
    <td class="tg1-wp8o">$5$</td>
    <td class="tg1-wp8o">$6.26$</td>
    <td class="tg1-wp8o">$7.40$</td>
    <td class="tg1-wp8o">$8.39$</td>
    <td class="tg1-wp8o">$9.25$</td>
    <td class="tg1-wp8o">$10.19$</td>
    <td class="tg1-wp8o">$10.97$</td>
    <td class="tg1-wp8o">$11.48$</td>
    <td class="tg1-wp8o">$12.31$</td>
  </tr>
  <tr>
    <td class="tg1-wp8o">$6$</td>
    <td class="tg1-wp8o">$5.72$</td>
    <td class="tg1-wp8o">$6.97$</td>
    <td class="tg1-wp8o">$8.09$</td>
    <td class="tg1-wp8o">$9.02$<br></td>
    <td class="tg1-wp8o">$10.01$</td>
    <td class="tg1-wp8o">$10.82$</td>
    <td class="tg1-wp8o">$11.37$</td>
    <td class="tg1-wp8o">$12.23$</td>
  </tr>
  <tr>
    <td class="tg1-lduz">$7$</td>
    <td class="tg1-lduz">$5.30$</td>
    <td class="tg1-lduz">$6.62$</td>
    <td class="tg1-lduz">$7.86$</td>
    <td class="tg1-lduz">$8.82$</td>
    <td class="tg1-lduz">$9.86$</td>
    <td class="tg1-lduz">$10.71$</td>
    <td class="tg1-lduz">$11.32$</td>
    <td class="tg1-lduz">$12.17$</td>
  </tr>
  <tr>
    <td class="tg1-lduz">$8$</td>
    <td class="tg1-lduz">$4.95$</td>
    <td class="tg1-lduz">$6.42$</td>
    <td class="tg1-lduz">$7.70$</td>
    <td class="tg1-lduz">$8.68$</td>
    <td class="tg1-lduz">$9.75$</td>
    <td class="tg1-lduz">$10.63$</td>
    <td class="tg1-lduz">$11.25$</td>
    <td class="tg1-lduz">$12.15$</td>
  </tr>
  <tr>
    <td class="tg1-lduz">$9$</td>
    <td class="tg1-lduz">$4.66$</td>
    <td class="tg1-lduz">$6.23$</td>
    <td class="tg1-lduz">$7.56$</td>
    <td class="tg1-lduz">$8.60$</td>
    <td class="tg1-lduz">$9.67$</td>
    <td class="tg1-lduz">$10.57$</td>
    <td class="tg1-lduz">$11.20$</td>
    <td class="tg1-lduz">$12.13$</td>
  </tr>
  <tr>
    <td class="tg1-lduz">$10$</td>
    <td class="tg1-lduz">$4.44$</td>
    <td class="tg1-lduz">$6.07$</td>
    <td class="tg1-lduz">$7.45$</td>
    <td class="tg1-lduz">$8.53$</td>
    <td class="tg1-lduz">$9.61$</td>
    <td class="tg1-lduz">$10.52$<br></td>
    <td class="tg1-lduz">$11.17$</td>
    <td class="tg1-lduz">$12.08$</td>
  </tr>
  <tr>
    <td class="tg1-lduz">$11$</td>
    <td class="tg1-lduz">$4.24$</td>
    <td class="tg1-lduz">$5.93$</td>
    <td class="tg1-lduz">$7.36$</td>
    <td class="tg1-lduz">$8.46$</td>
    <td class="tg1-lduz">$9.56$</td>
    <td class="tg1-lduz">$10.48$</td>
    <td class="tg1-lduz">$11.13$</td>
    <td class="tg1-lduz">$12.08$</td>
  </tr>
  <tr>
    <td class="tg1-lduz">$12$</td>
    <td class="tg1-lduz">$4.07$</td>
    <td class="tg1-lduz">$5.83$</td>
    <td class="tg1-lduz">$7.26$</td>
    <td class="tg1-lduz">$8.39$</td>
    <td class="tg1-lduz">$9.50$</td>
    <td class="tg1-lduz">$10.43$</td>
    <td class="tg1-lduz">$11.10$</td>
    <td class="tg1-lduz">$12.06$</td>
  </tr>
  <tr>
    <td class="tg1-lduz">$13$</td>
    <td class="tg1-lduz">$3.90$</td>
    <td class="tg1-lduz">$5.73$</td>
    <td class="tg1-lduz">$7.20$</td>
    <td class="tg1-lduz">$8.35$</td>
    <td class="tg1-lduz">$9.46$</td>
    <td class="tg1-lduz">$10.40$</td>
    <td class="tg1-lduz">$11.09$</td>
    <td class="tg1-lduz">$12.05$</td>
  </tr>
  <tr>
    <td class="tg1-lduz">$14$</td>
    <td class="tg1-lduz">$3.75$</td>
    <td class="tg1-lduz">$5.65$</td>
    <td class="tg1-lduz">$7.15$</td>
    <td class="tg1-lduz">$8.31$</td>
    <td class="tg1-lduz">$9.43$</td>
    <td class="tg1-lduz">$10.38$</td>
    <td class="tg1-lduz">$11.07$</td>
    <td class="tg1-lduz">$12.04$</td>
  </tr>
  <tr>
    <td class="tg1-lduz">$15$</td>
    <td class="tg1-lduz">$3.62$</td>
    <td class="tg1-lduz">$5.58$</td>
    <td class="tg1-lduz">$7.09$</td>
    <td class="tg1-lduz">$8.27$</td>
    <td class="tg1-lduz">$9.40$</td>
    <td class="tg1-lduz">$10.34$</td>
    <td class="tg1-lduz">$11.05$</td>
    <td class="tg1-lduz">$12.04$</td>
  </tr>
  <tr>
    <td class="tg1-lduz">$16$</td>
    <td class="tg1-lduz">$3.75$</td>
    <td class="tg1-lduz">$5.65$</td>
    <td class="tg1-lduz">$7.15$</td>
    <td class="tg1-lduz">$8.31$<br></td>
    <td class="tg1-lduz">$9.43$<br></td>
    <td class="tg1-lduz">$10.38$<br></td>
    <td class="tg1-lduz">$11.07$</td>
    <td class="tg1-lduz">$12.04$</td>
  </tr>
  <tr>
    <td class="tg1-lduz">$17$</td>
    <td class="tg1-lduz">$3.39$</td>
    <td class="tg1-lduz">$5.44$</td>
    <td class="tg1-lduz">$7.00$</td>
    <td class="tg1-lduz">$8.21$</td>
    <td class="tg1-lduz">$9.36$</td>
    <td class="tg1-lduz">$10.29$</td>
    <td class="tg1-lduz">$11.00$</td>
    <td class="tg1-lduz">$12.01$</td>
  </tr>
  <tr>
    <td class="tg1-lduz">$18$</td>
    <td class="tg1-lduz">$3.29$</td>
    <td class="tg1-lduz">$5.40$</td>
    <td class="tg1-lduz">$6.96$</td>
    <td class="tg1-lduz">$8.17$</td>
    <td class="tg1-lduz">$9.34$<br></td>
    <td class="tg1-lduz">$10.27$</td>
    <td class="tg1-lduz">$10.99$</td>
    <td class="tg1-lduz">$12.00$<br></td>
  </tr>
  <tr>
    <td class="tg1-lduz">$19$</td>
    <td class="tg1-lduz">$3.20$</td>
    <td class="tg1-lduz">$5.36$</td>
    <td class="tg1-lduz">$6.92$</td>
    <td class="tg1-lduz">$8.14$</td>
    <td class="tg1-lduz">$9.32$</td>
    <td class="tg1-lduz">$10.26$</td>
    <td class="tg1-lduz">$10.98$</td>
    <td class="tg1-lduz">$12.00$</td>
  </tr>
  <tr>
    <td class="tg1-lduz">$20$</td>
    <td class="tg1-lduz">$3.13$</td>
    <td class="tg1-lduz">$5.31$</td>
    <td class="tg1-lduz">$6.90$<br></td>
    <td class="tg1-lduz">$8.12$</td>
    <td class="tg1-lduz">$9.30$<br></td>
    <td class="tg1-lduz">$10.24$</td>
    <td class="tg1-lduz">$10.97$<br></td>
    <td class="tg1-lduz">$11.99$</td>
  </tr>
</table>

We can already see how portfolio risk _decreases_ as we add more assets, with sharper declines when we they have low correlation.

To recreate Dalio's chart (as seen in [this video](https://www.investopedia.com/video/play/ray-dalio-his-portfolio-holy-grail/)), we create a function that produces a plot given our simulated data and a risk level.

Let's see how diversification benefits a portfolio with assets that have a risk level of 10%.

<label for="img1" class="margin-toggle">⊕</label>
<input type="checkbox" id="img1" class="margin-toggle">
<span class="marginnote">Risk % by number of assets in the portfolio.</span>

<div id="altair-viz-62c9e8b76c2948579ccfe6988e4ce696"></div>
<script type="text/javascript">
  (function(spec, embedOpt){
    const outputDiv = document.getElementById("altair-viz-62c9e8b76c2948579ccfe6988e4ce696");
    const paths = {
      "vega": "https://cdn.jsdelivr.net/npm//vega@5?noext",
      "vega-lib": "https://cdn.jsdelivr.net/npm//vega-lib?noext",
      "vega-lite": "https://cdn.jsdelivr.net/npm//vega-lite@4.0.2?noext",
      "vega-embed": "https://cdn.jsdelivr.net/npm//vega-embed@6?noext",
    };

    function loadScript(lib) {
      return new Promise(function(resolve, reject) {
        var s = document.createElement('script');
        s.src = paths[lib];
        s.async = true;
        s.onload = () => resolve(paths[lib]);
        s.onerror = () => reject(`Error loading script: ${paths[lib]}`);
        document.getElementsByTagName("head")[0].appendChild(s);
      });
    }

    function showError(err) {
      outputDiv.innerHTML = `<div class="error" style="color:red;">${err}</div>`;
      throw err;
    }

    function displayChart(vegaEmbed) {
      vegaEmbed(outputDiv, spec, embedOpt)
        .catch(err => showError(`Javascript Error: ${err.message}<br>This usually means there's a typo in your chart specification. See the javascript console for the full traceback.`));
    }

    if(typeof define === "function" && define.amd) {
      requirejs.config({paths});
      require(["vega-embed"], displayChart, err => showError(`Error loading script: ${err.message}`));
    } else if (typeof vegaEmbed === "function") {
      displayChart(vegaEmbed);
    } else {
      loadScript("vega")
        .then(() => loadScript("vega-lite"))
        .then(() => loadScript("vega-embed"))
        .catch(showError)
        .then(() => displayChart(vegaEmbed));
    }
  })({"config": {"view": {"continuousWidth": 400, "continuousHeight": 300}}, "layer": [{"mark": "circle", "encoding": {"color": {"type": "nominal", "field": "correlation", "scale": {"scheme": "set2"}}, "opacity": {"value": 0}, "x": {"type": "quantitative", "axis": {"title": "Number of Assets"}, "field": "num_assets"}, "y": {"type": "quantitative", "axis": {"title": "Risk %"}, "field": "risk"}}, "height": 400, "selection": {"selector004": {"type": "single", "on": "mouseover", "fields": ["correlation"], "nearest": true}}, "width": 600}, {"mark": "line", "encoding": {"color": {"type": "nominal", "field": "correlation", "scale": {"scheme": "set2"}}, "size": {"condition": {"value": 1, "selection": {"not": "selector004"}}, "value": 3}, "tooltip": [{"type": "quantitative", "field": "correlation"}], "x": {"type": "quantitative", "axis": {"title": "Number of Assets"}, "field": "num_assets"}, "y": {"type": "quantitative", "axis": {"title": "Risk %"}, "field": "risk"}}}], "data": {"name": "data-654ea9b8ab29015260bc07f42dd80568"}, "$schema": "https://vega.github.io/schema/vega-lite/v4.0.2.json", "datasets": {"data-654ea9b8ab29015260bc07f42dd80568": [{"risk_level": 10, "num_assets": 1, "correlation": 0.0, "risk": 9.988874598041512}, {"risk_level": 10, "num_assets": 1, "correlation": 0.1, "risk": 10.066889536044009}, {"risk_level": 10, "num_assets": 1, "correlation": 0.2, "risk": 9.977686128775623}, {"risk_level": 10, "num_assets": 1, "correlation": 0.3, "risk": 10.238297023582492}, {"risk_level": 10, "num_assets": 1, "correlation": 0.4, "risk": 9.96511439064291}, {"risk_level": 10, "num_assets": 1, "correlation": 0.5, "risk": 9.956549665080548}, {"risk_level": 10, "num_assets": 1, "correlation": 0.6, "risk": 10.017771790633251}, {"risk_level": 10, "num_assets": 1, "correlation": 0.7, "risk": 9.970959330199557}, {"risk_level": 10, "num_assets": 2, "correlation": 0.0, "risk": 7.069624286589143}, {"risk_level": 10, "num_assets": 2, "correlation": 0.1, "risk": 7.484403831854324}, {"risk_level": 10, "num_assets": 2, "correlation": 0.2, "risk": 7.71457643359093}, {"risk_level": 10, "num_assets": 2, "correlation": 0.3, "risk": 8.13424066787885}, {"risk_level": 10, "num_assets": 2, "correlation": 0.4, "risk": 8.396130308848118}, {"risk_level": 10, "num_assets": 2, "correlation": 0.5, "risk": 8.598625671868138}, {"risk_level": 10, "num_assets": 2, "correlation": 0.6, "risk": 8.942893905769102}, {"risk_level": 10, "num_assets": 2, "correlation": 0.7, "risk": 9.153294769453483}, {"risk_level": 10, "num_assets": 3, "correlation": 0.0, "risk": 5.812492322989947}, {"risk_level": 10, "num_assets": 3, "correlation": 0.1, "risk": 6.381655665773931}, {"risk_level": 10, "num_assets": 3, "correlation": 0.2, "risk": 6.8276938034570325}, {"risk_level": 10, "num_assets": 3, "correlation": 0.3, "risk": 7.372087111671548}, {"risk_level": 10, "num_assets": 3, "correlation": 0.4, "risk": 7.751134151202533}, {"risk_level": 10, "num_assets": 3, "correlation": 0.5, "risk": 8.12999913417687}, {"risk_level": 10, "num_assets": 3, "correlation": 0.6, "risk": 8.52797862529422}, {"risk_level": 10, "num_assets": 3, "correlation": 0.7, "risk": 8.894694409671505}, {"risk_level": 10, "num_assets": 4, "correlation": 0.0, "risk": 5.015060723231312}, {"risk_level": 10, "num_assets": 4, "correlation": 0.1, "risk": 5.742681666377761}, {"risk_level": 10, "num_assets": 4, "correlation": 0.2, "risk": 6.27454899529484}, {"risk_level": 10, "num_assets": 4, "correlation": 0.3, "risk": 6.954382564645678}, {"risk_level": 10, "num_assets": 4, "correlation": 0.4, "risk": 7.414982902770195}, {"risk_level": 10, "num_assets": 4, "correlation": 0.5, "risk": 7.881528826127797}, {"risk_level": 10, "num_assets": 4, "correlation": 0.6, "risk": 8.338786169467706}, {"risk_level": 10, "num_assets": 4, "correlation": 0.7, "risk": 8.7702347928734}, {"risk_level": 10, "num_assets": 5, "correlation": 0.0, "risk": 4.503901084763166}, {"risk_level": 10, "num_assets": 5, "correlation": 0.1, "risk": 5.322640160193844}, {"risk_level": 10, "num_assets": 5, "correlation": 0.2, "risk": 5.959644140161698}, {"risk_level": 10, "num_assets": 5, "correlation": 0.3, "risk": 6.662458923546909}, {"risk_level": 10, "num_assets": 5, "correlation": 0.4, "risk": 7.190384583185708}, {"risk_level": 10, "num_assets": 5, "correlation": 0.5, "risk": 7.707624605125377}, {"risk_level": 10, "num_assets": 5, "correlation": 0.6, "risk": 8.22507385452154}, {"risk_level": 10, "num_assets": 5, "correlation": 0.7, "risk": 8.686678410730348}, {"risk_level": 10, "num_assets": 6, "correlation": 0.0, "risk": 4.080931781229849}, {"risk_level": 10, "num_assets": 6, "correlation": 0.1, "risk": 5.027402272489107}, {"risk_level": 10, "num_assets": 6, "correlation": 0.2, "risk": 5.733374634975609}, {"risk_level": 10, "num_assets": 6, "correlation": 0.3, "risk": 6.5124973505972745}, {"risk_level": 10, "num_assets": 6, "correlation": 0.4, "risk": 7.043390723369565}, {"risk_level": 10, "num_assets": 6, "correlation": 0.5, "risk": 7.611410025976708}, {"risk_level": 10, "num_assets": 6, "correlation": 0.6, "risk": 8.136715681555751}, {"risk_level": 10, "num_assets": 6, "correlation": 0.7, "risk": 8.652095170592714}, {"risk_level": 10, "num_assets": 7, "correlation": 0.0, "risk": 3.7559290501571816}, {"risk_level": 10, "num_assets": 7, "correlation": 0.1, "risk": 4.7905931751981115}, {"risk_level": 10, "num_assets": 7, "correlation": 0.2, "risk": 5.586166701460125}, {"risk_level": 10, "num_assets": 7, "correlation": 0.3, "risk": 6.3796495181822985}, {"risk_level": 10, "num_assets": 7, "correlation": 0.4, "risk": 6.939940479199481}, {"risk_level": 10, "num_assets": 7, "correlation": 0.5, "risk": 7.525964962159929}, {"risk_level": 10, "num_assets": 7, "correlation": 0.6, "risk": 8.090047317878604}, {"risk_level": 10, "num_assets": 7, "correlation": 0.7, "risk": 8.589030846790688}, {"risk_level": 10, "num_assets": 8, "correlation": 0.0, "risk": 3.5209238219039465}, {"risk_level": 10, "num_assets": 8, "correlation": 0.1, "risk": 4.621799536355236}, {"risk_level": 10, "num_assets": 8, "correlation": 0.2, "risk": 5.470704126624215}, {"risk_level": 10, "num_assets": 8, "correlation": 0.3, "risk": 6.265974927485572}, {"risk_level": 10, "num_assets": 8, "correlation": 0.4, "risk": 6.866651862945254}, {"risk_level": 10, "num_assets": 8, "correlation": 0.5, "risk": 7.47084194353405}, {"risk_level": 10, "num_assets": 8, "correlation": 0.6, "risk": 8.040815609238301}, {"risk_level": 10, "num_assets": 8, "correlation": 0.7, "risk": 8.556504868793002}, {"risk_level": 10, "num_assets": 9, "correlation": 0.0, "risk": 3.3217042521060813}, {"risk_level": 10, "num_assets": 9, "correlation": 0.1, "risk": 4.48160765076608}, {"risk_level": 10, "num_assets": 9, "correlation": 0.2, "risk": 5.366940943078688}, {"risk_level": 10, "num_assets": 9, "correlation": 0.3, "risk": 6.193538243186635}, {"risk_level": 10, "num_assets": 9, "correlation": 0.4, "risk": 6.8044364199468985}, {"risk_level": 10, "num_assets": 9, "correlation": 0.5, "risk": 7.425386053665795}, {"risk_level": 10, "num_assets": 9, "correlation": 0.6, "risk": 8.02354591428385}, {"risk_level": 10, "num_assets": 9, "correlation": 0.7, "risk": 8.536671526760736}, {"risk_level": 10, "num_assets": 10, "correlation": 0.0, "risk": 3.1567119306035463}, {"risk_level": 10, "num_assets": 10, "correlation": 0.1, "risk": 4.365474872000492}, {"risk_level": 10, "num_assets": 10, "correlation": 0.2, "risk": 5.281784387740449}, {"risk_level": 10, "num_assets": 10, "correlation": 0.3, "risk": 6.130867318188108}, {"risk_level": 10, "num_assets": 10, "correlation": 0.4, "risk": 6.756435420972388}, {"risk_level": 10, "num_assets": 10, "correlation": 0.5, "risk": 7.376794106313596}, {"risk_level": 10, "num_assets": 10, "correlation": 0.6, "risk": 8.005714348837017}, {"risk_level": 10, "num_assets": 10, "correlation": 0.7, "risk": 8.524254175600198}, {"risk_level": 10, "num_assets": 11, "correlation": 0.0, "risk": 3.0130610946136556}, {"risk_level": 10, "num_assets": 11, "correlation": 0.1, "risk": 4.258148879132876}, {"risk_level": 10, "num_assets": 11, "correlation": 0.2, "risk": 5.205746451923322}, {"risk_level": 10, "num_assets": 11, "correlation": 0.3, "risk": 6.065473976197256}, {"risk_level": 10, "num_assets": 11, "correlation": 0.4, "risk": 6.7132917508503205}, {"risk_level": 10, "num_assets": 11, "correlation": 0.5, "risk": 7.345819977818375}, {"risk_level": 10, "num_assets": 11, "correlation": 0.6, "risk": 7.981123111443838}, {"risk_level": 10, "num_assets": 11, "correlation": 0.7, "risk": 8.507237531697914}, {"risk_level": 10, "num_assets": 12, "correlation": 0.0, "risk": 2.8873796661841302}, {"risk_level": 10, "num_assets": 12, "correlation": 0.1, "risk": 4.177522979380948}, {"risk_level": 10, "num_assets": 12, "correlation": 0.2, "risk": 5.139216771945179}, {"risk_level": 10, "num_assets": 12, "correlation": 0.3, "risk": 6.018566564409335}, {"risk_level": 10, "num_assets": 12, "correlation": 0.4, "risk": 6.680031656315569}, {"risk_level": 10, "num_assets": 12, "correlation": 0.5, "risk": 7.3168233134099845}, {"risk_level": 10, "num_assets": 12, "correlation": 0.6, "risk": 7.961891255916454}, {"risk_level": 10, "num_assets": 12, "correlation": 0.7, "risk": 8.491774519632665}, {"risk_level": 10, "num_assets": 13, "correlation": 0.0, "risk": 2.764135313390701}, {"risk_level": 10, "num_assets": 13, "correlation": 0.1, "risk": 4.106413983035421}, {"risk_level": 10, "num_assets": 13, "correlation": 0.2, "risk": 5.09243866410117}, {"risk_level": 10, "num_assets": 13, "correlation": 0.3, "risk": 5.972793133158227}, {"risk_level": 10, "num_assets": 13, "correlation": 0.4, "risk": 6.642530495932471}, {"risk_level": 10, "num_assets": 13, "correlation": 0.5, "risk": 7.306908988328294}, {"risk_level": 10, "num_assets": 13, "correlation": 0.6, "risk": 7.946378979368648}, {"risk_level": 10, "num_assets": 13, "correlation": 0.7, "risk": 8.477244672961966}, {"risk_level": 10, "num_assets": 14, "correlation": 0.0, "risk": 2.671654968599471}, {"risk_level": 10, "num_assets": 14, "correlation": 0.1, "risk": 4.041841420495182}, {"risk_level": 10, "num_assets": 14, "correlation": 0.2, "risk": 5.067300680583676}, {"risk_level": 10, "num_assets": 14, "correlation": 0.3, "risk": 5.943159215257512}, {"risk_level": 10, "num_assets": 14, "correlation": 0.4, "risk": 6.616607437649344}, {"risk_level": 10, "num_assets": 14, "correlation": 0.5, "risk": 7.284738724287593}, {"risk_level": 10, "num_assets": 14, "correlation": 0.6, "risk": 7.924510302821753}, {"risk_level": 10, "num_assets": 14, "correlation": 0.7, "risk": 8.468827933211164}, {"risk_level": 10, "num_assets": 15, "correlation": 0.0, "risk": 2.583072761308214}, {"risk_level": 10, "num_assets": 15, "correlation": 0.1, "risk": 3.9856919992207964}, {"risk_level": 10, "num_assets": 15, "correlation": 0.2, "risk": 5.03651055844854}, {"risk_level": 10, "num_assets": 15, "correlation": 0.3, "risk": 5.9158673048493}, {"risk_level": 10, "num_assets": 15, "correlation": 0.4, "risk": 6.591347608977625}, {"risk_level": 10, "num_assets": 15, "correlation": 0.5, "risk": 7.270793207332615}, {"risk_level": 10, "num_assets": 15, "correlation": 0.6, "risk": 7.914806909737165}, {"risk_level": 10, "num_assets": 15, "correlation": 0.7, "risk": 8.46116642920399}, {"risk_level": 10, "num_assets": 16, "correlation": 0.0, "risk": 2.505774242563774}, {"risk_level": 10, "num_assets": 16, "correlation": 0.1, "risk": 3.9217769114927385}, {"risk_level": 10, "num_assets": 16, "correlation": 0.2, "risk": 5.00595662318927}, {"risk_level": 10, "num_assets": 16, "correlation": 0.3, "risk": 5.890821056858878}, {"risk_level": 10, "num_assets": 16, "correlation": 0.4, "risk": 6.575654506880724}, {"risk_level": 10, "num_assets": 16, "correlation": 0.5, "risk": 7.252791491175006}, {"risk_level": 10, "num_assets": 16, "correlation": 0.6, "risk": 7.901523992655929}, {"risk_level": 10, "num_assets": 16, "correlation": 0.7, "risk": 8.450648633224345}, {"risk_level": 10, "num_assets": 17, "correlation": 0.0, "risk": 2.437052927857563}, {"risk_level": 10, "num_assets": 17, "correlation": 0.1, "risk": 3.88570912715349}, {"risk_level": 10, "num_assets": 17, "correlation": 0.2, "risk": 4.97640250232958}, {"risk_level": 10, "num_assets": 17, "correlation": 0.3, "risk": 5.8680843685405275}, {"risk_level": 10, "num_assets": 17, "correlation": 0.4, "risk": 6.547186518172158}, {"risk_level": 10, "num_assets": 17, "correlation": 0.5, "risk": 7.236600867911784}, {"risk_level": 10, "num_assets": 17, "correlation": 0.6, "risk": 7.894967516107746}, {"risk_level": 10, "num_assets": 17, "correlation": 0.7, "risk": 8.446427182701727}, {"risk_level": 10, "num_assets": 18, "correlation": 0.0, "risk": 2.3753781163983607}, {"risk_level": 10, "num_assets": 18, "correlation": 0.1, "risk": 3.849382600805155}, {"risk_level": 10, "num_assets": 18, "correlation": 0.2, "risk": 4.956903577276406}, {"risk_level": 10, "num_assets": 18, "correlation": 0.3, "risk": 5.85057589155876}, {"risk_level": 10, "num_assets": 18, "correlation": 0.4, "risk": 6.52571418098101}, {"risk_level": 10, "num_assets": 18, "correlation": 0.5, "risk": 7.232532654307521}, {"risk_level": 10, "num_assets": 18, "correlation": 0.6, "risk": 7.894136347354723}, {"risk_level": 10, "num_assets": 18, "correlation": 0.7, "risk": 8.44068263102865}, {"risk_level": 10, "num_assets": 19, "correlation": 0.0, "risk": 2.3130992440658327}, {"risk_level": 10, "num_assets": 19, "correlation": 0.1, "risk": 3.8146657356125204}, {"risk_level": 10, "num_assets": 19, "correlation": 0.2, "risk": 4.931422011015554}, {"risk_level": 10, "num_assets": 19, "correlation": 0.3, "risk": 5.844293815024879}, {"risk_level": 10, "num_assets": 19, "correlation": 0.4, "risk": 6.516342316223013}, {"risk_level": 10, "num_assets": 19, "correlation": 0.5, "risk": 7.223818266627368}, {"risk_level": 10, "num_assets": 19, "correlation": 0.6, "risk": 7.8847964270857585}, {"risk_level": 10, "num_assets": 19, "correlation": 0.7, "risk": 8.43523335682978}, {"risk_level": 10, "num_assets": 20, "correlation": 0.0, "risk": 2.2593578498432185}, {"risk_level": 10, "num_assets": 20, "correlation": 0.1, "risk": 3.7853048094503223}, {"risk_level": 10, "num_assets": 20, "correlation": 0.2, "risk": 4.91259866052523}, {"risk_level": 10, "num_assets": 20, "correlation": 0.3, "risk": 5.828429042274702}, {"risk_level": 10, "num_assets": 20, "correlation": 0.4, "risk": 6.508034002078632}, {"risk_level": 10, "num_assets": 20, "correlation": 0.5, "risk": 7.214790861567079}, {"risk_level": 10, "num_assets": 20, "correlation": 0.6, "risk": 7.883610499854245}, {"risk_level": 10, "num_assets": 20, "correlation": 0.7, "risk": 8.432613065898623}]}}, {"mode": "vega-lite"});
</script>



A highly correlated portfolio _does not_ benefit much from increased diversification. We get diminishing returns by adding highly correlated assets beyond 3 or 4.  
In contrast, we can _halve_ the risk by adding just 6 or 7 uncorrelated (or more realistically, weakly correlated) assets to a portfolio.

Let's plot the risk levels for a portfolio with returns streams with 7% risk.

<label for="img1" class="margin-toggle">⊕</label>
<input type="checkbox" id="img1" class="margin-toggle">
<span class="marginnote">Risk % by number of assets in the portfolio.</span>


<div id="altair-viz-def488cf99c04fe9b15e4e19cdaccbb7"></div>
<script type="text/javascript">
  (function(spec, embedOpt){
    const outputDiv = document.getElementById("altair-viz-def488cf99c04fe9b15e4e19cdaccbb7");
    const paths = {
      "vega": "https://cdn.jsdelivr.net/npm//vega@5?noext",
      "vega-lib": "https://cdn.jsdelivr.net/npm//vega-lib?noext",
      "vega-lite": "https://cdn.jsdelivr.net/npm//vega-lite@4.0.2?noext",
      "vega-embed": "https://cdn.jsdelivr.net/npm//vega-embed@6?noext",
    };

    function loadScript(lib) {
      return new Promise(function(resolve, reject) {
        var s = document.createElement('script');
        s.src = paths[lib];
        s.async = true;
        s.onload = () => resolve(paths[lib]);
        s.onerror = () => reject(`Error loading script: ${paths[lib]}`);
        document.getElementsByTagName("head")[0].appendChild(s);
      });
    }

    function showError(err) {
      outputDiv.innerHTML = `<div class="error" style="color:red;">${err}</div>`;
      throw err;
    }

    function displayChart(vegaEmbed) {
      vegaEmbed(outputDiv, spec, embedOpt)
        .catch(err => showError(`Javascript Error: ${err.message}<br>This usually means there's a typo in your chart specification. See the javascript console for the full traceback.`));
    }

    if(typeof define === "function" && define.amd) {
      requirejs.config({paths});
      require(["vega-embed"], displayChart, err => showError(`Error loading script: ${err.message}`));
    } else if (typeof vegaEmbed === "function") {
      displayChart(vegaEmbed);
    } else {
      loadScript("vega")
        .then(() => loadScript("vega-lite"))
        .then(() => loadScript("vega-embed"))
        .catch(showError)
        .then(() => displayChart(vegaEmbed));
    }
  })({"config": {"view": {"continuousWidth": 400, "continuousHeight": 300}}, "layer": [{"mark": "circle", "encoding": {"color": {"type": "nominal", "field": "correlation", "scale": {"scheme": "set2"}}, "opacity": {"value": 0}, "x": {"type": "quantitative", "axis": {"title": "Number of Assets"}, "field": "num_assets"}, "y": {"type": "quantitative", "axis": {"title": "Risk %"}, "field": "risk"}}, "height": 400, "selection": {"selector005": {"type": "single", "on": "mouseover", "fields": ["correlation"], "nearest": true}}, "width": 600}, {"mark": "line", "encoding": {"color": {"type": "nominal", "field": "correlation", "scale": {"scheme": "set2"}}, "size": {"condition": {"value": 1, "selection": {"not": "selector005"}}, "value": 3}, "tooltip": [{"type": "quantitative", "field": "correlation"}], "x": {"type": "quantitative", "axis": {"title": "Number of Assets"}, "field": "num_assets"}, "y": {"type": "quantitative", "axis": {"title": "Risk %"}, "field": "risk"}}}], "data": {"name": "data-08cc901433f19e30375166b9b92d3027"}, "$schema": "https://vega.github.io/schema/vega-lite/v4.0.2.json", "datasets": {"data-08cc901433f19e30375166b9b92d3027": [{"risk_level": 7, "num_assets": 1, "correlation": 0.0, "risk": 7.079464105795791}, {"risk_level": 7, "num_assets": 1, "correlation": 0.1, "risk": 7.001969785463717}, {"risk_level": 7, "num_assets": 1, "correlation": 0.2, "risk": 7.114235218268703}, {"risk_level": 7, "num_assets": 1, "correlation": 0.3, "risk": 7.0585983702203015}, {"risk_level": 7, "num_assets": 1, "correlation": 0.4, "risk": 7.046231201424136}, {"risk_level": 7, "num_assets": 1, "correlation": 0.5, "risk": 7.040076240929961}, {"risk_level": 7, "num_assets": 1, "correlation": 0.6, "risk": 6.965753861122921}, {"risk_level": 7, "num_assets": 1, "correlation": 0.7, "risk": 6.994230272683885}, {"risk_level": 7, "num_assets": 2, "correlation": 0.0, "risk": 4.991670968456456}, {"risk_level": 7, "num_assets": 2, "correlation": 0.1, "risk": 5.160070148653499}, {"risk_level": 7, "num_assets": 2, "correlation": 0.2, "risk": 5.499048036146301}, {"risk_level": 7, "num_assets": 2, "correlation": 0.3, "risk": 5.689172805125513}, {"risk_level": 7, "num_assets": 2, "correlation": 0.4, "risk": 5.860228617837361}, {"risk_level": 7, "num_assets": 2, "correlation": 0.5, "risk": 6.109868811065723}, {"risk_level": 7, "num_assets": 2, "correlation": 0.6, "risk": 6.2492612340203415}, {"risk_level": 7, "num_assets": 2, "correlation": 0.7, "risk": 6.438541416986078}, {"risk_level": 7, "num_assets": 3, "correlation": 0.0, "risk": 4.0707541325588945}, {"risk_level": 7, "num_assets": 3, "correlation": 0.1, "risk": 4.415155405157742}, {"risk_level": 7, "num_assets": 3, "correlation": 0.2, "risk": 4.854858434604212}, {"risk_level": 7, "num_assets": 3, "correlation": 0.3, "risk": 5.146359014554256}, {"risk_level": 7, "num_assets": 3, "correlation": 0.4, "risk": 5.422269317773321}, {"risk_level": 7, "num_assets": 3, "correlation": 0.5, "risk": 5.7270517955416445}, {"risk_level": 7, "num_assets": 3, "correlation": 0.6, "risk": 6.0021082897243945}, {"risk_level": 7, "num_assets": 3, "correlation": 0.7, "risk": 6.238912677114608}, {"risk_level": 7, "num_assets": 4, "correlation": 0.0, "risk": 3.506562262124998}, {"risk_level": 7, "num_assets": 4, "correlation": 0.1, "risk": 3.978963395196149}, {"risk_level": 7, "num_assets": 4, "correlation": 0.2, "risk": 4.501134027838279}, {"risk_level": 7, "num_assets": 4, "correlation": 0.3, "risk": 4.857883697672174}, {"risk_level": 7, "num_assets": 4, "correlation": 0.4, "risk": 5.207047232966782}, {"risk_level": 7, "num_assets": 4, "correlation": 0.5, "risk": 5.577187025388975}, {"risk_level": 7, "num_assets": 4, "correlation": 0.6, "risk": 5.864116970162001}, {"risk_level": 7, "num_assets": 4, "correlation": 0.7, "risk": 6.14025566433462}, {"risk_level": 7, "num_assets": 5, "correlation": 0.0, "risk": 3.1570848790753927}, {"risk_level": 7, "num_assets": 5, "correlation": 0.1, "risk": 3.6917971091833373}, {"risk_level": 7, "num_assets": 5, "correlation": 0.2, "risk": 4.2379028264605605}, {"risk_level": 7, "num_assets": 5, "correlation": 0.3, "risk": 4.67041123639482}, {"risk_level": 7, "num_assets": 5, "correlation": 0.4, "risk": 5.077144491000972}, {"risk_level": 7, "num_assets": 5, "correlation": 0.5, "risk": 5.468483812766686}, {"risk_level": 7, "num_assets": 5, "correlation": 0.6, "risk": 5.786309437605462}, {"risk_level": 7, "num_assets": 5, "correlation": 0.7, "risk": 6.0848191310303354}, {"risk_level": 7, "num_assets": 6, "correlation": 0.0, "risk": 2.8945339902477785}, {"risk_level": 7, "num_assets": 6, "correlation": 0.1, "risk": 3.495203563804925}, {"risk_level": 7, "num_assets": 6, "correlation": 0.2, "risk": 4.082387523047231}, {"risk_level": 7, "num_assets": 6, "correlation": 0.3, "risk": 4.535551393455977}, {"risk_level": 7, "num_assets": 6, "correlation": 0.4, "risk": 4.967789346241509}, {"risk_level": 7, "num_assets": 6, "correlation": 0.5, "risk": 5.389365785318906}, {"risk_level": 7, "num_assets": 6, "correlation": 0.6, "risk": 5.729078684873262}, {"risk_level": 7, "num_assets": 6, "correlation": 0.7, "risk": 6.0520135450705075}, {"risk_level": 7, "num_assets": 7, "correlation": 0.0, "risk": 2.6781400679348035}, {"risk_level": 7, "num_assets": 7, "correlation": 0.1, "risk": 3.3465721555478423}, {"risk_level": 7, "num_assets": 7, "correlation": 0.2, "risk": 3.9648217863636566}, {"risk_level": 7, "num_assets": 7, "correlation": 0.3, "risk": 4.439439774701661}, {"risk_level": 7, "num_assets": 7, "correlation": 0.4, "risk": 4.901545119139352}, {"risk_level": 7, "num_assets": 7, "correlation": 0.5, "risk": 5.338140700826717}, {"risk_level": 7, "num_assets": 7, "correlation": 0.6, "risk": 5.687652723951773}, {"risk_level": 7, "num_assets": 7, "correlation": 0.7, "risk": 6.019669440158399}, {"risk_level": 7, "num_assets": 8, "correlation": 0.0, "risk": 2.4969002497696002}, {"risk_level": 7, "num_assets": 8, "correlation": 0.1, "risk": 3.226204303401534}, {"risk_level": 7, "num_assets": 8, "correlation": 0.2, "risk": 3.8632303404428687}, {"risk_level": 7, "num_assets": 8, "correlation": 0.3, "risk": 4.360880200634228}, {"risk_level": 7, "num_assets": 8, "correlation": 0.4, "risk": 4.847746296064062}, {"risk_level": 7, "num_assets": 8, "correlation": 0.5, "risk": 5.293392185711091}, {"risk_level": 7, "num_assets": 8, "correlation": 0.6, "risk": 5.659301212009281}, {"risk_level": 7, "num_assets": 8, "correlation": 0.7, "risk": 6.009036551188073}, {"risk_level": 7, "num_assets": 9, "correlation": 0.0, "risk": 2.3481716741060605}, {"risk_level": 7, "num_assets": 9, "correlation": 0.1, "risk": 3.1250500624699593}, {"risk_level": 7, "num_assets": 9, "correlation": 0.2, "risk": 3.7891445380870894}, {"risk_level": 7, "num_assets": 9, "correlation": 0.3, "risk": 4.310615118725745}, {"risk_level": 7, "num_assets": 9, "correlation": 0.4, "risk": 4.813802024736416}, {"risk_level": 7, "num_assets": 9, "correlation": 0.5, "risk": 5.259202157963434}, {"risk_level": 7, "num_assets": 9, "correlation": 0.6, "risk": 5.6274551589771855}, {"risk_level": 7, "num_assets": 9, "correlation": 0.7, "risk": 5.988810099446441}, {"risk_level": 7, "num_assets": 10, "correlation": 0.0, "risk": 2.233287425532112}, {"risk_level": 7, "num_assets": 10, "correlation": 0.1, "risk": 3.0377656177058094}, {"risk_level": 7, "num_assets": 10, "correlation": 0.2, "risk": 3.717278667331596}, {"risk_level": 7, "num_assets": 10, "correlation": 0.3, "risk": 4.261765478983779}, {"risk_level": 7, "num_assets": 10, "correlation": 0.4, "risk": 4.775432633435739}, {"risk_level": 7, "num_assets": 10, "correlation": 0.5, "risk": 5.230720733610845}, {"risk_level": 7, "num_assets": 10, "correlation": 0.6, "risk": 5.600194178280576}, {"risk_level": 7, "num_assets": 10, "correlation": 0.7, "risk": 5.979569418566313}, {"risk_level": 7, "num_assets": 11, "correlation": 0.0, "risk": 2.1296021343107787}, {"risk_level": 7, "num_assets": 11, "correlation": 0.1, "risk": 2.9676640885533203}, {"risk_level": 7, "num_assets": 11, "correlation": 0.2, "risk": 3.66283425684514}, {"risk_level": 7, "num_assets": 11, "correlation": 0.3, "risk": 4.21546818706827}, {"risk_level": 7, "num_assets": 11, "correlation": 0.4, "risk": 4.754031672979908}, {"risk_level": 7, "num_assets": 11, "correlation": 0.5, "risk": 5.209105395487776}, {"risk_level": 7, "num_assets": 11, "correlation": 0.6, "risk": 5.581041786179439}, {"risk_level": 7, "num_assets": 11, "correlation": 0.7, "risk": 5.969248715404031}, {"risk_level": 7, "num_assets": 12, "correlation": 0.0, "risk": 2.033635098726067}, {"risk_level": 7, "num_assets": 12, "correlation": 0.1, "risk": 2.9128869052697874}, {"risk_level": 7, "num_assets": 12, "correlation": 0.2, "risk": 3.6215183883438673}, {"risk_level": 7, "num_assets": 12, "correlation": 0.3, "risk": 4.186448639782271}, {"risk_level": 7, "num_assets": 12, "correlation": 0.4, "risk": 4.728842379046725}, {"risk_level": 7, "num_assets": 12, "correlation": 0.5, "risk": 5.19000658749401}, {"risk_level": 7, "num_assets": 12, "correlation": 0.6, "risk": 5.567982650143887}, {"risk_level": 7, "num_assets": 12, "correlation": 0.7, "risk": 5.963569182635211}, {"risk_level": 7, "num_assets": 13, "correlation": 0.0, "risk": 1.9507716069466354}, {"risk_level": 7, "num_assets": 13, "correlation": 0.1, "risk": 2.8695648994209653}, {"risk_level": 7, "num_assets": 13, "correlation": 0.2, "risk": 3.5936042653736506}, {"risk_level": 7, "num_assets": 13, "correlation": 0.3, "risk": 4.159165234095877}, {"risk_level": 7, "num_assets": 13, "correlation": 0.4, "risk": 4.708090508205426}, {"risk_level": 7, "num_assets": 13, "correlation": 0.5, "risk": 5.175388998298038}, {"risk_level": 7, "num_assets": 13, "correlation": 0.6, "risk": 5.55460638969435}, {"risk_level": 7, "num_assets": 13, "correlation": 0.7, "risk": 5.9567317185433994}, {"risk_level": 7, "num_assets": 14, "correlation": 0.0, "risk": 1.885468444262976}, {"risk_level": 7, "num_assets": 14, "correlation": 0.1, "risk": 2.8303763022484305}, {"risk_level": 7, "num_assets": 14, "correlation": 0.2, "risk": 3.5700674841567266}, {"risk_level": 7, "num_assets": 14, "correlation": 0.3, "risk": 4.145070483067351}, {"risk_level": 7, "num_assets": 14, "correlation": 0.4, "risk": 4.6900039871428225}, {"risk_level": 7, "num_assets": 14, "correlation": 0.5, "risk": 5.158491875728092}, {"risk_level": 7, "num_assets": 14, "correlation": 0.6, "risk": 5.543921179383785}, {"risk_level": 7, "num_assets": 14, "correlation": 0.7, "risk": 5.949810338182597}, {"risk_level": 7, "num_assets": 15, "correlation": 0.0, "risk": 1.8152425509032288}, {"risk_level": 7, "num_assets": 15, "correlation": 0.1, "risk": 2.7930824071560845}, {"risk_level": 7, "num_assets": 15, "correlation": 0.2, "risk": 3.5417440718585547}, {"risk_level": 7, "num_assets": 15, "correlation": 0.3, "risk": 4.1198330851276594}, {"risk_level": 7, "num_assets": 15, "correlation": 0.4, "risk": 4.675721786377278}, {"risk_level": 7, "num_assets": 15, "correlation": 0.5, "risk": 5.149742481371259}, {"risk_level": 7, "num_assets": 15, "correlation": 0.6, "risk": 5.534458110521681}, {"risk_level": 7, "num_assets": 15, "correlation": 0.7, "risk": 5.94810808670645}, {"risk_level": 7, "num_assets": 16, "correlation": 0.0, "risk": 1.7570516919356627}, {"risk_level": 7, "num_assets": 16, "correlation": 0.1, "risk": 2.7571036725576814}, {"risk_level": 7, "num_assets": 16, "correlation": 0.2, "risk": 3.521188019985128}, {"risk_level": 7, "num_assets": 16, "correlation": 0.3, "risk": 4.100962909664397}, {"risk_level": 7, "num_assets": 16, "correlation": 0.4, "risk": 4.666949443020912}, {"risk_level": 7, "num_assets": 16, "correlation": 0.5, "risk": 5.13904163298413}, {"risk_level": 7, "num_assets": 16, "correlation": 0.6, "risk": 5.520196189827978}, {"risk_level": 7, "num_assets": 16, "correlation": 0.7, "risk": 5.941219995350202}, {"risk_level": 7, "num_assets": 17, "correlation": 0.0, "risk": 1.7039115682012602}, {"risk_level": 7, "num_assets": 17, "correlation": 0.1, "risk": 2.7282850380444215}, {"risk_level": 7, "num_assets": 17, "correlation": 0.2, "risk": 3.5066641365339764}, {"risk_level": 7, "num_assets": 17, "correlation": 0.3, "risk": 4.08345214676821}, {"risk_level": 7, "num_assets": 17, "correlation": 0.4, "risk": 4.650851636071404}, {"risk_level": 7, "num_assets": 17, "correlation": 0.5, "risk": 5.126467465379457}, {"risk_level": 7, "num_assets": 17, "correlation": 0.6, "risk": 5.5094202401111065}, {"risk_level": 7, "num_assets": 17, "correlation": 0.7, "risk": 5.936855748278328}, {"risk_level": 7, "num_assets": 18, "correlation": 0.0, "risk": 1.6527586454416792}, {"risk_level": 7, "num_assets": 18, "correlation": 0.1, "risk": 2.710077089293083}, {"risk_level": 7, "num_assets": 18, "correlation": 0.2, "risk": 3.490554726656233}, {"risk_level": 7, "num_assets": 18, "correlation": 0.3, "risk": 4.069826627327732}, {"risk_level": 7, "num_assets": 18, "correlation": 0.4, "risk": 4.640756076692054}, {"risk_level": 7, "num_assets": 18, "correlation": 0.5, "risk": 5.124269776721228}, {"risk_level": 7, "num_assets": 18, "correlation": 0.6, "risk": 5.501914217374313}, {"risk_level": 7, "num_assets": 18, "correlation": 0.7, "risk": 5.933292227106985}, {"risk_level": 7, "num_assets": 19, "correlation": 0.0, "risk": 1.6104422480341252}, {"risk_level": 7, "num_assets": 19, "correlation": 0.1, "risk": 2.6833242690264765}, {"risk_level": 7, "num_assets": 19, "correlation": 0.2, "risk": 3.472550419283725}, {"risk_level": 7, "num_assets": 19, "correlation": 0.3, "risk": 4.052498051624683}, {"risk_level": 7, "num_assets": 19, "correlation": 0.4, "risk": 4.637124667292083}, {"risk_level": 7, "num_assets": 19, "correlation": 0.5, "risk": 5.120941555952021}, {"risk_level": 7, "num_assets": 19, "correlation": 0.6, "risk": 5.501427890177202}, {"risk_level": 7, "num_assets": 19, "correlation": 0.7, "risk": 5.929188400043958}, {"risk_level": 7, "num_assets": 20, "correlation": 0.0, "risk": 1.5720139795487094}, {"risk_level": 7, "num_assets": 20, "correlation": 0.1, "risk": 2.661200400258242}, {"risk_level": 7, "num_assets": 20, "correlation": 0.2, "risk": 3.4595202718558524}, {"risk_level": 7, "num_assets": 20, "correlation": 0.3, "risk": 4.046230647021512}, {"risk_level": 7, "num_assets": 20, "correlation": 0.4, "risk": 4.6297860615575495}, {"risk_level": 7, "num_assets": 20, "correlation": 0.5, "risk": 5.112604852697898}, {"risk_level": 7, "num_assets": 20, "correlation": 0.6, "risk": 5.499322778363281}, {"risk_level": 7, "num_assets": 20, "correlation": 0.7, "risk": 5.924732915682491}]}}, {"mode": "vega-lite"});
</script>



## Conclusion

The benefits of diversification are generally well known: reduced risk through exposure to different sources of income.  
The insight Dalio brings to the forefront, is that the construction of a diversified portfolio through a combination of _uncorrelated_ return streams, significantly decreases our overall risk, raising in turn our return/risk ratio. By the careful mixing of uncorrelated assets, we capture true _alpha_, enabling us to use leverage to increase our returns.

