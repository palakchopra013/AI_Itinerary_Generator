from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend

# Load CSV
places_df = pd.read_csv("data/places.csv")

@app.route("/itinerary")
def generate_itinerary():
    try:
        days = int(request.args.get("days", 3))
        city = request.args.get("city", None)
        trip_type = request.args.get("type", None)
        budget = request.args.get("budget", None)
        ideal_time = request.args.get("ideal_time", None)

        # Filter by preferences
        filtered_df = places_df.copy()
        if city:
            filtered_df = filtered_df[filtered_df["city"] == city]
        if trip_type:
            filtered_df = filtered_df[filtered_df["type"] == trip_type]
        if budget:
            filtered_df = filtered_df[filtered_df["budget_level"] == budget]
        if ideal_time:
            filtered_df = filtered_df[filtered_df["ideal_time"] == ideal_time]

        if filtered_df.empty:
            return jsonify({"error": "No places found with these preferences"}), 404

        # Shuffle to randomize selection
        filtered_df = filtered_df.sample(frac=1).reset_index(drop=True)

        # Split unique places across days
        itinerary = []
        total_places = len(filtered_df)
        for day in range(1, days + 1):
            # Calculate start and end index
            start_idx = (day - 1) * total_places // days
            end_idx = day * total_places // days
            day_places = filtered_df.iloc[start_idx:end_idx].to_dict(orient="records")
            itinerary.append({"day": day, "places": day_places})

        return jsonify(itinerary)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
