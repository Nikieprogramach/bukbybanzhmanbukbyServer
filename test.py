import csv

fishLocationData = []
with open("tuna_data.csv", 'r', newline='', encoding='utf-8') as f_in:
    reader = csv.DictReader(f_in)
    names = []

    for row in reader:
        if row['scientificname'] not in names:
            names.append(row['scientificname'])

with open('array.txt', 'w') as f:
    for item in names:
        f.write(str(item) + '\n')