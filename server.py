from flask import Flask, request
from flask_cors import CORS
import csv
import json

app = Flask(__name__)

CORS(app)


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
                if row['scientificname'] == name:
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
        
    return json.dumps(fishLocationData)

if __name__ == '__main__':
    app.run(debug=True)