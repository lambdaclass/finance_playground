"""Generates charts from a portfolio report"""

import altair as alt


def returns_chart(report):
    selection = alt.selection(type="interval", encodings=["x"])

    chart = alt.Chart().mark_area(point="transparent").encode(
        alt.X("index:T", scale={"domain": selection.ref()}),
        y="% Price:Q",
        tooltip=["% Price:Q"]).properties(
            width=600, height=200)

    lower = chart.properties(height=60).add_selection(selection)

    return alt.vconcat(chart, lower, data=report.reset_index())


def portfolio_composition(report):
    alt.Chart(report.reset_index()).mark_area(opacity=0.3).encode(
        x="index:T",
        y=alt.Y("Total Portfolio:Q", stack=None),
        color="source:N")


def returns_histogram(report):
    bar = alt.Chart(report).mark_bar().encode(
        x=alt.X(
            "Interval Change:Q",
            bin=alt.BinParams(maxbins=100),
            axis=alt.Axis(format='%')),
        y="count():Q")
    return bar


def monthly_returns_heatmap(report):
    monthly_returns = report.resample(
        "M")["Total Portfolio"].last().pct_change().reset_index()
    monthly_returns.columns = ["Date", "Monthly Returns"]

    chart = alt.Chart(monthly_returns).mark_rect().encode(
        alt.X("Date:T", bin=alt.Bin(maxbins=60)),
        alt.Y("Monthly Returns", bin=alt.Bin(maxbins=40)),
        alt.Color("Monthly Returns:Q", scale=alt.Scale(scheme="greenblue")))

    return chart
