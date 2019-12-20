const Chart = require('chart.js');
const { unpackArray, range } = require('./utils');
const { generateWealthTrajectories, getHistograms } = require('./rgbm');

function getConfig(xLabel, xTicks, yLabel) {
  xTicks = typeof xTicks !== 'undefined' ? xTicks : false;
  return {
    type: 'bar',
    options: {
      legend: { display: false },
      animation: false,
      events: [],
      scales: {
        xAxes: [
          {
            scaleLabel: {
              display: true,
              fontSize: 18,
              labelString: xLabel
            },
            gridLines: {
              display: false
            },
            ticks: {
              display: xTicks
            }
          }
        ],
        yAxes: [
          {
            scaleLabel: {
              display: true,
              fontSize: 18,
              labelString: yLabel
            },
            ticks: {
              steps: 10,
              stepValue: 5,
              min: 0
            }
          }
        ]
      }
    }
  };
}

function plotTimeStep(chart, step, data, labels) {
  labels = typeof labels !== 'undefined' ? labels : range(data.length);
  chart.data.labels = labels;
  chart.data.datasets = [{ backgroundColor: '#c45850', data: data }];
  const histogram_time_span = document.getElementById('histogram_time');
  histogram_time_span.innerHTML = 'Year ' + step;
  const animation_time_span = document.getElementById('animation_time');
  animation_time_span.innerHTML = 'Year ' + step;
  chart.update();
}

function resetChart(chart) {
  var data = chart.data.datasets[0].data;
  chart.data.datasets[0].data = data.map(el => 0);
  chart.update();
}

window.onload = function() {
  var ctx = document.getElementById('animation').getContext('2d');
  var hist_ctx = document.getElementById('histogram').getContext('2d');
  window.barplot = new Chart(ctx, getConfig('Individual', false, 'Normalized wealth'));
  window.histogram = new Chart(hist_ctx, getConfig('Wealth percentile', true, 'Number of individuals'));
};

window.isPaused = false;
window.isDone = true;

var playButton = document.getElementById('startAnimation');
var pauseButton = document.getElementById('pauseAnimation');
var stopButton = document.getElementById('stopAnimation');

pauseButton.addEventListener('click', function() {
  window.isPaused = true;
});

stopButton.addEventListener('click', function() {
  if (window.animate) {
    clearInterval(window.animate);
  }
  resetChart(window.barplot);
  resetChart(window.histogram);
  window.isPaused = true;
  window.isDone = true;
});

playButton.addEventListener('click', function() {
  if (window.isDone) {
    if (window.animate) {
      clearInterval(window.animate);
    }

    var timeStep = 0;
    var N = getParam('N');
    var T = getParam('T');
    var dt = getParam('dt');
    var mu = getParam('mu');
    var sigma = getParam('sigma');
    var tau = getParam('tau');
    var bins = getParam('bins');
    wealthTrajectories = generateWealthTrajectories(N, T, dt, mu, sigma, tau);
    histograms = getHistograms(wealthTrajectories, bins);

    const maxSteps = Math.floor(T / dt / 10);
    const histStep = 100 / bins;
    const binLabels = range(bins).map(
      el => `${Math.round(el * histStep * 100) / 100} - ${Math.round((el + 1) * histStep * 100) / 100}`
    );

    window.animate = window.setInterval(function() {
      if (!window.isPaused) {
        if (timeStep < maxSteps) {
          var row = unpackArray(wealthTrajectories.pick(timeStep * 10, null));
          var histRow = unpackArray(histograms.pick(timeStep * 10, null));
          plotTimeStep(window.barplot, timeStep, row);
          plotTimeStep(window.histogram, timeStep, histRow, binLabels);
          timeStep++;
        } else {
          window.isDone = true;
          clearInterval(window.animate);
        }
      }
    }, 300);

    window.isDone = false;
  }

  window.isPaused = false;
});

function getParam(name) {
  return parseFloat(document.getElementById(name).value);
}
