from mcp.server import FastMCP

mcp = FastMCP("travel-search", port=3336)

@mcp.tool()
def search_destination(destination: str) -> str:
    """Retrieves tourist attractions, landmarks, and activities for a given destination."""
    return (
        f"Top attractions in {destination}: "
        "1. Historic Old Town, 2. Local Museum, 3. Central Market, "
        "4. Scenic Viewpoint, 5. Traditional Restaurant District."
    )

if __name__ == "__main__":
    mcp.run(transport="sse")