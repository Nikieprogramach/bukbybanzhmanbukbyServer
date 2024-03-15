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

returnShipData = []
shipData = []

async def connect_ais_stream():

    async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
        subscribe_message = {"APIKey": "68f4a9e0b43a29f5a4c2a01658e928d53f90c73e", "BoundingBoxes": [[[-90, -180], [90, 180]]]}

        subscribe_message_json = json.dumps(subscribe_message)
        await websocket.send(subscribe_message_json)

        async for message_json in websocket:
            message = json.loads(message_json)
            message_type = message["MessageType"]

            if message["MessageType"] != "UnknownMessage" and message["MessageType"] == "ShipStaticData":
                # # the message parameter contains a key of the message type which contains the message itself
                # #print(f"[{datetime.now(timezone.utc)}] ShipId: {ais_message['UserID']} Latitude: {ais_message['Latitude']} Longitude: {ais_message['Longitude']}")
                # shipEntryAlreadyExists = False
                # for ship in shipData:
                #     if ship['ShipID'] == ais_message['UserID']:
                #         shipEntryAlreadyExists = True
                #         ship['Latitude'] = ais_message['Latitude']
                #         ship['Longitude'] = ais_message['Longitude']
                # if not shipEntryAlreadyExists and len(shipData) < 1000:
                #     shipData.append({"ShipID": ais_message['UserID'], "Latitude": ais_message['Latitude'], "Longitude": ais_message['Longitude']})
                if(message['Message']['ShipStaticData']['Type'] == 30):
                    ais_message = message['MetaData']
                    #print(message['Message']['ShipStaticData'])
                    #print(message)
                    shipEntryAlreadyExists = False
                    for ship in shipData:
                        if ship['ShipID'] == ais_message['MMSI']:
                            shipEntryAlreadyExists = True
                            ship['Latitude'] = ais_message['latitude']
                            ship['Longitude'] = ais_message['longitude']
                            print("Changed location")
                    if not shipEntryAlreadyExists and len(shipData) < 200:
                            shipData.append({"ShipID": ais_message['MMSI'], "Latitude": ais_message['latitude'], "Longitude": ais_message['longitude'], "Name": ais_message['ShipName']})

@app.route('/getFish', methods=['GET'])
def getFishInfo():
    searchType = request.args.get('searchType') # Options: all, byName, byClass
    name = request.args.get('name')
    print(searchType, name)
    fishLocationData = []
    with open("summaryData.csv", 'r', newline='', encoding='utf-8') as f_in:
        reader = csv.DictReader(f_in)
        
        if  searchType == "all":
            for row in reader:
                fishLocationData.append({"id": row['id'], "name": row['scientificname'], "latitude": row['decimallatitude'], "longitude": row['decimallongitude'], "amount": row['amount']})
        elif searchType == "byName":
            for row in reader:
                if row['scientificname'] == name:
                    fishLocationData.append({"id": row['id'], "name": row['scientificname'], "latitude": row['decimallatitude'], "longitude": row['decimallongitude'], "amount": row['amount']})
                else:
                    continue
        elif searchType == "byClass":
            for row in reader:
                if row['class'] == name:
                    fishLocationData.append({"id": row['id'], "name": row['scientificname'], "latitude": row['decimallatitude'], "longitude": row['decimallongitude'], "amount": row['amount']})
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