import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
from matplotlib.ticker import AutoMinorLocator
def plot(df,start,end,month_mean=False):
    ''' start & end fmt=yyyy-mm-dd'''
    fig, ax = plt.subplots(constrained_layout=True, figsize=(16, 7))

    years = mdates.YearLocator()   # every year
    months = mdates.MonthLocator(interval=3)  # every 3 months
    years_fmt = mdates.DateFormatter('%Y')

    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(years_fmt)
    ax.xaxis.set_minor_locator(months)

    ax.tick_params(axis="x", labelsize=12, labelrotation=40)
    ax.tick_params(axis="y", labelsize=12)
    df['Dates'] = pd.to_datetime(df['Dates'], format='%d/%m/%Y')    
    
    start_date=pd.to_datetime(start, format='%Y-%m-%d')
    end_date=pd.to_datetime(end, format='%Y-%m-%d')
   
    mask = (df['Dates'] > start_date) & (df['Dates'] <= end_date)
    df=df.loc[mask]
    
    ax.grid(alpha=0.3)
    
    ax.set_xlabel(df.columns[0],fontweight='bold',fontsize='x-large')
    ax.set_ylabel(df.columns[1],fontweight='bold',fontsize='x-large')
    #ax.set_title(df.columns[1]+' over time, Argentina',fontweight='bold',fontsize='xx-large')

    ax.plot(df[str(df.columns[0])],df[str(df.columns[1])],"-",color='black',markersize=2)
    return ax