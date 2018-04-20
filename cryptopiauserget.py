import json
from urllib.request import urlopen 
from pymongo import MongoClient

class CryptopiaUserGet(object):
    """Get Current TradePair Price"""

    def FetchURL(self, url):
        retries = 50
        while True:
            try:
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
            except:
                retries -= 1
                if retries == 0:
                    return None
                continue
                
                
    def CurrentMarketData(self, tradepair):
        url = "https://www.cryptopia.co.nz/api/GetMarket/{}".format(tradepair)
        response = self.FetchURL(url)
        return response
