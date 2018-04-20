#!/usr/bin/env/ python3

import json
from pymongo import MongoClient
import datetime

class UserData(object):
    """Back end for user wallet"""

    #Pull user info from the database
    def Connect(self, userData):
    
        self.mongoClient = MongoClient("mongodb://colea:PW@cluster01-shard-00-00-oheid.mongodb.net:27017,cluster01-shard-00-01-oheid.mongodb.net:27017,cluster01-shard-00-02-oheid.mongodb.net:27017/admin?replicaSet=Cluster01-shard-0&ssl=true")
        #self.mongoClient = MongoClient("mongodb://colea:PW@userwallet-shard-00-00-2tbmf.mongodb.net:27017,userwallet-shard-00-01-2tbmf.mongodb.net:27017,userwallet-shard-00-02-2tbmf.mongodb.net:27017/admin?replicaSet=UserWallet-shard-0&ssl=true")
        
        #Search for user
        self.mongoDB = self.mongoClient['user']
        self.userData = self.mongoDB.wallet.find_one({'email':userData['email']})	
        if self.userData is None:
            print("User doesn't exist")
            exit (1)
            
        else: #Retrieve user data
            userInfo = self.userData
            print("User's Data: ", userInfo['email'], "and", userInfo['cryptocurrencies'], "\n")


    #Check database for cryptocurrencies in buy/sell list
    def CheckTradePairBalance(self, userData, tradepair):
        #self.mongoDB = self.mongoClient['user']
        userInfo = self.mongoDB['wallet'].find_one({'$and':[{'email':userData['email']},{tradepair: {'$exists': True}}]})
        if userInfo is None:
            #print("Balance doesn't exist")
            tradepairBalance = 0
            
        else:
            tradepairBalance = userInfo[tradepair]

        print("Cryptocurrency Balance: ", tradepairBalance)
        return tradepairBalance


    #Calculate total wallet value in bitcoin
    def CalculateTotalWorth(self, userData, cuGet):
        userInfo = self.mongoDB.wallet.find_one({'email':userData['email']})	
        #self.userInfo = self.userData
        self.mongoDB2 = self.mongoClient['tradepairs'] #access tradepairs database

        total = 0
        #Get cryptocurrency and balances separately from balances array
        for i in range(len(userInfo['cryptocurrencies'])):
            for coin,balance in userInfo['cryptocurrencies'][i].items():
                #print("{}".format(coin))
                #print("{}".format(balance))

                #Get tradepair database doc using currency name
                tradepairDoc = self.mongoDB2['tradepairs'].find_one({'Currency':coin})
                print(tradepairDoc)

                #Get tradepair label from tradepair database
                if coin != 'Bitcoin':
                    cryptocurrencyId = tradepairDoc['Id']
                    print("Tradepair: ", cryptocurrencyId)

                    #Access market data
                    self.cryptopiauserGet = cuGet
                    tradepairMarketData = self.cryptopiauserGet.CurrentMarketData(cryptocurrencyId)
                    cryptoPriceInBitcoin = tradepairMarketData['Data']['LastPrice']
                    print("Price: ", tradepairMarketData['Data']['LastPrice'])

                    #Bitcoin conversion
                    bitcoinTradeBalance = balance * cryptoPriceInBitcoin
                    print("bitcointradebalance: ", bitcoinTradeBalance)

                    #Update holdings object
                    userInfo['holdings'][coin] = bitcoinTradeBalance

                    self.mongoDB.wallet.update(
                    {
                        'email': userInfo['email']
                    },{
                        '$set':
                        {
                            'holdings': userInfo['holdings']
                        }
                    })

                    
                    #Calculate trade fee
                    tradeFeePercent = tradepairDoc['TradeFee'] #~0.20% BTC
                    tradeFee = bitcoinTradeBalance * (tradeFeePercent * .01)
                    print("Fee: ", tradeFee)

                    #Bitcoin final balance for cryptocoin
                    bitcoinNewTradeBalance = bitcoinTradeBalance - tradeFee
                    print("New Bitcoin Trade Balance: ", bitcoinNewTradeBalance,"\n")

                else:
                    bitcoinNewTradeBalance = balance
                    
            dateTime = datetime.datetime.now()
            timestamp = dateTime.strftime("%m-%d-%Y %H:%M:%S")
            total = round(total, 8) + round(bitcoinNewTradeBalance, 8)
            print("Subtotal: ", total, "\n")

        #Calculate bitcoin cashout minus withdrawal fee
        cashout = total - .001
        print("Cashout: ", cashout, "\n")

        #Update database
        self.mongoDB.wallet.update({'email':userData['email']},{'$set':{'cashout':cashout}})

        #Update cashoutHistoryArray
        if len(userInfo['cashoutHistory']) == 0:
            cashoutHistoryArrayNumber = str(0)
            self.mongoDB.wallet.update({'email':userData['email']},{'$set':{'cashoutHistory.' + cashoutHistoryArrayNumber:{'Time':timestamp, 'Cashout':.999}}})
        else:
            cashoutHistoryArrayNumber = str(len(userInfo['cashoutHistory']))
            self.mongoDB.wallet.update({'email':userData['email']},{'$set':{'cashoutHistory.' + cashoutHistoryArrayNumber:{'Time':timestamp, 'Cashout':cashout}}})


        #Update holdings object
        userInfo['holdings']['Bitcoin'] = cashout

        self.mongoDB.wallet.update(
                {
                    'email': userInfo['email']
                },{
                '$set':
                    {
                    'holdings': userInfo['holdings']
                    }
         })

    #Receive buy/sell input
    def Trade(self, userData, tradepair, action, cuGet):
        self.mongoDB2 = self.mongoClient['tradepairs'] #access tradepairs database
        tradepairDoc = self.mongoDB2['tradepairs'].find_one({'Id':int(tradepair)})

        userInfo = self.mongoDB.wallet.find_one({'email':userData['email']})	        
        #self.userInfo = self.userData
        bitcoinBalance = userInfo['bitcoinBalance']
        tradepairBalance = self.CheckTradePairBalance(userData, tradepair)

        if action == 1: #Buy
            if bitcoinBalance == 0:
                print("Unable to make purchase: Insufficient bitcoin balance")

            else:
                #Get currency name from tradepair database
                cryptocurrency = tradepairDoc['Currency']
                print("Cryptocurrency to Buy: ", cryptocurrency)
                
                #Access market data
                self.cryptopiauserGet = cuGet
                tradepairMarketData = self.cryptopiauserGet.CurrentMarketData(tradepair)
                dateTime = datetime.datetime.now()
                timestamp = dateTime.strftime("%m-%d-%Y %H:%M:%S")                
                cryptoPriceInBitcoin = tradepairMarketData['Data']['LastPrice']
                print("Price: ", tradepairMarketData['Data']['LastPrice'])

                #Process trade
                print("Presale bitcoin balance:", bitcoinBalance)
                bitcoinTradeAmount = .05 * bitcoinBalance
                print("Trade amount:", bitcoinTradeAmount)
                cryptoTradeBalance = bitcoinTradeAmount/cryptoPriceInBitcoin
                print("Cryptocurrency Purchased: ",cryptoTradeBalance)

                #Cryptocoin buy
                if tradepairBalance == 0:
                    newBalance = True
                else:
                    newBalance = False
                    oldBalance = tradepairBalance 
                tradepairBalance = cryptoTradeBalance + tradepairBalance
                print("New Cryptocurrency Balance: ",tradepairBalance)

                #Calculate trade fee
                tradeFeePercent = tradepairDoc['TradeFee']
                tradeFee = bitcoinTradeAmount * (tradeFeePercent * .01)
                print("Fee: ", tradeFee)
                
                #Bitcoin sale
                bitcoinBalance = bitcoinBalance - bitcoinTradeAmount - tradeFee
                print("New Bitcoin Balance: ", bitcoinBalance,"\n")
                
                #Update balances in database
                self.mongoDB.wallet.update({'email':userData['email']},{'$set':{tradepair:tradepairBalance,'bitcoinBalance':bitcoinBalance}})
                
                #Balances array
                cryptocurrencyArrayNumber = str(0)
                self.mongoDB.wallet.update({'email':userData['email']},{'$set':{'cryptocurrencies.' + cryptocurrencyArrayNumber:{'Bitcoin':bitcoinBalance}}})
                if newBalance == True: #add cryptocurrency entry
                    cryptocurrencyArrayNumber = str(len(userInfo['cryptocurrencies']))
                    self.mongoDB.wallet.update({'email':userData['email']},{'$set':{'cryptocurrencies.' + cryptocurrencyArrayNumber:{cryptocurrency:tradepairBalance}}})
                else: #update balance
                    for i in range(len(userInfo['cryptocurrencies'])):
                        if cryptocurrency in userInfo['cryptocurrencies'][i]:
                            cryptocurrencyArrayNumber = str(i)
                            self.mongoDB.wallet.update({'email':userData['email']},{'$set':{'cryptocurrencies.' + cryptocurrencyArrayNumber:{cryptocurrency:tradepairBalance}}})
                            
	        	#Update trade history
                tradeArrayNumber = str(len(userInfo['trades']))
                self.mongoDB.wallet.update({'email':userData['email']},{'$set':{'trades.' + tradeArrayNumber:{'Trade': 'Buy','Cryptocurrency':cryptocurrency, 'Sell':bitcoinTradeAmount, 'Buy':cryptoTradeBalance, 'Price':cryptoPriceInBitcoin, 'Fee':tradeFee, 'Timestamp':timestamp}}})

                
        elif action == -1: #Sell
            if tradepairBalance > 0: #If user has that cryptocurrency
                oldBalance = tradepairBalance

                #Get currency name from tradepair database
                cryptocurrency = tradepairDoc['Currency']
                print("Cryptocurrency to Sell: ", cryptocurrency)

                #Access market data
                self.cryptopiauserGet = cuGet
                tradepairMarketData = self.cryptopiauserGet.CurrentMarketData(tradepair)
                dateTime = datetime.datetime.now()
                timestamp = dateTime.strftime("%m-%d-%Y %H:%M:%S")
                cryptoPriceInBitcoin = tradepairMarketData['Data']['LastPrice']
                print("Price: ", tradepairMarketData['Data']['LastPrice'])

                #Process trade - cryptocoin sale
                bitcoinTradeBalance = tradepairBalance * cryptoPriceInBitcoin
                tradepairBalance = 0
                print("New Cryptocurrency Balance: ",tradepairBalance)

                #Calculate trade fee
                tradeFeePercent = tradepairDoc['TradeFee']
                tradeFee = bitcoinTradeBalance * (tradeFeePercent * .01)
                print("Fee: ", tradeFee)

                #Bitcoin buy
                bitcoinBalance = bitcoinBalance + bitcoinTradeBalance - tradeFee
                print("New Bitcoin Balance: ", bitcoinBalance,"\n")

                #Update balances in database
                self.mongoDB.wallet.update({'email':userData['email']},{'$set':{'bitcoinBalance':bitcoinBalance}})
                self.mongoDB.wallet.update({'email':userData['email']},{'$unset':{tradepair:tradepairBalance,}})

                #Balances array
                self.mongoDB.wallet.update({'email':userData['email']},{'$set':{'cryptocurrencies.0':{'Bitcoin':bitcoinBalance}}})
                self.mongoDB.wallet.update({'email':userData['email']},{'$pull':{'cryptocurrencies':{cryptocurrency:oldBalance}}})

                #Update holdings object
                userInfo['holdings'].pop(cryptocurrency, oldBalance)
                self.mongoDB.wallet.update(
                    {
                        'email': userData['email']
                    },{
                        '$set':
                        {
                            'holdings': userInfo['holdings']
                        }
                    })


                #Update trade history
                tradeArrayNumber2 = str(len(userInfo['trades']))
                self.mongoDB.wallet.update({'email':userData['email']},{'$set':{'trades.'+ tradeArrayNumber2: {'Trade':'Sell','Cryptocurrency':cryptocurrency,'Buy':bitcoinTradeBalance, 'Sell': oldBalance, 'Price':cryptoPriceInBitcoin, 'Fee':tradeFee, 'Timestamp':timestamp}}})
            else:
                #Get currency name from tradepair database
                cryptocurrency = tradepairDoc['Currency']
                print("No {} to sell.\n".format(cryptocurrency))

        elif action != 1 and action != -1:
            print("Error-Action can only be 1 or -1")
            exit(1)
