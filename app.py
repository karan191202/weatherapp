from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("a220d1ce0bb206cebd38f5c1ae031048")  # Load API key from environment variable

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    if request.method == "POST":
        city = request.form.get("city")
        if API_KEY and city:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url).json()
            if response.get("cod") == 200:
                weather = {
                    "city": city,
                    "temperature": response["main"]["temp"],
                    "description": response["weather"][0]["description"],
                    "icon": response["weather"][0]["icon"],
                }
            else:
                weather = {"error": "City not found!"}
        else:
            weather = {"error": "Missing city or API key."}
    return render_template("index.html", weather=weather)

if __name__ == "__main__":
    app.run(debug=True)
