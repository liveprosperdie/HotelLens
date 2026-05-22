import requests
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY= os.environ.get("RAPIDAPI_KEY")

def get_dest_id(city):
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchDestination"
    querystring = {"query":city}
    headers = {
	    "x-rapidapi-key": API_KEY,
	    "x-rapidapi-host": "booking-com15.p.rapidapi.com",
	    "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if "data" not in response.json():
        return None
    if city.upper() in response.json()["data"][0]["city_name"].upper():
        return response.json()["data"][0]["dest_id"]
    elif city.upper() == "CHANDIGARH":
        return response.json()["data"][0]["dest_id"]
    else:
        return None
    

def get_hotels(city,arrival_date="2026-09-01",departure_date="2026-09-04",adults=1,children_age=[],min_price=0,max_price=10**5):
    dest_id=get_dest_id(city)
    if dest_id is None:
        return []
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchHotels"
    headers = {
	    "x-rapidapi-key": API_KEY,
	    "x-rapidapi-host": "booking-com15.p.rapidapi.com",
	    "Content-Type": "application/json"
    }
    def fetch_pages(page):
        querystring = {
        "dest_id":dest_id,
        "search_type":"CITY",
        "arrival_date":arrival_date,
        "departure_date":departure_date,
        "adults":adults,
        "children_age":children_age,
        "room_qty":"1",
        "page_number":page,
        "units":"metric",
        "temperature_unit":"c",
        "languagecode":"en-us",
        "currency_code":"INR",
        "price_min":min_price,
        "price_max":max_price,
        "location":"US"}
        response=requests.get(url, headers=headers, params=querystring)
        return response.json()["data"]["hotels"]
    nights=(datetime.strptime(departure_date,"%Y-%m-%d") - datetime.strptime(arrival_date,"%Y-%m-%d")).days
    with ThreadPoolExecutor() as executor:
        all_pages=executor.map(fetch_pages,[1,2,3,4,5])
    hotels_details=[]
    for page in all_pages:
        for hotel in page:
            hotels_details.append(
                {
                    "name": hotel["property"]["name"],
                    "review_score": hotel["property"]["reviewScore"],
                    "price": ((hotel["property"]["priceBreakdown"]["grossPrice"]["value"])/nights),
                    "total_price": hotel["property"]["priceBreakdown"]["grossPrice"]["value"],
                    "property_class": hotel["property"]["propertyClass"],
                    "hotel_id": hotel["hotel_id"],
                    "photo": hotel["property"].get("photoUrls", [])
                }
            )
    with ThreadPoolExecutor() as executor:
        amenities_list=executor.map(get_amenities, [h["hotel_id"] for h in hotels_details])
        for hotel,amenities in zip(hotels_details,amenities_list):
            hotel["amenities"]=amenities
    return hotels_details


def get_amenities(hotel_id,arrival_date="2026-09-01",departure_date="2026-09-04"):
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/getHotelFacilities"
    querystring = {"hotel_id":hotel_id,
                   "arrival_date":arrival_date,
                   "departure_date":departure_date,
                   "languagecode":"en-us"
                   }
    headers = {
	    "x-rapidapi-key": API_KEY,
	    "x-rapidapi-host": "booking-com15.p.rapidapi.com",
	    "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data=response.json()
    if not data.get("data") or not data["data"].get("facilities"):
        return []
    amenities=[i["instances"][0]["title"] for i in data["data"]["facilities"]]
    return amenities


def get_hotel_details(hotel_id,arrival_date="2026-09-01",departure_date="2026-09-04",adults=1,children_age=[]):
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/getHotelDetails"
    querystring = {"hotel_id":hotel_id,
                   "arrival_date":arrival_date,
                   "departure_date":departure_date,
                   "adults":adults,
                   "children_age":children_age,
                   "room_qty":"1",
                   "units":"metric",
                   "temperature_unit":"c",
                   "languagecode":"en-us",
                   "currency_code":"INR"
                   }
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "booking-com15.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, params=querystring)
    s = response.json()["data"]
    room_id= str(s["block"][0]["room_id"])
    nights=(datetime.strptime(departure_date,"%Y-%m-%d") - datetime.strptime(arrival_date,"%Y-%m-%d")).days
    details={
        "name": s["hotel_name"],
        "address": s["address"],
        "coordinates": {"latitude": s["latitude"],"longitude":s["longitude"]},
        "url": s["url"],
        "top_amenities": [i["name"] for i in s["facilities_block"]["facilities"]], 
        "photo_urls":[i["url_max750"] for i in s["rooms"][room_id]["photos"]],
        "room_info": s["rooms"][room_id]["description"],
        "cancellation_policy": s["block"][0]["paymentterms"]["cancellation"]["description"],
        "total_price": s["product_price_breakdown"]["gross_amount_hotel_currency"]["value"],
        "nights":nights,
        "price_per_night":(s["product_price_breakdown"]["gross_amount_hotel_currency"]["value"])/nights
    }
    return details


