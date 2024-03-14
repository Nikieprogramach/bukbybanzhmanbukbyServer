import csv

fishLocationData = []
with open("tuna_data.csv", 'r', newline='', encoding='utf-8') as f_in:
    reader = csv.DictReader(f_in)
    
    for row in reader:
        #latitude = row['decimalLatitude']
        print(list(row.values())[1])
        #longitude = row['decimalLongitude']
        #name = row['scientificName']
        #fishLocationData.append({"name": name, "latitude": latitude, "longitude": longitude})

    print(fishLocationData)