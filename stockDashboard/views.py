from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def HomePage(request):
    logout(request)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = request.POST["Email_SI"]
            pwd = request.POST['Password_SI']
            user = authenticate(username=username, password=pwd)
            login(request, user)
            if user != None:
                if user.is_authenticated:
                    resp = redirect(DashboardForUser, username)
                    return resp

            else:
                form = LoginForm()
                messages.error(request, "Email or password is incorrect.")
                return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def ShowStockData(request):

    stock = StockData()
    symbols = ["TATASTEEL"]
    content = { "data" : stock.GetStockData(symbols)}
    print(content)

    return render(request, "dashboard.html", content)

@login_required
def DashboardForUser(request, username):
    stockList = []
    stockTotal = []
    stock = StockData()
    IndexData = stock.GetIndexData()

    querySet = WatchlistPerUser.objects.filter(username=username)
    for row in querySet:
        stockList.append(row.stockCode)
    for row in querySet:
        stockTotal.append(row.quantity * row.trade_cost)

    content = {
        "data" : stock.GetStockDataForUser(username),
        "IndexData" : IndexData,
        "StockList" : stockList,
        "StockTotal" : stockTotal,
    }

    return render (request, "dashboard.html",content)

def SignUpView(request):

    if request.method == 'POST':
        print("1")
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            print("2")
            return redirect(HomePage)
        else:
            print("3")
            messages.error(request, 'Invalid Input')
            return render(request, "signup.html", {'form': form})
    else:
        form = SignUpForm()
        print("4")
        return render(request, "signup.html", {'form': form})


def Logout(request):
    logout(request)
    print("logging out")
    return redirect('home')

@login_required
def Watchlist(request, username):
    if request.method == 'POST':
        form = WatchListForm(request.POST)
        if form.is_valid():
            WatchListData = []
            ticker = form.cleaned_data['ticker']
            TradeDate = form.cleaned_data['trade_Date']
            Price = form.cleaned_data['Price']
            #Comment = form.cleaned_data['Comment']
            Quantity = form.cleaned_data['Quantity']

            WatchListData.append(username)
            WatchListData.append(ticker)
            WatchListData.append(Quantity)
            WatchListData.append(True)
            WatchListData.append(True)
            WatchListData.append(TradeDate)
            WatchListData.append(Price)

            w = WatchlistPerUser()
            w.SaveToWatchList(WatchListData)

    elif request.method == 'GET':
        form = WatchListForm()

    WL = WatchlistPerUser()
    WL_data = WL.GetWatchlistForUser(username)
    if len(WL_data) == 0:
        count = 0
    else:
        count = 1
    stock = StockData()

    content = {
        'form': form,
        'count': count,
        "data": stock.GetStockDataForUser(username)
    }

    return render(request, "watchlist.html", content)

def MarketResearch(request, username):
    nse = Nse()

    stock = StockData()
    IndexData = stock.GetIndexData()

    if request.method == 'POST':
        form = Search(request.POST)
        if form.is_valid():
            code = form.cleaned_data['search']
            if nse.is_valid_code(code):
                data = nse.get_quote(code, as_json=False)

                ReqStockData = []
                ReqStockData.append(data["symbol"])
                ReqStockData.append(data["companyName"])
                ReqStockData.append(data["open"])
                ReqStockData.append(data["dayHigh"])
                ReqStockData.append(data["dayLow"])
                ReqStockData.append(data["previousClose"])
                ReqStockData.append(data["lastPrice"])
                ReqStockData.append(data["pChange"])
                content={
                    "count" : 1,
                    "data" : ReqStockData,
                    "form" : form,
                }
            else:
                messages.error(request, "Invalid Code.Please enter correct code.")
                content = {
                    "count" : 0,
                    "form" : form,
                }
        else:
            messages.error(request, "Invalid Input.")

    else:       #GET
        form = Search()
        content = {
            "count" : 0,
            "form" : form,
        }

        content['IndexData'] = IndexData
    return render(request, "marketResearch.html", content)

#@login_required
def GainersLosers(request,username):
    print("GainersLosers Data")
    nse = Nse()
    TopGainers = nse.get_top_gainers(as_json=False)[:5]
    TopLossers = nse.get_top_losers(as_json=False)[:5]
    content = {
        'TopLosers' : TopLossers,
        'TopGainers': TopGainers,
    }
    print(TopGainers[0])
    print(TopLossers[0])
    return render(request, "GainersLosers.html", content)

def homeNew(request):
    print("Portfolio Management System")
    return render(request, "homeNew.html")

