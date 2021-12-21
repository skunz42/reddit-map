import csv
import json

msa_properties = {}

with open('../data/urbanareas.csv', encoding='utf-8-sig') as props:
    csv_props = csv.reader(props, delimiter=',', quotechar='"')
    for line in csv_props:
        cbsa_id = line[2]
        dem_votes = line[4]
        rep_votes = line[5]
        
        msa_properties[cbsa_id] = {}
        msa_properties[cbsa_id]["dem_votes"] = dem_votes
        msa_properties[cbsa_id]["rep_votes"] = rep_votes

with open('../json/all.geojson') as geojson:
    data = json.load(geojson)
    for i, k in enumerate(data["features"]):
        cbsa_id = data['features'][i]['properties']['id']
        dvotes = msa_properties[cbsa_id]['dem_votes']
        rvotes = msa_properties[cbsa_id]['rep_votes']
        data['features'][i]['properties']['dem_votes'] = dvotes
        data['features'][i]['properties']['rep_votes'] = rvotes

f = open('all.geojson', 'w+')
f.write(json.dumps(data))
f.close()
