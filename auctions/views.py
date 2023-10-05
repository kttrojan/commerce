from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Category, Listing, Comment, Bid


def index(request):
    return render(request, "auctions/index.html", {
    "listings" : Listing.objects.filter(active=True),
    })


def create_listing(request):

    if request.method == "GET":
        return render(request, "auctions/create_listing.html", {
            "categories" : Category.objects.all(),
        })
    else:
        title_form = request.POST["title"]
        description_form = request.POST["description"]
        image_form = request.POST["image"]
        price_form = request.POST["price"]
        user = request.user

        active_form = request.POST["active"]
        if active_form == "on":
            active_form = True
        elif active_form == "off":
            active_form = False
        
        category_name = request.POST["category"]
        actual_category = Category.objects.get(name=category_name)

        first_bid = Bid(bid=int(price_form), user=user)
        first_bid.save()

    new_listing = Listing(
        title=title_form,
        description=description_form,
        image_url=image_form, 
        price=first_bid,
        active=active_form,
        owner=user,
        category=actual_category)
    
    new_listing.save()
    return HttpResponseRedirect(reverse("index"))      


def view_listing(request, listing_id):
    if request.method == "GET":
        listing = Listing.objects.get(pk=listing_id)
        watchlist_flag = request.user in listing.watchlist.all()
        comments = Comment.objects.filter(listing=listing)
        owner_flag = request.user == listing.owner
        return render(request, "auctions/view_listing.html", {
            "user" : request.user,
            "listing" : Listing.objects.get(pk=listing_id),
            "watchlist_flag" : watchlist_flag,
            "comments" : comments,
            "owner_flag" : owner_flag,
        })


def watchlist_remove(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("view_listing", args=[listing_id]))


def watchlist_add(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("view_listing", args=[listing_id]))


def watchlists(request):
    user = request.user
    return render(request, "auctions/watchlists.html", {
        "listings" : user.watched_listings.all()
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories" : Category.objects.all() 
    })


def view_category(request, category_name):
    category = Category.objects.get(name=category_name)
    listings = Listing.objects.filter(category=category)
    return render(request, "auctions/view_category.html", {
        "category" : category,
        "listings" : listings,
    })


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


def add_comment(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    comment = request.POST["comment"]

    new_comment = Comment(
        commenter = user,
        listing = listing,
        comment = comment,
    )
    new_comment.save()
    return HttpResponseRedirect(reverse("view_listing", args=[listing_id]))


def add_bid(request, listing_id):
    user = request.user
    new_bid = request.POST["new_bid"]
    listing = Listing.objects.get(pk=listing_id)
    watchlist_flag = request.user in listing.watchlist.all()
    comments = Comment.objects.filter(listing=listing)
    if int(new_bid) > listing.price.bid:
        
        updated_bid = Bid(user=user, bid=int(new_bid))
        updated_bid.save()

        listing.price = updated_bid
        listing.save()


        return render(request, "auctions/view_listing.html", {
            "listing" : listing,
            "message" : "New bid placed successfully",
            "success_flag" : True,
            "watchlist_flag" : watchlist_flag,
            "comments" : comments, 
            })
    else:
        return render(request, "auctions/view_listing.html", {
            "listing" : listing,
            "message" : "Error, try again.",
            "success_flag" : False,
            "watchlist_flag" : watchlist_flag,
            "comments" : comments, 
        })
    

def close_auction(request, listing_id):
    if request.method == "POST":
        user = request.user

        listing = Listing.objects.get(pk=listing_id)
        listing.active = False
        listing.save()

        owner_flag = request.user == listing.owner
        watchlist_flag = user in listing.watchlist.all()
        comments = Comment.objects.filter(listing=listing)

        return render(request, "auctions/view_listing.html", {
            "listing" : listing,
            "comments" : comments,
            "watchlist_flag" : watchlist_flag,
            "owner_flag" : owner_flag,
            "success_flag" : True,
            "message" : "The auction is now closed."
        })
