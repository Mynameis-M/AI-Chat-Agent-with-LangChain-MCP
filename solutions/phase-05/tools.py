"""
Phase 5: Tool Definitions for the AI Assistant

Tools are functions that the LLM agent can call to perform actions or get external data.
This is what makes agents more powerful than simple chat - they can interact with the world!

Key Concepts:
- @tool decorator: Converts a Python function into a LangChain tool
- Docstrings matter: The agent uses the docstring to understand when to use the tool
- Error handling: Tools should handle errors gracefully and return helpful messages

How tools work:
1. User asks a question (e.g., "What's the weather in Paris?")
2. Agent reads the tool descriptions and decides to call get_weather
3. Agent calls the tool with appropriate arguments
4. Tool returns a result (weather data or error message)
5. Agent incorporates the result into its response
"""

import os
import httpx
from langchain_core.tools import tool


@tool
def get_weather(city: str) -> str:
    """
    Get the current weather for a city.

    The agent will use this tool when users ask about weather.
    The docstring is CRITICAL - the agent reads it to understand:
    - What the tool does
    - What arguments to pass
    - What to expect as a result

    Args:
        city: The name of the city to get weather for (e.g., "London", "Tokyo", "New York")

    Returns:
        A string describing the current weather conditions.
    """
    # Get API key from environment variables
    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key or api_key == "your_weather_api_key_here":
        return "Error: Weather API key not configured. Please add WEATHER_API_KEY to your .env file."

    try:
        # Call the WeatherAPI
        url = f"http://api.weatherapi.com/v1/current.json"
        params = {"key": api_key, "q": city, "aqi": "no"}

        response = httpx.get(url, params=params, timeout=10.0)
        response.raise_for_status()

        data = response.json()

        # Extract relevant information
        location = data["location"]["name"]
        country = data["location"]["country"]
        temp_c = data["current"]["temp_c"]
        temp_f = data["current"]["temp_f"]
        condition = data["current"]["condition"]["text"]
        humidity = data["current"]["humidity"]
        wind_kph = data["current"]["wind_kph"]

        return f"""Weather for {location}, {country}:
🌡️ Temperature: {temp_c}°C ({temp_f}°F)
☁️ Condition: {condition}
💧 Humidity: {humidity}%
💨 Wind: {wind_kph} km/h"""

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 400:
            return f"Sorry, I couldn't find weather data for '{city}'. Please check the city name."
        return f"Error fetching weather: {e}"
    except httpx.RequestError as e:
        return f"Network error: Could not connect to weather service. {e}"
    except Exception as e:
        return f"Unexpected error: {e}"


# List of all available tools to pass to create_agent()
# Add more tools here as you build them!
# Each tool should have a clear docstring explaining what it does
TOOLS = [get_weather]
