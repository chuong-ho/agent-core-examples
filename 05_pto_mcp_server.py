#!/usr/bin/env python3
"""
PTO Hours MCP Server (HTTP/SSE)

This script creates a FastMCP server that exposes PTO checking tools over HTTP.
It uses if-else logic similar to the agent-example.ipynb.

Usage:
    python pto_mcp_server.py

The server will run at: http://127.0.0.1:8000

To use with Claude Desktop, add this to your config:
{
  "mcpServers": {
    "pto-server": {
      "command": "python",
      "args": ["/path/to/pto_mcp_server.py"]
    }
  }
}

Or connect directly via HTTP at: http://127.0.0.1:8000
"""

from fastmcp import FastMCP
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastMCP server
mcp = FastMCP("PTO Hours Server")

# PTO data (simulating employee PTO balance)
PTO_HOURS_AVAILABLE = 94
PTO_HOURS_TAKEN = 104


@mcp.tool()
def get_pto_hours() -> str:
    """
    Get the total number of PTO hours available.
    
    Returns:
        str: The available PTO hours
    """
    return f"You have {PTO_HOURS_AVAILABLE} PTO hours available."


@mcp.tool()
def get_pto_days() -> str:
    """
    Get the total number of PTO days available (assuming 8-hour workday).
    
    Returns:
        str: The available PTO days and hours
    """
    days = PTO_HOURS_AVAILABLE / 8
    return f"You have {days} PTO days available ({PTO_HOURS_AVAILABLE} hours)."


@mcp.tool()
def can_take_full_day() -> str:
    """
    Check if employee has enough PTO for a full day off (8 hours).
    Uses if-else logic to determine availability.
    
    Returns:
        str: Whether a full day can be taken
    """
    if PTO_HOURS_AVAILABLE >= 8:
        return f"Yes, you can take a full day off. You have {PTO_HOURS_AVAILABLE} hours available."
    else:
        return f"No, you don't have enough PTO for a full day. You only have {PTO_HOURS_AVAILABLE} hours available."


@mcp.tool()
def can_take_half_day() -> str:
    """
    Check if employee has enough PTO for a half day off (4 hours).
    Uses if-else logic to determine availability.
    
    Returns:
        str: Whether a half day can be taken
    """
    if PTO_HOURS_AVAILABLE >= 4:
        return f"Yes, you can take a half day off. You have {PTO_HOURS_AVAILABLE} hours available."
    else:
        return f"No, you don't have enough PTO for a half day. You only have {PTO_HOURS_AVAILABLE} hours available."
    
@mcp.tool()
def how_many_days_taken() -> str:
    """
    Check to see how may hours the employee has taken this year. 
    Uses if-else logic to determine availability.
    
    Returns:
        str: How many days the employee has taken this year
    """

    days = PTO_HOURS_TAKEN / 8
    return f"You have taken {days} PTO days off this year. You have ({PTO_HOURS_AVAILABLE} hours)."


if __name__ == "__main__":
    # Run the MCP server over HTTP at 127.0.0.1:8000
    print("🚀 Starting PTO Hours MCP Server over HTTP...")
    print("📡 Server URL: http://127.0.0.1:8000")
    print("⚙️  Available tools: get_pto_hours, get_pto_days, can_take_full_day, can_take_half_day")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 60)
    
    # Run server with SSE transport over HTTP
    mcp.run(transport="sse", host="127.0.0.1", port=8000)

