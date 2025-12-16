#!/usr/bin/env python3
"""
Weather Lookup MCP Server (HTTP/SSE)

This script creates a FastMCP server that exposes weather lookup tools over HTTP.
It uses the WeatherAPI.com service to fetch current weather data by US zip code.

Setup:
1. Get a free API key from https://www.weatherapi.com/signup.aspx
2. Add it to your `.env` file as `WEATHER_API_KEY=your_key_here`

Usage:
    python 06_weather_fast_mcp.py

The server will run at: http://127.0.0.1:8001

To use with Claude Desktop, add this to your config:
{
  "mcpServers": {
    "weather-server": {
      "command": "python",
      "args": ["/path/to/06_weather_fast_mcp.py"]
    }
  }
}

Or connect directly via HTTP at: http://127.0.0.1:8001
"""

from fastmcp import FastMCP
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastMCP server
mcp = FastMCP("Weather Lookup Server")


@mcp.tool()
def get_weather_by_zipcode(zipcode: str) -> dict:
    """
    Get current weather for a US zip code from WeatherAPI.com
    
    Args:
        zipcode: US zip code (e.g., "10001")
    
    Returns:
        Dictionary containing weather information
    """
    try:
        # Get API key from environment
        api_key = os.getenv('WEATHER_API_KEY')
        
        if not api_key:
            # Free tier: Get key from https://www.weatherapi.com/signup.aspx
            return {
                "error": "WEATHER_API_KEY not found in environment variables",
                "message": "Get a free API key from https://www.weatherapi.com/signup.aspx"
            }
        
        # WeatherAPI.com endpoint
        url = f"http://api.weatherapi.com/v1/current.json"
        params = {
            "key": api_key,
            "q": zipcode,
            "aqi": "no"
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Format the response
        weather_info = {
            "location": f"{data['location']['name']}, {data['location']['region']}",
            "zipcode": zipcode,
            "temperature_f": data['current']['temp_f'],
            "temperature_c": data['current']['temp_c'],
            "condition": data['current']['condition']['text'],
            "humidity": data['current']['humidity'],
            "wind_mph": data['current']['wind_mph'],
            "feels_like_f": data['current']['feelslike_f'],
            "last_updated": data['current']['last_updated']
        }
        
        return weather_info
        
    except requests.exceptions.RequestException as e:
        return {
            "error": "Failed to fetch weather data",
            "details": str(e)
        }
    except KeyError as e:
        return {
            "error": "Failed to parse weather data",
            "details": f"Missing key: {str(e)}"
        }


    
    return f"""Weather for {weather['location']} (Zip: {weather['zipcode']}):
🌡️ Temperature: {weather['temperature_f']}°F ({weather['temperature_c']}°C)
🌤️ Conditions: {weather['condition']}
🤚 Feels like: {weather['feels_like_f']}°F
💧 Humidity: {weather['humidity']}%
💨 Wind: {weather['wind_mph']} mph
⏰ Last updated: {weather['last_updated']}"""


if __name__ == "__main__":
    # Run the MCP server over HTTP at 127.0.0.1:8001
    print("🚀 Starting Weather Lookup MCP Server over HTTP...")
    print("📡 Server URL: http://127.0.0.1:8001")
    print("⚙️  Available tools: get_weather_by_zipcode, get_weather_summary")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 60)
    
    # Run server with SSE transport over HTTP
    mcp.run(transport="sse", host="127.0.0.1", port=8001)

