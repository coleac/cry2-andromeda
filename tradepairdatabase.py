#!/usr/bin/env/ python3

from pymongo import MongoClient
import json
from urllib.request import urlopen

#Get data from Cryptopia API
def FetchURL(url):
    retries = 5
    while True:
        response = urlopen(url).read().decode('utf')
        result = json.loads(response)
        if result is None:
            retries -= 1
            if retries == 0:
               return None
            continue
        if not result['Success']:
            print("Error")
        else:
            return result


closedMarkets = ['NZDT', 'USDT', 'LTC', 'DOGE']
response = FetchURL('https://www.cryptopia.co.nz/api/GetTradePairs')
response['Data'] = list(filter(lambda x: x['Label'].split('/')[-1] not in closedMarkets, response['Data']))

#Connect to MongoDB - Note: Change connection string as needed
#client = MongoClient("mongodb://colea:PW@userwallet-shard-00-00-2tbmf.mongodb.net:27017,userwallet-shard-00-01-2tbmf.mongodb.net:27017,userwallet-shard-00-02-2tbmf.mongodb.net:27017/admin?replicaSet=UserWallet-shard-0&ssl=true")
client = MongoClient("mongodb://colea:PW@cluster01-shard-00-00-oheid.mongodb.net:27017,cluster01-shard-00-01-oheid.mongodb.net:27017,cluster01-shard-00-02-oheid.mongodb.net:27017/admin?replicaSet=Cluster01-shard-0&ssl=true")

db=client.tradepairs

#Insert multiple user object directly into MongoDB via insert
for crypto in response['Data']:
	db.tradepairs.insert_one(crypto)

#Tell us that you are done
print("finished")
