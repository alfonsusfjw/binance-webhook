import json, config
from datetime import datetime, timedelta, timezone
from binance.um_futures import UMFutures
from flask import Flask, request


# Requirement code for flask
app = Flask(__name__)

# API_KEY & API_SECRET
eKey=config.testnet.key
eSecret=config.testnet.key
eBaseURL=config.testnet.url
um_futures_client = UMFutures(key=eKey, secret=eSecret, base_url=eBaseURL)

# Database
# eSymbol = str("").upper() # BTCUSDT, BNBUSDT, ETHUSDT
# eSide = str("").upper() # BUY, SELL
# eType = str("MARKET").upper() # LIMIT, MARKET, STOP, STOP_MARKET, TAKE_PROFIT
# ePositionSide = str("BOTH").upper() # BOTH, LONG, SHORT
# eTimeInForce = str("GTC").upper()
# eQuantity = float()
# eReduceOnly = str("").upper()
# ePrice = float()
# eNewClientOrderId = "byTradingTool" # Optional string. An unique ID among open orders. Automatically generated if not sent.
# eStopPrice = float() # Optional float. Use with STOP/STOP_MARKET or TAKE_PROFIT/TAKE_PROFIT_MARKET orders
# eClosePosition = str("").upper() # Optional string. true or false; Close-All, use with STOP_MARKET or TAKE_PROFIT_MARKET.
# eActivationPrice = float() # Optional float. Use with TRAILING_STOP_MARKET orders, default is the latest price
# eCallbackRate = float() # Optional float. Use with TRAILING_STOP_MARKET orders, min 0.1, max 5 where 1 for 1%.
# eWorkingType = str("CONTRACT_PRICE").upper()
# ePriceProtect = str("FALSE").upper()
# eNewOrderRespType = str("ACK").upper()
# eRecvWindow = int(5000)
# webhookData = str()

# Homepage
@app.route('/')
def welcomePage():
    return 'Welcome to trading tools management system!'

# Execute webhook signal
@app.route("/webhook", methods=["POST"])
def webhook():

    webhookData = json.loads(request.data)
    eSymbol = webhookData["eSymbol"].upper()
    eSide = webhookData["eSide"].upper()
    eType = webhookData["eType"].upper()
    ePositionSide = webhookData["ePositionSide"].upper()
    eTimeInForce = webhookData["eTimeInForce"].upper()
    eQuantity = float(str(webhookData["eQuantity"].split()[0]))
    ePrice = float(webhookData["ePrice"])
    pembagi = float(ePrice / eQuantity)
    lot = float(1.0/pembagi)
    lot = str(lot)
    lot = lot[0:4]
    tp = ePrice + (ePrice * 3/100)

    
    eNewClientOrderId = webhookData["eNewClientOrderId"]
    print(eSymbol)
    print(eSide)
    print(eType)
    print(ePositionSide)
    print(eTimeInForce)
    print(eQuantity)
    print(pembagi)
    print(f"Size = {lot}")
    print(eNewClientOrderId)
    print(tp)

    um_futures_client = UMFutures(key=config.testnet.key, secret=config.testnet.secret, base_url=config.testnet.url)
    newOrder = um_futures_client.new_order(symbol=eSymbol, side=eSide, type=eType, positionSide=ePositionSide, quantity=lot, newClientOrderId=eNewClientOrderId)

    nowtime = datetime.now()
    d = datetime.fromisoformat(str(nowtime))
    tz = timezone(timedelta(hours=7))
    new_time = d.astimezone(tz)

    print()
    print("=======================================================")
    print()
    print(f"Eksekusi pada {new_time}")
    print()
    print(newOrder)
    print()
    print("=======================================================")

    return webhookData 


# Run flask
if __name__ == "__main__":
    app.run(debug=True)

