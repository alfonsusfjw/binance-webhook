import json, config
from sys import excepthook
from datetime import datetime, timedelta, timezone
from binance.um_futures import UMFutures
from flask import Flask, request

# Requirement code for flask
app = Flask(__name__)

# API_KEY & API_SECRET
eKey=config.testnet.key
eSecret=config.testnet.secret
eBaseURL=config.testnet.url
um_futures_client = UMFutures(key=eKey, secret=eSecret, base_url=eBaseURL)

# Homepage
@app.route('/')
def welcomePage():
    return 'Welcome to trading tools management system!'

# Execute webhook signal
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        webhookData = json.loads(request.data)
        dSymbol = webhookData["whSymbol"]
        dPrice = webhookData["whPrice"]
        dSide = webhookData["whSide"]
        dPositionSide = "LONG" if dSide == "BUY" else "SHORT"
        dType = webhookData["whType"] # MARKET/LIMIT/STOP
        dSize = webhookData["whSize"]
        dQuantity = round(1.0 / (float(dPrice) / float(dSize.split(" USDT")[0])), 2)
        dTimeInForce = webhookData["whTimeInForce"]
        dUseTP = webhookData["whUseTP"] # True / False
        dUseSL = webhookData["whUseSL"]
        dTP = webhookData["whTP"] # dalam percent
        dSL = webhookData["whSL"] # dalam percent
        
        # Place a time for debugging
        nowtime = datetime.now()
        d = datetime.fromisoformat(str(nowtime))
        tz = timezone(timedelta(hours=7))
        new_time = d.astimezone(tz)

        print()
        print("###################################################################################################")
        print(new_time)
        print("###################################################################################################")
        print(f"dSymbol = {dSymbol}")
        print(f"dPrice = {dPrice}")
        print(f"dSide = {dSide}")
        print(f"dPositionSide = {dPositionSide}")
        print(f"dType = {dType}")
        print(f"dSize = {dSize}")
        print(f"dQuantity = {dQuantity}")
        print(f"dTimeInForce = {dTimeInForce}")
        print(f"dUseTP = {dUseTP}")
        print(f"dUseSLT = {dUseSL}")
        print(f"dTP = {dTP}")
        print(f"dSL = {dSL}")

        # Take Profit Formula
        def TP(x,y): # x = dTP & y = dPrice
            if dSide == "BUY" :
                return round((100.0 + x)/100 * y, 2)
            else:
                return round((100.0 - x)/100 * y, 2)

        # Stop Loss Formula
        def SL(x,y): # x = dSL & y = dPrice
            if dSide == "BUY" :
                return round((100.0 - x)/100 * y, 2)
            else:
                return round((100.0 + x)/100 * y, 2)

        # Execute The Signal
        if dType == "MARKET":
            lastOrder = um_futures_client.get_position_risk(symbol="BNBUSDT",recvWindow=6000)
            openedLongSize = float(lastOrder[0]["positionAmt"])
            openedShortSize = float(lastOrder[1]["positionAmt"])
            openedLongPnL = float(lastOrder[0]["unRealizedProfit"])
            openedShortPnL = float(lastOrder[1]["unRealizedProfit"])

            if openedLongSize != 0.00 and openedLongPnL > 0:
                # Close Opened Buy
                newOpenPosition = um_futures_client.new_order(
                    symbol=dSymbol,
                    side="SELL",
                    positionSide="LONG",
                    type=dType,
                    quantity=abs(openedLongSize),
                )
            if openedShortSize != 0.00 and openedShortPnL >0:
                # Close Opened Sell
                newOpenPosition = um_futures_client.new_order(
                    symbol=dSymbol,
                    side="BUY",
                    positionSide="SHORT",
                    type=dType,
                    quantity=abs(openedShortSize),
                )
            # Open New Market
            newOpenPosition = um_futures_client.new_order(
                symbol=dSymbol,
                side=dSide,
                positionSide=dPositionSide,
                type=dType,
                quantity=dQuantity,
            )
        elif dType == "LIMIT":
            newOpenPosition = um_futures_client.new_order(
                symbol=dSymbol,
                side=dSide,
                positionSide=dPositionSide,
                type=dType,
                quantity=dQuantity,
                timeInForce=dTimeInForce,
                price=dPrice,
            )
        elif dType == "STOP":
            newOpenPosition = um_futures_client.new_order(
                symbol=dSymbol,
                side=dSide,
                positionSide=dPositionSide,
                type=dType,
                quantity=dQuantity,
                timeInForce=dTimeInForce,
                price=dPrice,
                stopPrice=dPrice
            )
        
        # Use Take Profit & Stoplos
        if dUseTP == "TRUE":
            setTakeProfit = um_futures_client.new_order(
                    symbol=dSymbol,
                    side= "SELL" if dSide == "BUY" else "BUY",
                    positionSide=dPositionSide,
                    type="TAKE_PROFIT_MARKET",
                    quantity=dQuantity,
                    timeInForce=dTimeInForce,
                    stopPrice=TP(0.3,dPrice)
                    # reduceOnly="TRUE"
                )
        if dUseSL == "TRUE":
            setStopLoss = um_futures_client.new_order(
                symbol=dSymbol,
                side= "SELL" if dSide == "BUY" else "BUY",
                positionSide=dPositionSide,
                type="STOP_MARKET",
                quantity=dQuantity,
                timeInForce=dTimeInForce,
                stopPrice=SL(dSL,dPrice)
            )

        print("===================================================================================================")
        print(newOpenPosition)
        print("===================================================================================================")
        
        return webhookData

# Run flask
if __name__ == "__main__":
    app.run(debug=True)

