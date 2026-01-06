import json
import random

def load_data(destination):
    try:
        with open(f"data/{destination.lower()}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise Exception("Destination data not available yet.")

def generate_itinerary(destination, days, budget, interests):
    attractions = load_data(destination)

    # Step 1: Filter
    filtered = [a for a in attractions if a["type"] in interests and a["cost"] == budget]
    if not filtered:
        filtered = attractions

    # Step 2: Shuffle
    random.shuffle(filtered)

    # Step 3: Allocate day-wise
    itinerary = {}
    idx = 0
    for day in range(1, days + 1):
        daily_plan = []
        time_left = 8
        while idx < len(filtered) and filtered[idx]["time_required"] <= time_left:
            daily_plan.append(filtered[idx])
            time_left -= filtered[idx]["time_required"]
            idx += 1
        itinerary[f"Day {day}"] = daily_plan

    return itinerary
