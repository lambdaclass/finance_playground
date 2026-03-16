#!/usr/bin/env python

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (14, 8)


def plot_average_growth_rate(country, filename):
    df = pd.read_csv(
        filename,
        header=None,
        names=['year', 'short_rate', 'long_rate', 'stock', 'housing'])

    df['stock_returns'] = df['stock'].pct_change()
    df['housing_returns'] = df['housing'].pct_change()

    stock_rets = df['stock_returns'].values[1:]
    house_rets = df['housing_returns'].values[1:]
    riskless_rets = (df['long_rate'] / 100).values[1:]

    leverage_levels = np.sort(np.append([0], np.linspace(-12, 12, 1000)))

    # Should consider vectorizing this code
    rets = np.zeros([len(leverage_levels), 2])

    for j in range(len(leverage_levels)):
        equity_s = equity_h = 1.0
        for i in range(len(stock_rets)):
            equity_s = ((1 + stock_rets[i]) * leverage_levels[j] +
                        (1 + riskless_rets[i]) *
                        (1 - leverage_levels[j])) * equity_s
            equity_h = ((1 + house_rets[i]) * leverage_levels[j] +
                        (1 + riskless_rets[i]) *
                        (1 - leverage_levels[j])) * equity_h
        rets[j, 0] = equity_s
        rets[j, 1] = equity_h

    sigma_s = np.std(stock_rets)
    sigma_h = np.std(house_rets)
    sigma_r = np.std(riskless_rets)

    rho_s = np.corrcoef(riskless_rets, stock_rets)
    rho_h = np.corrcoef(riskless_rets, house_rets)

    sigsig_s = np.sqrt(
        sigma_s**2 + sigma_r**2 + 2 * rho_s[0, 1] * sigma_s * sigma_r) / (
            np.sqrt(len(stock_rets)) *
            (sigma_s**2 + sigma_r**2 - 2 * rho_s[0, 1] * sigma_s * sigma_r))
    sigsig_h = np.sqrt(
        sigma_h**2 + sigma_r**2 + 2 * rho_h[0, 1] * sigma_h * sigma_r) / (
            np.sqrt(len(house_rets)) *
            (sigma_h**2 + sigma_r**2 - 2 * rho_h[0, 1] * sigma_h * sigma_r))

    limits_s = np.where(rets[:, 0] < 0)[0]
    cutoff_s = np.where(limits_s > 500)[0][0]
    bounds_s = np.arange(limits_s[cutoff_s - 1] + 1, limits_s[cutoff_s])

    leverage_levels_s = leverage_levels[bounds_s]
    stock_rets_bounded = rets[:, 0][bounds_s]

    limits_h = np.where(rets[:, 1] < 0)[0]
    cutoff_h = np.where(limits_h > 500)[0][0]
    limits_h = np.append(limits_h, 0)
    bounds_h = np.arange(limits_h[cutoff_h - 1] + 1, limits_h[cutoff_h])

    leverage_levels_h = leverage_levels[bounds_h]
    house_rets_bounded = rets[:, 1][bounds_h]

    bounded_stock_rets = rets[:, 0][bounds_s]
    yearly_log_rets_s = np.log(bounded_stock_rets) / len(stock_rets)

    bounded_house_rets = rets[:, 1][bounds_h]
    yearly_log_rets_h = np.log(bounded_house_rets) / len(house_rets)

    max_stock_ret = stock_rets_bounded.max()
    opt_lev_stock_idx = stock_rets_bounded.argmax()
    opt_lev_stock = leverage_levels_s[opt_lev_stock_idx]

    if house_rets_bounded.size > 0:
        max_house_ret = house_rets_bounded.max()
        opt_lev_house_idx = house_rets_bounded.argmax()
        opt_lev_house = leverage_levels_h[opt_lev_house_idx]
    else:
        opt_lev_house = leverage_levels[0]

    max_ls = opt_lev_stock + 2 * sigsig_s
    min_ls = opt_lev_stock - 2 * sigsig_s
    area_s = np.where((leverage_levels_s >= min_ls)
                      & (leverage_levels_s <= max_ls))[0]

    max_lh = opt_lev_house + 2 * sigsig_h
    min_lh = opt_lev_house - 2 * sigsig_h
    area_h = np.where((leverage_levels_h >= min_lh)
                      & (leverage_levels_h <= max_lh))[0]

    with plt.style.context('Solarize_Light2'):
        plt.title(country + ' ' + str(df['year'].min()) + '-' +
                  str(df['year'].max()))
        plt.xlabel('Leverage')
        plt.ylabel('Time-average annual growth rate')

        plt.plot(leverage_levels_s,
                 yearly_log_rets_s,
                 'tab:blue',
                 label='Stocks',
                 linewidth=3)
        plt.plot(leverage_levels_h,
                 yearly_log_rets_h,
                 'tab:orange',
                 label='Housing',
                 linewidth=3)

        max_log_ret_s = np.log(max_stock_ret) / len(stock_rets)
        max_log_ret_h = np.log(max_house_ret) / len(house_rets)

        plt.vlines(opt_lev_stock,
                   ymin=0,
                   ymax=max_log_ret_s,
                   colors=['tab:blue'],
                   linestyle=':',
                   linewidth=2)
        plt.vlines(opt_lev_house,
                   ymin=0,
                   ymax=max_log_ret_h,
                   colors=['tab:orange'],
                   linestyle=':',
                   linewidth=2)
        plt.vlines(1,
                   ymin=0,
                   ymax=max(max_log_ret_s, max_log_ret_h),
                   linestyle='--',
                   linewidth=2)

        plt.fill_between(leverage_levels_s[area_s],
                         np.log(bounded_stock_rets[area_s]) / len(stock_rets),
                         facecolor='tab:blue',
                         alpha=0.35)
        plt.fill_between(leverage_levels_h[area_h],
                         np.log(bounded_house_rets[area_h]) / len(house_rets),
                         facecolor='tab:orange',
                         alpha=0.35)

        plt.ylim(0, 0.15)
        plt.legend(loc='upper right')

        plt.savefig(country + str(df['year'].min()) + '-' +
                    str(df['year'].max()))
        plt.close()


if __name__ == '__main__':
    countries = [
        'AUS', 'BEL', 'CAN', 'CHE', 'DEU', 'DNK', 'ESP', 'FIN', 'FRA', 'GBR',
        'ITA', 'JPN', 'NLD', 'NOR', 'PRT', 'SWE', 'USA'
    ]

    for country in countries:
        filename = os.path.join('data', country + '.csv')
        plot_average_growth_rate(country, filename)
