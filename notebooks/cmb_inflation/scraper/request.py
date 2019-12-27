#!/usr/bin/env python 
import requests 
from datetime import date,datetime

def request_inflation(from_date="1943-02-28",to_date=date.today()):
   
    url="http://45.235.96.100/PublicacionesEstadisticas/Principales_variables_datos.asp"
    form_data = {"fecha_desde":[from_date,'20140207'],"fecha_hasta":[to_date,'20190903'],"B1":"Enviar",
                "primeravez":1,"serie":7931,"serie1":0,"serie2":0,"serie3":0,"serie4":0,"detalle":"Inflación+mensual+(variación+en+)"}
    r = requests.post(url,data=form_data)
    return r.text

def request_base_monetaria(from_date="2003-01-30",to_date=date.today()):
    url="http://45.235.96.100/PublicacionesEstadisticas/Principales_variables_datos.asp"
    form_data = {"fecha_desde":[from_date,None],"fecha_hasta":[to_date,None],"B1":"Enviar",
            "primeravez":1,"serie":7930,"serie1":0,"serie2":0,"serie3":0,"serie4":0,"detalle":"Base+Monetaria+-+Promedio+acumulado+del+mes++(MM+de+$)"}
    r = requests.post(url,data=form_data)
    return r.text

def request_base_monetaria_circulante(from_date="2003-01-30",to_date=date.today()):
    url="http://45.235.96.100/PublicacionesEstadisticas/Principales_variables_datos.asp"
    form_data = {"fecha_desde":[from_date,None],"fecha_hasta":[to_date,None],"B1":"Enviar",
            "primeravez":1,"serie":251,"serie1":0,"serie2":0,"serie3":0,"serie4":0,"detalle":"Circulación+monetaria+(en+millones+de+pesos)"}
    r = requests.post(url,data=form_data)
    return r.text


