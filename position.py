from utility.datetime import GetDateTime
from utility.jsonagent import GetJson, SaveJson
import os

"""dict = {
    "fund_name": "jijin",
    "average_price": 2.3,
    "sum_volume": 6.2,
    "avail_volume": 3.1,
    "history":
    {
        2022*365+5*31+5:
        {
            "price": 2.3,
            "volume": 3.1,
        },
        2022*365+5*31+5:
        {
            "price": 2.3,
            "volume": 3.1,
        },
    }
}"""


class Position:
    def __init__(self, user_key, fund_name):
        self.__user_key = user_key
        self.__fund_name = fund_name
        self.__path = "./database/{}".format(user_key)
        self.__filename = "./database/{}/{}.json".format(user_key, fund_name)
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)
        if not os.path.exists(self.__filename):
            dict = {
                "fund_name": fund_name,
                "average_price": 0.0,
                "sum_volume": 0.0,
                "avail_volume": 0.0,
                "history": {},
            }
            SaveJson(dict, self.__filename)

    def Add(self, price, volume, datetime=GetDateTime()):
        data = GetJson(self.__filename)
        data["average_price"] = (
            price*volume + data["average_price"]*data["sum_volume"]) / (data["sum_volume"] + volume)
        data["sum_volume"] += volume
        data["history"][str(datetime)] = {
            "price": price,
            "volume": volume,
        }
        SaveJson(data, self.__filename)

    def Remove(self,datetime):
        data = GetJson(self.__filename)
        price=data["history"][str(datetime)]["price"]
        volume=data["history"][str(datetime)]["volume"]
        if (data["sum_volume"] - volume)<0.0001:
            data["average_price"]=0.0
            data["sum_volume"] =0.0
        else:
            data["average_price"] = (
                data["average_price"]*data["sum_volume"] - price*volume) / (data["sum_volume"] - volume)
            data["sum_volume"]-=volume
        data["history"].pop(str(datetime))
        SaveJson(data, self.__filename)