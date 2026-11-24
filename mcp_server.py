import httpx
from mcp.server import MCPServer

# URL of our existing Flask app (app.py)
FLASK_API = "http://127.0.0.1:8051"
mcp = MCPServer("Planets Server")


def call_flask(endpoint: str, params: dict | None = None):
    """Call our Flask REST API and return JSON."""
    with httpx.Client(timeout=10.0) as client:
        response = client.get(FLASK_API + endpoint, params=params)
        response.raise_for_status()
        return response.json()


@mcp.tool()
def planets_with_rings() -> list:
    """List every planet and whether it has rings (hasRings is true or false)."""
    return call_flask("/guides/rings")


@mcp.tool()
def planets_with_gas(gas: str) -> list:
    """List the planets whose main atmosphere contains a gas.
    Use the chemical formula, for example "H2", "He", "CO2" or "CH4"."""
    return call_flask("/guides/atmosphere", {"gas": gas})


@mcp.tool()
def planets_by_temperature() -> list:
    """List the planets from hottest to coldest by mean surface temperature in Celsius."""
    return call_flask("/guides/temperature/ranked")


@mcp.tool()
def planets_in_order() -> list:
    """List the planets in order from the Sun (1 = closest)."""
    return call_flask("/guides/order")


@mcp.tool()
def get_statistics(key: str) -> dict:
    """Get a usage statistic for our app from Redis.
    key must be "active_users" or "query_count" (how many requests our app has served)."""
    allowed_keys = {"active_users", "query_count"}
    if key not in allowed_keys:
        raise ValueError("Unsupported statistic")
    return call_flask("/stats", {"key": key})


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)