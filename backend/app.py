from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# --- Check if CSV exists ---
csv_path = "data/places.csv"
if not os.path.exists(csv_path):
    print(f"ERROR: CSV file not found at {csv_path}")
else:
    print(f"Loading CSV from {csv_path}")

# Load CSV safely
places_df = pd.read_csv(csv_path)

# --- Routes ---

@app.route("/itinerary")
def generate_itinerary():
    try:
        days = int(request.args.get("days", 3))
        city = request.args.get("city")
        category = request.args.get("category")
        budget = request.args.get("budget")
        ideal_time = request.args.get("ideal_time")

        if not city:
            return jsonify({"error": "City is required"}), 400

        # Step 1: City filter (mandatory)
        df = places_df[places_df["city"] == city]

        if df.empty:
            return jsonify({"error": f"No places found for city '{city}'"}), 404

        # Step 2: Try strict filtering
        strict_df = df.copy()
        if category:
            strict_df = strict_df[strict_df["category"] == category]
        if ideal_time:
            strict_df = strict_df[strict_df["ideal_time"] == ideal_time]
        if budget:
            strict_df = strict_df[strict_df["budget_level"] == budget]

        # Step 3: Relax if strict fails
        final_df = strict_df if not strict_df.empty else df

        # Step 4: Sort by rating (highest first)
        final_df = final_df.sort_values(by="rating", ascending=False)

        # Step 5: Shuffle slightly for variety
        final_df = final_df.sample(frac=1).reset_index(drop=True)

        # Step 6: Distribute places across days (no repetition)
        itinerary = []
        total_places = len(final_df)

        for day in range(1, days + 1):
            start = (day - 1) * total_places // days
            end = day * total_places // days
            day_places = final_df.iloc[start:end].to_dict(orient="records")
            itinerary.append({
                "day": day,
                "places": day_places
            })

        return jsonify(itinerary)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/cities")
def get_cities():
    """Return all unique cities in CSV"""
    try:
        unique_cities = sorted(places_df["city"].unique())
        return jsonify(unique_cities)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("Starting Flask server on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
