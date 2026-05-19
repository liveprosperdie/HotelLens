import requests
import json


def get_dest_id(city):
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchDestination"
    querystring = {"query":city}
    headers = {
    	"x-rapidapi-key": "392ab4de0bmsh54ce54dab743b94p161e0ejsn2fe9990ac38c",
	    "x-rapidapi-host": "booking-com15.p.rapidapi.com",
	    "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if (response.json()["data"][0]["city_name"]).upper()==city.upper():
        return response.json()["data"][0]["dest_id"]
    else:
        return None
    

def get_hotels(city):
    dest_id=get_dest_id(city)
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchHotels"
    querystring = {
        "dest_id":dest_id,
        "search_type":"CITY",
        "arrival_date":"2026-06-01",
        "departure_date":"2026-06-04",
        "adults":"1",
        "children_age":"0,17",
        "room_qty":"1",
        "page_number":"1",
        "units":"metric",
        "temperature_unit":"c",
        "languagecode":"en-us",
        "currency_code":"INR",
        "location":"US"}
    headers = {
	    "x-rapidapi-key": "392ab4de0bmsh54ce54dab743b94p161e0ejsn2fe9990ac38c",
	    "x-rapidapi-host": "booking-com15.p.rapidapi.com",
	    "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    data=response.json()
    hotels_details=[]
    for hotel in data["data"]["hotels"]:
        hotels_details.append(
            {
                "name": hotel["property"]["name"],
                "review_score": hotel["property"]["reviewScore"],
                "price": hotel["property"]["priceBreakdown"]["grossPrice"]["value"],
                "property_class": hotel["property"]["propertyClass"],
                "hotel_id": hotel["hotel_id"]
            }
        )
    print(json.dumps(hotels_details,indent=4))


get_hotels("AGRA")