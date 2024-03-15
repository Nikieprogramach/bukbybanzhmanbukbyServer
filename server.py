from flask import Flask, request
from flask_cors import CORS
import csv
import json
import requests

import asyncio
import websockets
import json
from datetime import datetime, timezone

from threading import Thread
from werkzeug.serving import run_simple


app = Flask(__name__)

CORS(app)

shipData = []

async def connect_ais_stream():

    async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
        subscribe_message = {"APIKey": "1e5475701789abb7a9a04441e01761ba1ff90d78", "BoundingBoxes": [[[-90, -180], [90, 180]]]}

        subscribe_message_json = json.dumps(subscribe_message)
        await websocket.send(subscribe_message_json)

        async for message_json in websocket:
            message = json.loads(message_json)
            message_type = message["MessageType"]

            if message_type == "PositionReport":
                # the message parameter contains a key of the message type which contains the message itself
                ais_message = message['Message']['PositionReport']
                #print(f"[{datetime.now(timezone.utc)}] ShipId: {ais_message['UserID']} Latitude: {ais_message['Latitude']} Longitude: {ais_message['Longitude']}")
                shipEntryAlreadyExists = False
                for ship in shipData:
                    if ship['ShipID'] == ais_message['UserID']:
                        shipEntryAlreadyExists = True
                        ship['Latitude'] = ais_message['Latitude']
                        ship['Longitude'] = ais_message['Longitude']
                if not shipEntryAlreadyExists and len(shipData) < 1000:
                    shipData.append({"ShipID": ais_message['UserID'], "Latitude": ais_message['Latitude'], "Longitude": ais_message['Longitude']})

@app.route('/getFish', methods=['GET'])
def getFishInfo():
    searchType = request.args.get('searchType') # Options: all, byName, byClass
    name = request.args.get('name')
    print(searchType, name)
    fishLocationData = []
    with open("tuna_data.csv", 'r', newline='', encoding='utf-8') as f_in:
        reader = csv.DictReader(f_in)
        
        if  searchType == "all":
            for row in reader:
                alreadyHaveFish = False
                for fishInfo in fishLocationData:
                    if round(float(fishInfo['latitude']), 1) == round(float(list(row.values())[3]), 1) and round(float(fishInfo['longitude']), 1) == round(float(list(row.values())[2]), 1):
                        fishInfo["amount"] += 1
                        alreadyHaveFish = True
                        break
                if  not alreadyHaveFish:
                    fishLocationData.append({"id": list(row.values())[0], "name": list(row.values())[8], "latitude": list(row.values())[3], "longitude": list(row.values())[2], "amount": 1})
        elif searchType == "byName":
            for row in reader:
                if str(row['scientificname']) == name:
                    alreadyHaveFish = False
                    for fishInfo in fishLocationData:
                        if round(float(fishInfo['latitude']), 1) == round(float(list(row.values())[3]), 1) and round(float(fishInfo['longitude']), 1) == round(float(list(row.values())[2]), 1):
                            fishInfo["amount"] += 1
                            alreadyHaveFish = True
                            break
                    if  not alreadyHaveFish:
                        fishLocationData.append({"id": list(row.values())[0], "name": list(row.values())[8], "latitude": list(row.values())[3], "longitude": list(row.values())[2], "amount": 1})
                else:
                    continue
        elif searchType == "byClass":
            for row in reader:
                if row['class'] == name:
                    alreadyHaveFish = False
                    for fishInfo in fishLocationData:
                        if round(float(fishInfo['latitude']), 1) == round(float(list(row.values())[3]), 1) and round(float(fishInfo['longitude']), 1) == round(float(list(row.values())[2]), 1):
                            fishInfo["amount"] += 1
                            alreadyHaveFish = True
                            break
                    if  not alreadyHaveFish:
                        fishLocationData.append({"id": list(row.values())[0], "name": list(row.values())[8], "latitude": list(row.values())[3], "longitude": list(row.values())[2], "amount": 1})
                else:
                    continue
        else:
            return "Wrong input!"
    #print(fishLocationData)
    return json.dumps(fishLocationData)

@app.route('/getShips', methods=['GET'])
def GetShipInfo():
    return json.dumps(shipData)

if __name__ == '__main__':
    # app.run(debug=True)
        # Start Flask app in a separate thread
    async_thread = Thread(target=lambda: asyncio.run(connect_ais_stream()))
    async_thread.start()
    app.run(debug=True)