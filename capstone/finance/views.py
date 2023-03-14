from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django import forms
import datetime
import yfinance as yf

from .models import User, Share


class shareForm(forms.Form):
    ticker = forms.CharField(label="Ticker:", widget=forms.TextInput(attrs={"class": "form-control"}))


class currencyForm(forms.Form):
    amount = forms.DecimalField(label="Amount", max_digits=15, decimal_places=5, initial=1, widget=forms.TextInput(attrs={"class": "form-control"}))
    currency_from = forms.CharField(label="From Currency", widget=forms.TextInput(attrs={"class": "form-control"}))
    currency_to = forms.CharField(label="To Currency", widget=forms.TextInput(attrs={"class": "form-control"}))


class addShareForm(forms.Form):
    ticker = forms.CharField(label="Ticker", widget=forms.TextInput(attrs={"class": "form-control"}))
    value = forms.DecimalField(label="Value", max_digits=15, decimal_places=5, widget=forms.TextInput(attrs={"class": "form-control"}))
    amount = forms.DecimalField(label="Amount", max_digits=25, decimal_places=5, widget=forms.TextInput(attrs={"class": "form-control"}))
    timestamp = forms.DateTimeField(initial=datetime.datetime.today, widget=forms.TextInput(attrs={"class": "form-control"}))
    

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "finance/login.html", {
                "message_bad": "Invalid username and/or password"
            })
    else:
        return render(request, "finance/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "finance/register.html", {
                "message_bad": "Passwords do not match"
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "finance/register.html", {
                "message_bad": "Username already taken"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "finance/register.html")


def index(request):
    return render(request, "finance/index.html")


def calculator(request):    
    return render(request, "finance/calculator.html")


def currency(request):
    if request.method == "POST":
        form = currencyForm(request.POST)
        if form.is_valid():
            # Get values from form and convert to correct format
            amount = form.cleaned_data["amount"]
            currency_from = form.cleaned_data["currency_from"]
            currency_to = form.cleaned_data["currency_to"]
            conversion = currency_from.upper() + currency_to.upper() + "=X"
            obj = yf.Ticker(conversion)
            try:
                info = obj.fast_info
                info["lastPrice"]
            except:
                return render(request, "finance/currency.html", {
                    "message_bad": "Currency pair not supported",
                    "form": form,
                })
            # Get information on currency pair
            infoDict = {
                "Currency": info["currency"],
                "Rate": round(info["lastPrice"], 4),
                "50 Day Average": round(info["fiftyDayAverage"], 4),
                "200 Day Average": round(info["twoHundredDayAverage"], 4),
                "Year Change": str(round(info["yearChange"] * 100, 4)) + "%",
                "Year Low": round(info["yearLow"], 4),
                "Year High": round(info["yearHigh"], 4),
            }
            # Calculate conversion
            conversion = round(float(amount) * info["lastPrice"], 4)
            return render(request, "finance/currency.html", {
                "info": infoDict,
                "conversion": conversion,
                "form": form,
            })
        else:
            return render(request, "finance/currency.html", {
                "message_bad": "An error ocurred - please try again",
                "form": form
            })
    else:
        return render(request, "finance/currency.html", {
            "form": currencyForm(),
        })


def shares(request):
    if request.method == "POST":
        form = shareForm(request.POST)
        if form.is_valid():
            # Get value from form
            ticker = form.cleaned_data["ticker"]
            obj = yf.Ticker(ticker)
            try:
                info = obj.fast_info
                info["lastPrice"]
            except:
                return render(request, "finance/shares.html", {
                    "message_bad": "Please input a valid ticker",
                    "form": form,
                })
            # Get information on share
            infoDict = {
                "Currency": info["currency"],
                "Price": round(info["lastPrice"], 4),
                "50 Day Average": round(info["fiftyDayAverage"], 4),
                "200 Day Average": round(info["twoHundredDayAverage"], 4),
                "Year Change": str(round(info["yearChange"] * 100, 4)) + "%",
                "Year Low": round(info["yearLow"], 4),
                "Year High": round(info["yearHigh"], 4),
            }
            return render(request, "finance/shares.html", {
                "info": infoDict,
                "form": form,
            })
        else:
            return render(request, "finance/shares.html", {
                "message_bad": "An error ocurred - please try again",
                "form": form,
            })
    else:
        return render(request, "finance/shares.html", {
            "form": shareForm(),
        })


@login_required
def transactions(request):
    # Get current user transactions and information
    def get_transactions():
        transactions_queryset = Share.objects.all().filter(user=request.user)
        transactions = []
        for share in transactions_queryset:
            obj = yf.Ticker(share.ticker)
            try:
                info = obj.fast_info
                info["lastPrice"]
            except:
                # If unable to obtain information regarding previous (successful) transactions
                infoDict = {
                    "id": share.pk,
                    "Ticker": share.ticker.upper(),
                    "Price": "0",
                    "Amount": "0",
                    "Original Value": "0",
                    "Current Value": "0",
                    "Change": "0",
                    "Currency": "Error",
                }
                transactions.append(infoDict)
                continue
            infoDict = {
                "id": share.pk,
                "Ticker": share.ticker.upper(),
                "Price": round(info["lastPrice"], 5),
                "Amount": str(share.amount).rstrip("0").rstrip("."),
                "Original Value": str(share.value).rstrip("0").rstrip("."),
                "Current Value": str(round(float(share.amount) * info["lastPrice"], 2)).rstrip("0").rstrip("."),
                "Change": str(round(((((float(share.amount) * info["lastPrice"]) / float(share.value)) - 1) * 100), 2)) + "%",
                "Currency": info["currency"],
            }
            transactions.append(infoDict)
        return transactions
    # Function saved in memory for most renders
    transactions = get_transactions()
    
    if request.method == "POST":
        # Attempting to add a transaction
        form = addShareForm(request.POST)
        if form.is_valid():
            ticker = form.cleaned_data["ticker"]
            value = form.cleaned_data["value"]
            amount = form.cleaned_data["amount"]
            timestamp = form.cleaned_data["timestamp"]
            # Check if ticker valid
            obj = yf.Ticker(ticker)
            try:
                info = obj.fast_info
                info["lastPrice"]
            except:
                return render(request, "finance/transactions.html", {
                    "message_bad": "Please input a valid ticker",
                    "form": form,
                    "transactions": transactions,
                })
            # Check if value & amount are valid
            if value < 0 or value > 999999999999999:
                return render(request, "finance/transactions.html", {
                    "message_bad": "Please input a valid value amount",
                    "form": form,
                    "transactions": transactions,
                })
            elif amount < 0 or amount > 999999999999999999999:
                return render(request, "finance/transactions.html", {
                    "message_bad": "Please input a valid amount of shares",
                    "form": form,
                    "transactions": transactions,
                })
            # Try to add transaction
            try:
                transaction = Share(user=request.user, ticker=ticker, value=value, amount=amount, timestamp=timestamp)
                transaction.save()
            except:
                return render(request, "finance/transactions.html", {
                    "message_bad": "An error occured - please try again",
                    "form": form,
                    "transactions": transactions,
                })
            # Transaction added
            return render(request, "finance/transactions.html", {
                "message_good": "Successfully added transaction",
                "form": addShareForm(),
                "transactions": get_transactions(),
            })
        else:
            return render(request, "finance/transactions.html", {
                "message_bad": "An error ocurred - please try again",
                "form": form,
                "transactions": transactions,
            })
    else:
        return render(request, "finance/transactions.html", {
            "form": addShareForm(),
            "transactions": transactions,
        })


def delete_transaction(request):
    # Should not access view incorrectly
    if request.method != "POST":
        return HttpResponseRedirect(reverse("transactions"))
    # Get transaction id
    my_var = request.POST
    id = 0
    for item in my_var.keys():
        if item.isdigit():
            id = int(item)
    # Check that transaction is valid & belongs to user
    if id == 0:
        return HttpResponseRedirect(reverse("transactions"))
    transaction = Share.objects.get(pk=id)
    if request.user.pk != transaction.user.pk:
        return HttpResponseRedirect(reverse("transactions"))
    # Delete transaction
    transaction.delete()
    return HttpResponseRedirect(reverse("transactions"))


@login_required
def portfolio(request):
    # Get current user portfolio and information
    portfolio_queryset = Share.objects.all().filter(user=request.user)
    portfolio = []
    for share in portfolio_queryset:
        obj = yf.Ticker(share.ticker)
        try:
            info = obj.fast_info
            info["lastPrice"]
        except:
            # If unable to obtain information regarding previous (successful) transactions
            infoDict = {
                "Ticker": share.ticker.upper(),
                "Price": "0",
                "Amount": "0",
                "Original Value": "0",
                "Current Value": "0",
                "Change": "0",
                "Currency": "Error",
            }
            portfolio.append(infoDict)
            continue
        # Boolean indicates if share is already in portfolio or not
        in_port = False
        for dict in portfolio:
            if share.ticker.upper() in dict["Ticker"]:
                # Share already in portfolio - modify entry to include additional transaction
                if info["currency"] == "USD":
                    # No conversion necessary
                    dict["Amount"] = str(float(dict["Amount"]) + float(share.amount)).rstrip("0").rstrip(".")
                    dict["Original Value"] = str(round(float(dict["Original Value"]) + float(share.value), 5)).rstrip("0").rstrip(".")
                    dict["Current Value"] = str(round(float(dict["Amount"]) * info["lastPrice"], 2)).rstrip("0").rstrip(".")
                    dict["Change"] = str(round(((((float(dict["Amount"]) * info["lastPrice"]) / (float(dict["Original Value"]))) - 1) * 100), 2)) + "%"
                    in_port = True
                    break
                else:
                    # Conversion to USD necessary before including additional transaction
                    conversion = info["currency"] + "USD=X"
                    obj = yf.Ticker(conversion)
                    try:
                        currency_info = obj.fast_info
                        rate = currency_info["lastPrice"]
                    except:
                        continue
                    # Add converted transaction
                    dict["Amount"] = str(float(dict["Amount"]) + float(share.amount)).rstrip("0").rstrip(".")
                    dict["Original Value"] = str(round(float(dict["Original Value"]) + float(share.value) * rate, 5)).rstrip("0").rstrip(".")
                    dict["Current Value"] = str(round(float(dict["Amount"]) * info["lastPrice"] * rate, 2)).rstrip("0").rstrip(".")
                    dict["Change"] = str(round(((((float(dict["Current Value"])) / float(dict["Original Value"])) - 1) * 100), 2)) + "%"
                    in_port = True
                    break
        if not in_port:
            # Share not yet in portfolio - simply add transaction
            if info["currency"] == "USD":
                # No conversion necessary
                infoDict = {
                    "Ticker": share.ticker.upper(),
                    "Price": round(info["lastPrice"], 5),
                    "Amount": str(share.amount).rstrip("0").rstrip("."),
                    "Original Value": str(share.value).rstrip("0").rstrip("."),
                    "Current Value": str(round(float(share.amount) * info["lastPrice"], 2)).rstrip("0").rstrip("."),
                    "Change": str(round(((((float(share.amount) * info["lastPrice"]) / float(share.value)) - 1) * 100), 2)) + "%",
                    "Currency": info["currency"],
                }
                portfolio.append(infoDict)
            else:
                # Need to convert transaction to USD
                conversion = info["currency"] + "USD=X"
                obj = yf.Ticker(conversion)
                try:
                    currency_info = obj.fast_info
                    rate = currency_info["lastPrice"]
                except:
                    continue
                # Add converted transaction
                infoDict = {
                    "Ticker": share.ticker.upper(),
                    "Price": round(float(info["lastPrice"]) * rate, 5),
                    "Amount": str(share.amount).rstrip("0").rstrip("."),
                    "Original Value": str(round(float(share.value) * rate, 5)).rstrip("0").rstrip("."),
                    "Current Value": str(round(float(share.amount) * info["lastPrice"] * rate, 2)).rstrip("0").rstrip("."),
                    "Change": str(round(((((float(share.amount) * info["lastPrice"]) / float(share.value)) - 1) * 100), 2)) + "%",
                    "Currency": "USD*",
                }
                portfolio.append(infoDict)
    # Calculate totals
    totals = {
        "og_val": 0,
        "cur_val": 0,
        "change": "",
    }
    for infoDict in portfolio:
        totals["og_val"] += float(infoDict["Original Value"])
        totals["cur_val"] += float(infoDict["Current Value"])
    totals["change"] = str(round((totals["cur_val"] / totals["og_val"] - 1) * 100, 2)) + "%"
    totals["og_val"] = str(round(totals["og_val"], 2)).rstrip("0").rstrip(".")
    totals["cur_val"] = str(round(totals["cur_val"], 2)).rstrip("0").rstrip(".")
    return render(request, "finance/portfolio.html", {
        "portfolio": portfolio,
        "totals": totals,
    })