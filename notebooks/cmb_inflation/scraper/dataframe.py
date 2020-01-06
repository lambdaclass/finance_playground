import pandas as pd 


def df(name_txt, header,save=False,name=None):
    data = pd.read_csv(name_txt, sep="\t", header=None,decimal=',')
    if save:
        data.to_csv('Documents/proyectos/Scraper/'+name+'.csv',header=header,index=False)
    return data