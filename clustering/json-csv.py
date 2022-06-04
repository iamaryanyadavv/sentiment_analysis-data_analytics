import json
import csv
 
f = open('./data/singapore_hotels_final.json')
 

data = json.load(f)["hotels"]
 


f.close()

with open('singapore.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Serial No.', 'Hotel Name', 'Overall Rating', 'Pincode'])
    counter = 1
    for i in data:
        writer.writerow([
            str(counter), i["name"], i["overall_rating"], i["address"][-5:]
        ])
        counter = counter + 1

