import os
import uvicorn
from fastapi import FastAPI, HTTPException # INSTALLATION: pip install fastapi uvicorn
import redis # INSTALLATION: pip install redis
import requests

# ==========================================
# 🌩️ WEATHER SERVICE CONFIGURATION
# ==========================================
# Requires an API key from OpenWeatherMap
# ==========================================
OPENWEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL", "3600")) # Default: 1 hour
PORT = int(os.getenv("PORT", "8000"))

app = FastAPI(title="Weather Service", version="1.0.0")

# Initialize Redis connection
cache = redis.from_url(REDIS_URL)

def get_weather_from_provider(city: str):
    """Fetches real-time data from external API."""
    if not OPENWEATHER_API_KEY:
        raise ValueError("API Key is missing")
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

@app.get("/weather/{city}")
def get_weather(city: str):
    """
    Get weather for a city (with caching).
    """
    # 1. Check Cache
    cached_data = cache.get(city)
    if cached_data:
        print(f"Serving {city} from cache")
        return {"source": "cache", "data": eval(cached_data)}

    # 2. Fetch Live
    try:
        data = get_weather_from_provider(city)
        if not data:
            raise HTTPException(status_code=404, detail="City not found")
        
        # 3. Save to Cache
        cache.setex(city, CACHE_TTL_SECONDS, str(data))
        return {"source": "live", "data": data}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Local Development
    print(f"Starting server on port {PORT}...")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
