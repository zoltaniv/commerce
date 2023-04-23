from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.forms import ModelForm, Textarea, NumberInput
from django.db import models

from .models import User, Auction, Category, Watchlist, Rate, Comment


class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ["lot", "description", "first_rate",
                  "category_id", "image"]
        widgets = {"description": Textarea(attrs={
            "rows": 5, 
            "cols": 10,
            "style": "resize: none;",
            "class": "form-control"
            })}
class RateForm(ModelForm):
    class Meta:
        model = Rate
        fields = ["current_rate"]
        widgets = {"current_rate": NumberInput(attrs={
            "placeholder": "Input rate",
            "class": "form-control"
        })}
        
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["annotation"]
        widgets = {"annotation": Textarea(attrs={
            "placeholder": "Input your comment here",
            "rows": 5,
            "cols": 50,
            "style": "resize: none;"
        })}

def index(request):
    # Get all objects from database
    auctions = Auction.objects.all()
    # Get all objects from database
    categories = Category.objects.all()

    return render(request, "auctions/index.html", {"auctions": auctions, "categories": categories})


def login_view(request):
    categories = Category.objects.all()
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
            return render(request, "auctions/login.html", {"categories": categories,
                "message": "Invalid username and/or password"
            })
    else:
        return render(request, "auctions/login.html", {"categories": categories})


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
        categories = Category.objects.all()
        return render(request, "auctions/register.html", {"categories": categories})


def category_list(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {"categories": categories})


def category(request, category_id):
    auctions = Auction.objects.filter(category_id= category_id)
    category = Category.objects.filter(id=category_id)
    name = category.first().name
    
    categories = Category.objects.all()
    
    return render(request, "auctions/category.html", {"auctions": auctions, "categories": categories, "name": name})


@login_required
def new_auction(request):
    if request.method == "POST":
        # Save data in database
        Auction(lot= request.POST.get("lot"),
            description= request.POST.get("description"),
            first_rate= request.POST.get("first_rate"),
            category_id= Category(request.POST.get("category_id")),
            image= request.POST.get("image"),
            user_id= User(request.user.id)
            ).save()
        
        # Add first rate of lot as current rate
        Rate(current_rate= request.POST.get("first_rate"),
            lot_id= Auction.objects.last(),
            user_id= User(request.user.id)).save()
        
        return redirect(reverse("index"))
    else:
        form = AuctionForm()
        categories = Category.objects.all()
        return render(request, "auctions/new_auction.html", {"form": form, "categories": categories})
    
    
@login_required
def auction_view(request, category_id, auction_id):
    # Get auction object
    auction = Auction.objects.get(id=auction_id)
    wlist = auction.aucwlist.filter(user=request.user.id)
    rate = auction.aucrates.last()
    # comments = Comment.objects.all()
    categories = Category.objects.all()
    
    if request.method == "GET":
        return render(request, "auctions/auction_view.html", {
            "auction": auction, "wlist": wlist, "rate_form": RateForm(), 
            "comment_form": CommentForm(), "categories": categories})
    else:
        # For Rate form
        if request.POST.get("current_rate"):
            # Get form value
            proposed_rate = int(request.POST.get("current_rate"))
            # Check proposed rate
            if rate.current_rate >= proposed_rate:
                return render(request, "auctions/auction_view.html", {
                    "auction": auction, "wlist": wlist, "rate_form": RateForm(),
                    "comment_form": CommentForm(), "categories": categories,
                    "message": "You inserted too small value!"})
            else:
                rate.current_rate = request.POST.get("current_rate")
                rate.user_id = User(request.user.id)
                rate.save()
                
        # For Watchlist form
        if request.POST.get("watchlist_auction"):
            if wlist.first() == None:
                Watchlist(user=User(request.user.id),
                          auction=Auction(auction_id)).save()
            else:
                wlist.first().delete()
                
        # Close the auction
        if request.POST.get("close_auction"):
            auction.is_active = False
            auction.save()
            
        # Add comment
        if request.POST.get("annotation"):
            Comment(annotation= request.POST.get("annotation"),
                    auction= Auction(auction_id), 
                    user= User(request.user.id)).save()
            # comments = Comment.objects.all()
        
        return render(request, "auctions/auction_view.html", {
                "auction": auction, "wlist": wlist, "rate_form": RateForm(),
                "comment_form": CommentForm(), "categories": categories})


@login_required 
def watchlist_view(request):
    user = User.objects.get(id= request.user.id)
    watchlist = user.usewlist.all()
    categories = Category.objects.all()
    
    return render(request, "auctions/watchlist.html", {"watchlist": watchlist, "categories": categories})