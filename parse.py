import csv
import json

catalog_file = 'SampleCSV.csv'

parsed_data = []
with open(catalog_file, mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        parsed_data.append({
            "Genus": row["genus"],
            "Mass (g)": float(row["mass(g)"]),
            "Name": row["name"],
            "Geological Location": row["geological location"],
            "Population Size": int(row["population size"].replace(",", "")),
            "Endangered": row["endangered"].upper() == "TRUE"
        })

parsed_data_json = json.dumps(parsed_data, indent=4)

print("Parsed Data:")
print(parsed_data_json)

json_file = 'catalog.json'
with open(json_file, mode='w') as file:
    file.write(parsed_data_json)

print(f"Parsed data saved to {json_file}.")

