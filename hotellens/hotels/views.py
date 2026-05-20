from django.shortcuts import render
from django.http import HttpResponse
from hotels.search import get_hotels
from hotels.ranker import rank_hotels


def index(request):
    return render(request, "index.html")


def search(request):
    city=request.GET["city"]
    hotels=rank_hotels(city)
    return render(request,"search.html",{"hotels":hotels})

