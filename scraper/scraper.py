import requests
import os
import sys
import boto3

def set_up_db_creds(filename):
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    fullpath = os.path.join(fileDir, filename)

    i = 0
    f = open(fullpath)

    host = user = password = dbname = user_agent = ""

    for line in f:
        if i == 0:
            username = line.rstrip()
        elif i == 1:
            password = line.rstrip()
        elif i == 2:
            pub_id = line.rstrip()
        elif i == 3:
            secret = line.rstrip()
        elif i == 4:
            user_agent = line.rstrip()
        i += 1
    f.close()

    return {'user': username, 'password': password, 'id': pub_id, 'secret': secret, 'user-agent': user_agent}

def fetch_token(auth):
    headers = {'User-Agent': auth['user-agent']}
    endpoint_url = "https://www.reddit.com/api/v1/access_token"
    auth_obj = requests.auth.HTTPBasicAuth(auth['id'], auth['secret'])
    login_data = {'grant_type': 'password',
                  'username': auth['user'],
                  'password': auth['password']}

    res = requests.post(endpoint_url, auth=auth_obj, data=login_data, headers=headers)
    token = res.json()['access_token']
    headers = {**headers, **{'Authorization':f"bearer {token}"}}
    return headers

def get_subscribers(metros, headers):
    print("Getting data from Reddit API...")
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://dynamodb.us-east-2.amazonaws.com')
    table = dynamodb.Table('map_subscribers')
    response = table.scan(AttributesToGet=['subreddit', 'id', 'share', 'metro'])
    for r in response['Items']:
        sub = r['subreddit']
        city = r['id']
        share = float(r['share'])
        metro_name = r['metro']
        reddit_response = requests.get(f'https://oauth.reddit.com/r/{sub}/about', headers=headers)
        subscribers = reddit_response.json()['data']['subscribers']
        metros[city] = (int(subscribers*(share/100.0)), sub, metro_name)

    print("Updating db...")
    
    for cid in metros:
        table.update_item(
            Key = {
                'id': cid,
                'metro': metros[cid][2]
            },
            UpdateExpression="set subscribers=:s",
            ExpressionAttributeValues={
                ':s': metros[cid][0]
            }
        )

    print("Db updated")

def main():
    if len(sys.argv) != 2:
        print("Need one argument")
        sys.exit(1)

    filename = sys.argv[1]

    auth = set_up_db_creds(filename)

    headers = fetch_token(auth)

    metros = {}
    get_subscribers(metros, headers)
    # update_json()

main()
