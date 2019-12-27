import pandas as pd

def apply_mask(df,start,end):

    start_date=pd.to_datetime(start, format='%Y-%m-%d')
    end_date=pd.to_datetime(end, format='%Y-%m-%d')
    df['Dates'] = pd.to_datetime(df['Dates'], format='%d/%m/%Y')    

    mask = (df['Dates'] > start_date) & (df['Dates'] <= end_date)
    df=df.loc[mask]
    return df

