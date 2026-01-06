from backend.ml.ml_model import generate_itinerary_logic

def generate_itinerary(data):
    return {
        "itinerary": generate_itinerary_logic(
            city=data.get("city"),
            days=int(data.get("days")),
            interests=data.get("interests"),
            budget=data.get("budget")
        )
    }
