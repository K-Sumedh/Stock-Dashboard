from django.db import models
from nsetools import Nse
from django.db import connection
from datetime import datetime, timedelta, date


def default_date():
    trade_date = datetime.utcnow()
    weekday = date.isoweekday(trade_date)
    # 6 = Saturday, 7 = Sunday
    if weekday == 6:
        trade_date = trade_date - timedelta(days=1)
    elif weekday == 7:
        trade_date = trade_date - timedelta(days=2)
    return trade_date

# Create your models here.
class Title(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class StockData(models.Model):
    nse = Nse()
    IndexData = []
    IndicesList = ['NIFTY 50', 'NIFTY NEXT 50', 'NIFTY MIDCAP 50', 'NIFTY BANK']

    def GetIndexData(self):
        for index in self.IndicesList:
            temp = self.nse.get_index_quote(index)
            self.IndexData.append(temp)

        print(self.IndexData)
        return self.IndexData

    def GetStockDataForUser(self, username):
        toSend = {}
        # for i in symbols:
        #     data =  self.nse.get_quote(i, as_json=False)
        #     ReqStockData = {
        #         "symbol": data["symbol"],
        #         "companyName": data["companyName"],
        #         "open": data["open"],
        #         "dayHigh": data["dayHigh"],
        #         "dayLow": data["dayLow"],
        #         "previousClose": data["previousClose"],
        #         "LastPrice": data["lastPrice"],
        #         "pChange": data["pChange"],
        #     }
        #     toSend[i] = ReqStockData

        w = WatchlistPerUser()
        return w.GetWatchlistForUser(username)


class WatchlistPerUser(models.Model):
    username = models.CharField(max_length=50)
    stockCode = models.CharField(max_length=20)
    quantity = models.IntegerField(default=0)
    isWatchList = models.BooleanField(default=True)
    isOwned = models.BooleanField(default=True)
    trade_date = models.DateTimeField(default=default_date)
    trade_cost = models.IntegerField()

    def SaveToWatchList(self, WatchListData):
        print(WatchListData)
        count = 0
        for e in WatchlistPerUser.objects.all():
            print(e.username)
            count +=1
        print(count)

        with connection.cursor() as cursor:
            WatchListData.insert(0, count+1)
            cursor.execute("INSERT into StockDashboard_watchlistperuser VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", WatchListData)

    def GetWatchlistForUser(self, username):
        data = {}
        i = 0
        nse = Nse()
        for watchlist in WatchlistPerUser.objects.raw("select * from StockDashboard_watchlistperuser "+"where username = %s", [username]):
            #d = nse.get_quote(watchlist.stockCode, as_json=False)
            #profit = watchlist.quantity* (d["lastPrice"] - watchlist.trade_cost)
            temp = {
                "Stock Code" : watchlist.stockCode,
                "Quantity" : watchlist.quantity,
                "Average Price" : watchlist.trade_cost,
                "Total Cost" : watchlist.quantity * watchlist.trade_cost,
                #"Current Price" : d["lastPrice"],
                #"Profit/Loss" : profit
            }
            data[i] = temp
            i = i + 1
        return data

    def GetStockCodes(self, username):
        return self.stockCode







