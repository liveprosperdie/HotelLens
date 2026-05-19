from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "index.html")


def search(request):
    city=request.GET["city"]
    return HttpResponse (f"Searching for {city}")