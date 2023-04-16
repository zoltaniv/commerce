from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.forms import ModelForm, Textarea
from django.db import models

from .models import User, Auction, Category, Watchlist,Rate


class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = "__all__"
        exclude = ["user_id"]
        widgets = {"description": Textarea(attrs={
            "rows": 5, 
            "cols": 50,
            "style": "resize: none;"
            })}
        
class RateForm(ModelForm):
    class Meta:
        model = Rate
        fields = ["current_rate"]
        


def index(request):
    
    # Get all objects from database
    auctions = Auction.objects.all()
    
    return render(request, "auctions/index.html", {"auctions": auctions})


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def category_list(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {"categories": categories})


def category(request, category_id):
    auction_list = Auction.objects.filter(category_id= category_id)
    category = Category.objects.filter(id=category_id)
    name = category.first().name
    
    return render(request, "auctions/category.html", {"auctions": auction_list, "name": name})


def new_auction(request):
    if request.method == "POST":
        # Save data in database
        auction = Auction(
            lot= request.POST.get("lot"),
            description= request.POST.get("description"),
            first_rate= request.POST.get("first_rate"),
            category_id= Category(request.POST.get("category_id")),
            image= request.POST.get("image"),
            user_id= User(request.user.id)
            )
        auction.save()
        return redirect(reverse("index"))
    else:
        form = AuctionForm()
        return render(request, "auctions/new_auction.html", {"form": form})
    
    
def auction_view(request, category_id, auction_id):
    auction = Auction.objects.filter(id=auction_id).first()
    
    wlist = Watchlist.objects.filter(user=request.user.id, auction=auction_id)
    
    return render(request, "auctions/auction_view.html", {"auction": auction, "wlist": wlist})


def into_watchlist(request, category_id, auction_id):
    wlist = Watchlist(user=User(request.user.id), auction=Auction(request.POST.get("auction")))
    wlist.save()
    
    return redirect(reverse("auction_view", args=[category_id, auction_id]))


def out_watchlist(request, category_id, auction_id):
    wlist = Watchlist.objects.filter(user=request.user.id, auction=auction_id)
    wlist.delete()
    
    return redirect(reverse("auction_view", args=[category_id, auction_id]))
