import json, config
from binance.client import Client
from binance.enums import *
import time
import arrow
from flask import Flask, request
app = Flask(__name__)

# API_KEY & API_SECRET
client = Client(config.ori_key, config.ori_secret)

# Store the price
openStore = []
closeStore = []
highStore = []
lowStore = []

def tambah():
    hasil = 1 + 12
    return hasil

@app.route('/')
def welcomePage():
    return 'Welcome to trading tools management system!'

@app.route("/webhook", methods=["POST"])
def webhook():
    #print(request.data)
    data = json.loads(request.data)

    print(data)
    if data["validasi"]=="sukses":
        print(f"berhasil, 1 + 12 = {tambah()}")
    
    aktif = True
    while aktif:
        candles = client.get_klines(symbol='BNBUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, limit = 1,)
        utc = candles[0][0]
        waktu = arrow.get(utc).format("YYYY-MM-DD HH:mm:ss")
        open = candles[0][1]
        openStore.append(open)
        high = candles[0][2]
        highStore.append(highStore)
        low = candles[0][3]
        lowStore.append(low)
        close = candles[0][4]
        closeStore.append(close)
        return f"{waktu}, Open: {open}, Close: {close}, High: {high}, Low: {low}"
        time.sleep(1)

if __name__ == "__main__":
    app.run(debug=True)
