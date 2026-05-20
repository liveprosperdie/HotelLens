from hotels.search import get_hotels


ESSENTIAL_AMENITIES=[
    "Air conditioning", 
    "Heating", 
    "Private bathroom", 
    "Shower", 
    "Flat-screen TV", 
    "Internet", 
    "Safe", 
    "24-hour front desk", 
    "Parking", 
    "Restaurant", 
    "Elevator", 
    "24-hour security", 
    "Key card access", 
    "Wheelchair accessible", 
    "Free toiletries", 
    "Hairdryer", 
    "Daily housekeeping", 
    "Smoke alarms",
    "Fire extinguishers", 
    "Laundry",
    "Non-smoking rooms"
]


LUXURY_AMENITIES=[ 
    "Bar", 
    "Fitness center",
    "Spa", 
    "Outdoor swimming pool", 
    "Room service", 
    "Bathrobe", 
    "Slippers", 
    "Massage", 
    "Hot tub/Jacuzzi", 
    "Dry cleaning", 
    "Currency exchange", 
    "Airport shuttle", 
    "Spa/Wellness packages", 
    "Steam room", 
    "Bathtub or shower", 
    "Minibar", 
    "Wine/Champagne", 
    "Garden"
]


def rank_hotels(city):
    hotels=get_hotels(city)
    for hotel in hotels:
        amenities=hotel["amenities"]
        score=(10*hotel["review_score"])+(5*hotel["property_class"])
        for e in ESSENTIAL_AMENITIES:
            if e in amenities:
                score+=1
            else:
                score-=2
        for l in LUXURY_AMENITIES:
            if l in amenities:
                score+=4
        score/=hotel["price"]
        hotel["score"]=score

    hotels.sort(key=lambda x:x["score"],reverse=True)
    return hotels