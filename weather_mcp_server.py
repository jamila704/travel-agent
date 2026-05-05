from mcp.server import FastMCP

mcp = FastMCP("weather-tools", port=3334)

@mcp.tool()
def get_weather(destination: str, travel_dates: str) -> str:
    """Provides typical or forecasted weather conditions for travel dates."""
    return f"Weather in {destination} during {travel_dates}: Sunny, 24°C average. Great for outdoor activities."

if __name__ == "__main__":
    mcp.run(transport="sse")