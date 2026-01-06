import pandas as pd
import random

def generate_itinerary(days):
    df = pd.read_csv("backend/data/places.csv")

    itinerary = []

    for day in range(1, days + 1):
        day_places = []

        # Pick places intelligently: attractions + markets/restaurants
        for category, count in [("attraction", 3), ("market", 1), ("restaurant", 1)]:
            cat_places = df[df['type'] == category]
            if len(cat_places) < count:
                selected = cat_places.to_dict(orient='records')
            else:
                selected = cat_places.sample(count).to_dict(orient='records')
            day_places.extend(selected)

        # Shuffle the day's places
        random.shuffle(day_places)
        itinerary.append({"day": day, "places": day_places})

    return itinerary
