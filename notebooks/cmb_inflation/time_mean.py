import pandas as pd

def mean_in_time(df,time_to_average):
    '''df: dataframe, time_to_average: rule of target conversion'''

    df['Dates'] = pd.to_datetime(df['Dates'], format='%d/%m/%Y')    
    name=df.columns[1]
    df=df.reset_index().set_index('Dates')
    df=df.drop(['index'],axis=1)
    df=df.resample(time_to_average).mean()
    df.reset_index(level=0, inplace=True)
    df.rename(columns={df.columns[1]:name},inplace = True)
    return df