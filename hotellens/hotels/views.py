from django.shortcuts import render
from hotels.search import get_hotel_details
from hotels.ranker import rank_hotels


def index(request):
    return render(request, "index.html")


def search(request):
    city=request.GET["city"]
    arrival_date=request.GET["arrival_date"]
    departure_date=request.GET["departure_date"]
    adults=request.GET["adults"]
    children_age=request.GET["children_age"]
    min_price=int(request.GET.get("min_price") or 0)
    max_price=int(request.GET.get("max_price") or 10**5)
    hotels=rank_hotels(city,arrival_date,departure_date,adults,children_age,min_price,max_price)
    return render(request,"search.html",{"hotels":hotels})

def hotel_detail(request):
    hotel_id=request.GET["hotel_id"]
    arrival_date=request.GET["arrival_date"]
    departure_date=request.GET["departure_date"]
    adults=request.GET["adults"]
    children_age=request.GET["children_age"]
    details=get_hotel_details(hotel_id,arrival_date,departure_date,adults,children_age)
    return render (request,"hotel.html",{"details":details})
