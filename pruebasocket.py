# -*- coding: utf-8 -*-

import json
import random
import time
from datetime import datetime
import requests
import pandas as pd



from flask import Flask, Response, render_template

application = Flask(__name__)


api_key = "a9d63e6b935687632ea75dcbe008a9e5d9452f053c192869607ef5441cd1203c"

@application.route("/")
def index():
    return render_template("index.html")



def price(fsym, tsyms, exchange):
     url = "https://min-api.cryptocompare.com/data/price"
     params = {"api-key" : api_key, "tsyms":tsyms, "fsym":fsym, "e":exchange}
     r = requests.get(url, params = params)
     js = r.json()
     df = pd.DataFrame(js, index=[fsym]).transpose()
     return df



def generate_data():
    
    
    while True:
        try:
            
            value=price("BTC", "USD", "Coinbase").iloc[0,0]
            value1=price("BTC", "USD", "Kraken").iloc[0,0]
            spread = abs(value - value1)
            
            json_data = json.dumps(
                {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "value": value,
                "value1":value1,
                "spread":spread
                 }
                )
            yield f"data:{json_data}\n\n"
        except:
            pass
        
        time.sleep(1)


@application.route("/chart-data")
def chart_data():
    return Response(generate_data(), mimetype="text/event-stream")


if __name__ == "__main__":
    application.run(threaded=True)