# import csv

# fishLocationData = []
# with open("tuna_data.csv", 'r', newline='', encoding='utf-8') as f_in:
#     reader = csv.DictReader(f_in)
#     names = []

#     for row in reader:
#         if row['class'] not in names:
#             names.append(row['class'])

# with open('array.txt', 'w') as f:
#     for item in names:
#         f.write(str(item) + '\n')

import csv
import sys

csv.field_size_limit(2147483647)

def filter_tuna(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as f_in:
        reader = csv.DictReader(f_in)
        
        # with open(output_file, 'w', newline='', encoding='utf-8') as f_out:
        #     # writer = csv.DictWriter(f_out, ['key', 'id', 'decimallongitude', 'decimallatitude', 'scientificname', 'class', 'amount'])
        #     fields = ['key', 'id', 'decimallongitude', 'decimallatitude', 'scientificname', 'class', 'amount']
        #     writer = csv.DictWriter(f_out, fieldnames=fields)
        #     writer.writeheader()
            
            # Reads classes
        dict = {}
        for row in reader:
            key = row['scientificname'] + "/" + str(round(float(row['decimallongitude']), 1)) + "/" + str(round(float(row['decimallatitude']), 1))
            if key in dict:
                dict[key]['amount'] += 1
            else:
                dict[key] = {'key': key, 'id': row['id'], 'decimallongitude': row['decimallongitude'], 'decimallatitude': row['decimallatitude'], 'scientificname': row['scientificname'], 'class': row['class'], 'amount': 1}

            # dict[key] = row['id'] + "," + row['decimallongitude'] + "," + row['decimallatitude'] + "," + row['name'] + "," + row['class'] + "," + 1
        # for keyInDict in dict:
        #     print(dict[keyInDict])
        #     row = str(keyInDict) + "," + str(dict[keyInDict]['id']) + "," + str(dict[keyInDict]['decimallongitude']) + "," + str(dict[keyInDict]['decimallatitude']) + "," + str(dict[keyInDict]['scientificname']) + "," + str(dict[keyInDict]['class']) + "," + str(dict[keyInDict]['amount'])
        #     writer.writerow(row)
        fields = ['key', 'id', 'decimallongitude', 'decimallatitude', 'scientificname', 'class', 'amount']
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            # writer.writerows(dict)
            for keyInDict in dict:
                # print(dict[keyInDict])
                # row = str(keyInDict) + "," + str(dict[keyInDict]['id']) + "," + str(dict[keyInDict]['decimallongitude']) + "," + str(dict[keyInDict]['decimallatitude']) + "," + str(dict[keyInDict]['scientificname']) + "," + str(dict[keyInDict]['class']) + "," + str(dict[keyInDict]['amount'])
                writer.writerow(dict[keyInDict])
           

if __name__ == "__main__":
    input_file = "tuna_data.csv"  # Replace with the path to your original CSV file
    output_file = "summaryData.csv"  # New CSV file with information about different kinds of tuna
    filter_tuna(input_file, output_file)