import requests
import json
import csv

msa_properties = {}

geoids = []

with open('urbanareas.csv', encoding="utf-8-sig") as props:
    csv_props = csv.reader(props, delimiter=',', quotechar='"')
    for line in csv_props:
        name = line[0]
        subreddit = line[1]
        cbsa_id = line[2]
        population = line[3]
        dem_votes = line[4]
        rep_votes = line[5]
        shared = line[6]

        msa_properties[cbsa_id] = {}
        msa_properties[cbsa_id]["subreddit"] = subreddit
        msa_properties[cbsa_id]["name"] = name
        msa_properties[cbsa_id]["population"] = population
        msa_properties[cbsa_id]["dem_votes"] = dem_votes
        msa_properties[cbsa_id]["rep_votes"] = rep_votes
        msa_properties[cbsa_id]["is_shared"] = shared

        geoids.append(cbsa_id)

url = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/CBSA/MapServer/8/query?where=CBSA%3D"
url2 = "&text=&objectIds=&time=&geometry=&geometryType=esriGeometryPolygon&inSR=&spatialRel=esriSpatialRelIntersects&distance=&units=esriSRUnit_Foot&relationParam=&outFields=&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&havingClause=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&historicMoment=&returnDistinctValues=false&resultOffset=&resultRecordCount=&returnExtentOnly=false&datumTransformation=&parameterValues=&rangeValues=&quantizationParameters=&featureEncoding=esriDefault&f=geojson"
    
geojson = {}
geojson["type"] = "FeatureCollection"
geojson["features"] = []

for g in geoids:
    print(g)
    full_url = url + g + url2
    resp = requests.get(full_url).json()

    resp["features"][0]["properties"]["id"] = g
    resp["features"][0]["properties"]["name"] = msa_properties[g]["name"]
    resp["features"][0]["properties"]["subreddit"] = msa_properties[g]["subreddit"]
    resp["features"][0]["properties"]["population"] = msa_properties[g]["population"]
    resp["features"][0]["properties"]["dem_votes"] = msa_properties[g]["dem_votes"]
    resp["features"][0]["properties"]["rep_votes"] = msa_properties[g]["rep_votes"]
    resp["features"][0]["properties"]["is_shared"] = msa_properties[g]["is_shared"]
    resp["features"][0]["properties"]["subscribers"] = 0

    geojson["features"].append(resp["features"][0])

f = open('all.geojson', 'w+')
f.write(json.dumps(geojson))
f.close()

