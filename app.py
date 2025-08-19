from flask import Flask, render_template, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Open-Meteo API URL
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
OPEN_METEO_ALERTS_URL = "https://api.open-meteo.com/v1/warnings"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/weather")
def get_weather():
    """Fetch weather data from Open-Meteo API"""
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "Missing lat/lon"}), 400

    try:
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "uv_index_max",
                "precipitation_sum"
            ],
            "timezone": "auto"
        }
        res = requests.get(OPEN_METEO_URL, params=params)
        weather_data = res.json()

        # Alerts API
        alert_params = {"latitude": lat, "longitude": lon}
        alert_res = requests.get(OPEN_METEO_ALERTS_URL, params=alert_params)
        alerts_data = alert_res.json()

        return jsonify({
            "weather": weather_data,
            "alerts": alerts_data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
