from mcp.server import FastMCP

mcp = FastMCP("budget-tools", port=3333)

@mcp.tool()
def estimate_budget(destination: str, days: int) -> float:
    """Estimate travel budget in USD."""
    base_cost = 100
    return base_cost * days

if __name__ == "__main__":
    mcp.run(transport="sse")