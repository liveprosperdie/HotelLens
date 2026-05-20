import requests
from concurrent.futures import ThreadPoolExecutor
API_KEY="094b5f6fefmsh137f2fa3147e8bdp143a5cjsnf1a699bb8745"

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
    if (response.json()["data"][0]["city_name"]).upper()==city.upper():
        return response.json()["data"][0]["dest_id"]
    else:
        return None
    

def get_hotels(city):
    dest_id=get_dest_id(city)
    if dest_id is None:
        return []
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
	    "x-rapidapi-key": API_KEY,
	    "x-rapidapi-host": "booking-com15.p.rapidapi.com",
	    "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data=response.json()
    hotels_details=[]
    for hotel in data["data"]["hotels"][:2]:
        hotels_details.append(
            {
                "name": hotel["property"]["name"],
                "review_score": hotel["property"]["reviewScore"],
                "price": hotel["property"]["priceBreakdown"]["grossPrice"]["value"],
                "property_class": hotel["property"]["propertyClass"],
                "hotel_id": hotel["hotel_id"]
            }
        )
    with ThreadPoolExecutor() as executor:
        amenities_list=executor.map(get_amenities, [h["hotel_id"] for h in hotels_details])
        for hotel,amenities in zip(hotels_details,amenities_list):
            hotel["amenities"]=amenities
    return hotels_details


def get_amenities(hotel_id):
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/getHotelFacilities"
    querystring = {"hotel_id":hotel_id,"arrival_date":"2026-06-01","departure_date":"2026-06-04","languagecode":"en-us"}
    headers = {
	    "x-rapidapi-key": API_KEY,
	    "x-rapidapi-host": "booking-com15.p.rapidapi.com",
	    "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data=response.json()
    amenities=[i["instances"][0]["title"] for i in data["data"]["facilities"]]
    return amenities