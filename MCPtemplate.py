
import httpx
from mcp.server import MCPServer

# URLs of the existing Flask applications
MONGO_API = "http://127.0.0.1:5001"
REDIS_API = "http://127.0.0.1:5002"
mcp = MCPServer("Multi-Database Server")

def call_flask(base_url: str, endpoint: str, params: dict):
    """Call an existing Flask REST API and return JSON."""
    with httpx.Client(timeout=10.0) as client:
        response = client.get(
            base_url + endpoint,
            params=params
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
def search_universities(
    name: str,
    year: str = ""
) -> list:
    """Search MongoDB universities records by name and
    optionally year."""
    return call_flask(
        MONGO_API,
        "/universities",
        {"name": name, "year": year}
    )
@mcp.tool()
def get_statistics(key: str) -> dict:
    """Retrieve a named statistic from the Redis service."""
    allowed_keys = {"active_users", "query_count"}
    if key not in allowed_keys:
        raise ValueError("Unsupported statistic")

    return call_flask(
        REDIS_API,
        "/stats",
        {"key": key}
    )

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=5000
    )
