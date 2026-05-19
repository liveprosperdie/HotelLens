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
    data=response.json()
    good_data=json.dumps(data, indent=4)
    print(good_data)

def main():
    get_dest_id("Agra")

main()