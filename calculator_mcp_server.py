from mcp.server import FastMCP

mcp = FastMCP("calculator-tools", port=3337)

@mcp.tool()
def calculate(expression: str) -> float:
    """Performs arithmetic operations required during agent reasoning."""
    try:
        result = eval(expression)
        return float(result)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="sse")