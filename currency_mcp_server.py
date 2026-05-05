from mcp.server import FastMCP

mcp = FastMCP("currency-tools", port=3335)

@mcp.tool()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """Converts estimated travel costs into the user's preferred currency."""
    rates = {
        "USD_EUR": 0.92,
        "USD_MAD": 10.1,
        "USD_GBP": 0.79,
        "EUR_USD": 1.09,
        "EUR_MAD": 11.0,
    }
    key = f"{from_currency.upper()}_{to_currency.upper()}"
    rate = rates.get(key, 1.0)
    return round(amount * rate, 2)

if __name__ == "__main__":
    mcp.run(transport="sse")