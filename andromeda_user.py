#!/usr/bin/env/ python3

import json
from pymongo import MongoClient

from userdata import UserData
from cryptopiauserget import CryptopiaUserGet
from userdatabase import CreateUser

#mongoClient = MongoClient("mongodb://colea:PW@userwallet-shard-00-00-2tbmf.mongodb.net:27017,userwallet-shard-00-01-2tbmf.mongodb.net:27017,userwallet-shard-00-02-2tbmf.mongodb.net:27017/admin?replicaSet=UserWallet-shard-0&ssl=true")

mongoClient = MongoClient("mongodb://colea:PW@cluster01-shard-00-00-oheid.mongodb.net:27017,cluster01-shard-00-01-oheid.mongodb.net:27017,cluster01-shard-00-02-oheid.mongodb.net:27017/admin?replicaSet=Cluster01-shard-0&ssl=true")

userData = UserData()
    
cuGet = CryptopiaUserGet()

createUser = CreateUser()

#createUser.Insert()

#createUser.AddNewUser()
#createUser.AddMultipleUsers()



#run wallet
mongoDB = mongoClient['user']

users = mongoDB['wallet'].find({}, {'email':1, '_id':0}) #array of user emails
#loop

for user in users:
    for email,address in user.items():
        userData.Connect(
        {
            "email":address       
        })

        userData.Trade(
        {
           "email":address
        }, "1494", -1, cuGet)

users = mongoDB['wallet'].find({}, {'email':1, '_id':0}) #array of user emails
#loop
for user in users:
    for email,address in user.items():
        userData.Connect(
        {
            "email":address       
        })

        userData.CalculateTotalWorth(
        {
            "email":address
        }, cuGet)

"""
userData.Connect(
    {
        "email":"acraft@gmail.com"
    })


#test
#userData.CalculateTotalWorth({"email":"acole@gmail.com"}, cuGet)
    


#machine learning input - possibly every epoch (5 min)
tradeOrderList = [("105", 1), ("5203", 1), ("101", 1), ("1494", 1), ("102", 1)]
tradeOrderDict = dict(tradeOrderList)

for key, value in tradeOrderDict.items():
    userData.Trade({
    "email":"acraft@gmail.com"
    }, key, value, cuGet)


userData.Connect(
    {
        "email":"acraft@gmail.com"
    })

userData.CalculateTotalWorth(
        {
            "email":"acraft@gmail.com"
        }, cuGet)

#userData.Trade(
#    {
#        "email":"acraft@gmail.com"
#    }, "1626", 1, cuGet)
"""

