"""
East Village Trading Robot
Requirements: Tradingview - Alpaca - Ngrok - AWS (amazon web server)
Enter your alpaca api key and secret key in config.py
Visit the wiki on the github page for detailed installation steps

Author: Dan Wallace
Contributors: William Bracken, Brent Richmond
Website: www.brick.technology
Email: danwallaceasu@gmail.com
Created: 08/30/20

<<Last Update: 09/25/20>>
"""

import ast
import requests
import json
from flask import Flask, request, abort
from config import *

def placeOrder(data):  
    BASE_URL = "https://paper-api.alpaca.markets"
    ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
    ORDERS_URL = "{}/v2/orders".format(BASE_URL)
    HEADERS = {'APCA-API-KEY-ID': key, 'APCA-API-SECRET-KEY': secretKey}
    order = requests.post(ORDERS_URL, json=data, headers=HEADERS)
    return json.loads(order.content)

def webhookParse(webhook_data):
    
    data = ast.literal_eval(webhook_data)
    return data

flaskServer = Flask(__name__)

@flaskServer.route('/')
def root():
    return 'online'

@flaskServer.route('/webhook', methods=['POST'])
def webhookListen():
    if request.method == 'POST':
        data = webhookParse(request.get_data(as_text=True))
        print(' ---- Tradingview Alert Received')
        print('Alert:', data)
        print(' ---- Sending Trade to Alpaca')
        print('Sending order: Symbol ', data["symbol"],' Quantity: ', data["qty"],' Buy/Sell: ', data["side"],' Type: ', data["type"],' Time in force: ', data["time_in_force"])
        print(' ---- Order Sent')
        placeOrder(data)
        return '', 200
    else:
        abort(400)

if __name__ == '__main__':
    flaskServer.run()

## <(^_^<)end(>^_^)>