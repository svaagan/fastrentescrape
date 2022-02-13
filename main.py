# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import datetime as dt
import os

url = "https://www.dnb.no/lan/boliglan/fastrente?mcc=ppc-google_boliglan-brand-fastrente&gclid=Cj0KCQiAoY-PBhCNARIsABcz770wPpwHwqEj63XdrGimJGe-n9_QEsmfQUTEhWrln1O9fqaFfz2CQIQaAnLkEALw_wcB"

nettside = requests.get(url)

soup = bs(nettside.content, 'html.parser')

#Henter ut alle rentesatsene
renteblokk = soup.find('div',class_="css-vszval e15b33c54") 

#Isolerer og henter ut 3 års fastrenta
trear = renteblokk.find('span',class_="css-o15es7 e15b33c51")

trear = trear.get_text()

#Isolerer 5 og 10 års
femar = renteblokk.find('div',class_="dnb-space dnb-space__top--medium e15b33c50 css-16k0o79 e1c60gem0")

#Finner 5 ar ved å hente ut første treff på tag/class
femar = femar.find("p")

#Finner 10 år ved å lete etter neste p-tag i femar da de ikke har forskjellig class
tiar = femar.find_next("p")

tiar = tiar.find("b")

tiar = tiar.get_text()

#Finner renten for 5 åringen
femar = femar.find("b")

femar = femar.get_text()

#fjerner % for å konvertere til tall
trear = trear.rstrip("%")

femar = femar.rstrip("%")

tiar = tiar.rstrip("%")

#endrer komma til punktum for å kunne konvertere til tall
trear = trear.replace(",",".")

femar = femar.replace(",",".")

tiar = tiar.replace(",",".")

trear = float(trear)

femar = float(femar)

tiar = float(tiar)

#import fastparquet

timestamp = dt.datetime.now()

#lager en liste
data = [(timestamp, trear, femar, tiar)]
    
#putter listen inn i dataframe med kolonnenavn
df = pd.DataFrame([(timestamp, trear, femar, tiar)],
            columns = ('Dttm','Trear','Femar','Tiar')
                 )
                    
    
print(df)    

# if file does not exist write header 
if not os.path.isfile('test.csv'):
   df.to_csv('test.csv')
else: # else it exists so append without writing the header
   df.to_csv('test.csv', mode='a', header=False)





















   
    
    
