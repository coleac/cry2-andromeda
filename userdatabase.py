#!/usr/bin/env/ python3

from pymongo import MongoClient

class CreateUser(object):

    def AddNewUser(self):
        #Connect to MongoDB - Note: Change connection string as needed
        #client = MongoClient("mongodb://colea:PW@userwallet-shard-00-00-2tbmf.mongodb.net:27017,userwallet-shard-00-01-2tbmf.mongodb.net:27017,userwallet-shard-00-02-2tbmf.mongodb.net:27017/admin?replicaSet=UserWallet-shard-0&ssl=true")
        
        client = MongoClient("mongodb://colea:PW@cluster01-shard-00-00-oheid.mongodb.net:27017,cluster01-shard-00-01-oheid.mongodb.net:27017,cluster01-shard-00-02-oheid.mongodb.net:27017/admin?replicaSet=Cluster01-shard-0&ssl=true")

        #database name: user
        db=client.user

        
        #Create user data (pending integration with website
        newuser = {        
	        "email":"acraft@gmail.com",
	        "firstName":"Aalon",
    	    	"lastName":"Cole",
        	"bitcoinBalance":1,
		"cryptocurrencies":[{'Bitcoin':1}],
		"trades":[{"Account Open": "1 bitcoin"}],
            	"holdings":{'Bitcoin':1},
            	"cashoutHistory":[],
            	"cashout":1
        }

        db.wallet.insert_one(newuser)

        #Tell us that you are done
        print("finished")


    def AddMultipleUsers(self):
        #client = MongoClient("mongodb://colea:PW@userwallet-shard-00-00-2tbmf.mongodb.net:27017,userwallet-shard-00-01-2tbmf.mongodb.net:27017,userwallet-shard-00-02-2tbmf.mongodb.net:27017/admin?replicaSet=UserWallet-shard-0&ssl=true")
        
        client = MongoClient("mongodb://colea:PW@cluster01-shard-00-00-oheid.mongodb.net:27017,cluster01-shard-00-01-oheid.mongodb.net:27017,cluster01-shard-00-02-oheid.mongodb.net:27017/admin?replicaSet=Cluster01-shard-0&ssl=true")
        
        #database name: user
        db=client.user

        #Insert multiple user object directly into MongoDB via insert
        db.wallet.insert([
	    {
		    "email":"acole@gmail.com",
		    "firstName":"Aalon",
		    "lastName":"Cole",
		    "bitcoinBalance":1,
		    "cryptocurrencies":[{'Bitcoin':1}],
		    "trades":[{"Account Open": "1 bitcoin"}],
            "cashout":1
        },
	    {
		    "email":"gcastle@gmail.com",
		    "firstName":"Gus",
		    "lastName":"Castle",
		    "bitcoinBalance":1,
		    "cryptocurrencies":[{'Bitcoin':1}],
		    "trades":[{"Account Open": "1 bitcoin"}],
            "cashout":1
	    }])

        #Tell us that you are done
        print("finished")

    def Insert(self):
         #client = MongoClient("mongodb://colea:PW@userwallet-shard-00-00-2tbmf.mongodb.net:27017,userwallet-shard-00-01-2tbmf.mongodb.net:27017,userwallet-shard-00-02-2tbmf.mongodb.net:27017/admin?replicaSet=UserWallet-shard-0&ssl=true")
         client = MongoClient("mongodb://colea:PW@cluster01-shard-00-00-oheid.mongodb.net:27017,cluster01-shard-00-01-oheid.mongodb.net:27017,cluster01-shard-00-02-oheid.mongodb.net:27017/admin?replicaSet=Cluster01-shard-0&ssl=true")
         
         #database name: user
         db=client.user
         db.wallet.update({},{"$set": {"cashoutHistory":[]}}, upsert=False, multi=True)
         db.wallet.update({},{"$set": {"holdings":{'Bitcoin':1}}}, upsert=False, multi=True)
