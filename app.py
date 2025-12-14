from flask import Flask, render_template
import requests
import yfinance as yf

app = Flask(__name__)

# --- SETTINGS ---
# Yahan apni API Key paste karo jo copy ki thi
API_KEY = "YOUR_API_KEY_HERE"  
CITY = "Mumbai"

# 1. Mausam ka Data Lana
def get_weather():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={b424ab646ee788eaa7ae9ff697871767}&units=metric"
        data = requests.get(url).json()
        return {
            "temp": data["main"]["temp"],
            "desc": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"]
        }
    except:
        return {"temp": "--", "desc": "Error", "icon": ""}

# 2. Market ka Data Lana (NIFTY 50)
def get_stock():
    try:
        stock = yf.Ticker("^NSEI") # Nifty 50 ka symbol
        hist = stock.history(period="2d")
        
        today = hist["Close"].iloc[-1]
        yesterday = hist["Close"].iloc[-2]
        change = today - yesterday
        
        return {
            "price": round(today, 2),
            "change": round(change, 2),
            "color": "green" if change > 0 else "red"
        }
    except:
        return {"price": "--", "change": "--", "color": "black"}

# 3. Website Par Dikhana
@app.route("/")
def home():
    weather_data = get_weather()
    stock_data = get_stock()
    
    # Simple Insight Logic
    insight = "Market ko mausam se fark nahi pad raha."
    if "rain" in weather_data["desc"].lower() and stock_data["change"] < 0:
        insight = "Baarish hai aur Market bhi gir gaya! 🌧️📉"
    elif "clear" in weather_data["desc"].lower() and stock_data["change"] > 0:
        insight = "Mausam saaf hai aur Market bhi khush hai! ☀️📈"

    return render_template("index.html", weather=weather_data, stock=stock_data, insight=insight)

if __name__ == "__main__":
    app.run(debug=True)