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
    "Garden",
    "Sauna",
    "Babysitting/Child services",
    "Concierge",
    "Beach chairs/Loungers"
]


def rank_hotels(city,arrival_date="2026-06-01",departure_date="2026-06-04",adults="1",children_age=[],min_price=0,max_price=10**5):
    hotels=get_hotels(city,arrival_date,departure_date,adults,children_age,min_price,max_price)
    for hotel in hotels:
        amenities=hotel["amenities"]
        score=(10*hotel["review_score"])+(5*hotel["property_class"])
        hotel["key_amenities"]=[]
        for e in ESSENTIAL_AMENITIES:
            if e in amenities:
                score+=1
                hotel["key_amenities"].append(e)
            else:
                score-=2
        for l in LUXURY_AMENITIES:
            if l in amenities:
                score+=4
                hotel["key_amenities"].append(l)
        quality_score=(score/233)*10
        hotel["score"]=round(quality_score,2)

    hotels.sort(key=lambda x:x["score"],reverse=True)
    return hotels