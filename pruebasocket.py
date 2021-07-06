# -*- coding: utf-8 -*-

import json
import random
import time
from datetime import datetime
import requests
import pandas as pd
import numpy as np


from flask import Flask, Response, render_template

app = Flask(__name__)


#api_key = "a9d63e6b935687632ea75dcbe008a9e5d9452f053c192869607ef5441cd1203c"
api_key="cdf1177d69fa088656c47d9e7f65b912604ca069c5c4351a9ba0e0594cfa5103"
@app.route("/")
def index():
    return render_template("index.html")



def price(fsym, tsyms, exchange):
     url = "https://min-api.cryptocompare.com/data/price"
     params = {"api-key" : api_key, "tsyms":tsyms, "fsym":fsym, "e":exchange}
     r = requests.get(url, params = params)
     js = r.json()
     df = pd.DataFrame(js, index=[fsym]).transpose()
     return df

def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()

def generate_data():
    
    
    while True:
        try:
            
            value=price("BTC", "USD", "Coinbase").iloc[0,0]
            value1=price("BTC", "USD", "Kraken").iloc[0,0]
            
            
            json_data = json.dumps(
                {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "value": value,
                "value1":value1
                
                 }, default=np_encoder
                )
            time.sleep(1)
            yield f"data:{json_data}\n\n"
        except GeneratorExit:
            print("Valor no encontrado")
            return
        time.sleep(1)


@app.route("/chart-data")
def chart_data():
    return Response(generate_data(), mimetype="text/event-stream")


