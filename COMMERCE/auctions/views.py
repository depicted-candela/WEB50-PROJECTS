from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Auction, Bid, Comment, Category
from .forms import AuctionForm, BidForm, CommentForm


def index(request):
    obj = Auction.objects.all()
    return render(request, "auctions/index.html",
    {"obj": obj})


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
        login(request, username)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create(request):
    if request.method == 'GET':
        return render(request, "auctions/create.html",
        {"form": AuctionForm()})
    if request.method == 'POST':
        form = AuctionForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            object = form.save(commit=False)
            object.seller = request.user
            object.save()
        return HttpResponseRedirect(reverse("index"))


def auction(request, id):

    obj = Auction.objects.get(id=id)
    bid = Bid.objects.filter(auction_id=id).filter(current=True).first()
    com = Comment.objects.filter(product=id)

    if obj.status == 1:
        if bid:
            return render(request, "auctions/auction.html",
            {"obj": obj,
            "bid": bid.bid,
            "com": com})
        else:
            return render(request, "auctions/auction.html",
            {"obj": obj,
            "bid": 0,
            "com": com})
    else:
        if bid:
            return render(request, "auctions/auction.html",
            {"obj": obj,
            "bid": bid.bid,
            "winner": bid.bidder,
            "com": com})
        else:
            return render(request, "auctions/auction.html",
            {"obj": obj,
            "bid": obj.price,
            "winner": 'Neither user bid for this auction',
            "com": com})


def watch_auction(request, id):
    obj = Auction.objects.get(id=id)
    if request.method == 'POST':
        if 'w' in request.POST:
            obj.watchers.add(request.user)
        else:
            obj.watchers.remove(request.user)
        return HttpResponseRedirect(reverse("auction", kwargs={'id':id}))


def bid_auction(request, id):
    obj = Auction.objects.get(id=id)
    if request.method == 'GET':
        return render(request, "auctions/bid.html",
        {"form": BidForm,
        "obj": obj})
    else:
        form = BidForm(request.POST or None)
        if form.is_valid():
            object = form.save(commit=False)
            object.bidder = request.user
            object.auction_id = obj.id
            not_c = Bid.objects.filter(auction_id=id).filter(current=True).first()
            if not_c:
                if obj.price >= object.bid:
                    return render(request, 'auctions/error.html',
                    {'message': "Your bid must be at least higher than the inital price"})
                elif not_c.bid >= object.bid:
                    return render(request, 'auctions/error.html',
                    {'message': "You must bid a higher price for the auction than the current bid"})
                else:
                    not_c.current = 0
                    not_c.save()
            else:
                if obj.price >= object.bid:
                    return render(request, 'auctions/error.html',
                    {'message': "Your bid must be at least higher than the inital price"})
            object.save()
        return HttpResponseRedirect(reverse("auction", kwargs={'id':id}))


def close_auction(request, id):

    if request.method == 'POST':
        obj = Auction.objects.get(id=id)
        obj.status = 0
        obj.save()
    return HttpResponseRedirect(reverse("auction", kwargs={'id':id}))


def comment_auction(request, id):

    obj = Auction.objects.get(id=id)

    if request.method == 'GET':
        return render(request, "auctions/comment.html", {
            'form':CommentForm(),
            'obj':obj
        })
    else:
        comm = CommentForm(request.POST or None)
        if comm.is_valid():
            object = comm.save(commit=False)
            object.user = request.user
            object.product_id = obj.id
            object.save()
            return HttpResponseRedirect(reverse("auction", kwargs={'id':id}))
        else:
            return HttpResponseRedirect(reverse("auction", kwargs={'id':id}))


def cancel_comment_auction(request, id):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse("auction", kwargs={'id':id}))


def watchlist(request):
    wlist = Auction.objects.filter(watchers=request.user.id)
    return render(request, 'auctions/watchlist.html',
    {"list":wlist})


def category(request):
    cat =  Category.objects.all()
    return render(request, 'auctions/category.html',
                  {'cats':cat})


def category_l(request, id):
    cat = Category.objects.get(id=id)
    act = Auction.objects.filter(category_id=id)
    print(cat)
    return render(request, 'auctions/category_l.html',
                  {'cats':act, 'title':cat})