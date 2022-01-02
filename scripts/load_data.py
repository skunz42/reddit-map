import boto3
import json

def fetch_json():
    geojson = None
    with open("../json/all.geojson") as json_file:
        geojson = json.load(json_file)
    return geojson

def dump_to_db(geojson):
    dynamo_db = boto3.resource('dynamodb', endpoint_url="http://dynamodb.us-east-2.amazonaws.com")
    table = dynamo_db.Table('map_subscribers')
    if geojson is not None:
        for f in geojson["features"]:
            name = f["properties"]["BASENAME"]
            response = table.put_item(
                Item = {
                    'subreddit': f["properties"]["subreddit"],
                    'dem': f["properties"]["dem_votes"],
                    'id': f["properties"]["id"],
                    'metro': f["properties"]["BASENAME"],
                    'rep': f["properties"]["rep_votes"],
                    'share': f["properties"]["is_shared"],
                    'subscribers': f["properties"]["subscribers"]
                }
            )
            print(f"Inserted {name}")
    else:
        print("Invalid JSON")

geo_data = fetch_json()
dump_to_db(geo_data)
