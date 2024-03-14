import csv

fishLocationData = []
with open("tuna_data.csv", 'r', newline='', encoding='utf-8') as f_in:
    reader = csv.DictReader(f_in)
    
    for row in reader:
        alreadyHaveFish = False
        for fishInfo in fishLocationData:
            if fishInfo['latitude'] == list(row.values())[3] and fishInfo['longitude'] == list(row.values())[2]:
                fishInfo["amount"] += 1
                alreadyHaveFish = True
                break
        if  not alreadyHaveFish:
            fishLocationData.append({"id": list(row.values())[0], "name": list(row.values())[8], "latitude": list(row.values())[3], "longitude": list(row.values())[2], "amount": 1})

print(fishLocationData)