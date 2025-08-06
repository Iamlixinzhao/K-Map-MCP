#!/usr/bin/env python3

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel,
)
from solvers import KMapSolver2, KMapSolver3, KMapSolver4

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server
server = Server("kmap-solver")

# Tool definitions
TOOLS = [
    Tool(
        name="solve_kmap_2",
        description="Solve a 2-variable Karnaugh Map. Input should be a 2x2 matrix with values 0, 1, or 2 (don't care).",
        inputSchema={
            "type": "object",
            "properties": {
                "map_data": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {"type": "integer", "enum": [0, 1, 2]},
                        "minItems": 2,
                        "maxItems": 2
                    },
                    "minItems": 2,
                    "maxItems": 2,
                    "description": "2x2 matrix representing the K-Map. Values: 0=false, 1=true, 2=don't care"
                }
            },
            "required": ["map_data"]
        }
    ),
    Tool(
        name="solve_kmap_3",
        description="Solve a 3-variable Karnaugh Map. Input should be a 2x4 matrix with values 0, 1, or 2 (don't care).",
        inputSchema={
            "type": "object",
            "properties": {
                "map_data": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {"type": "integer", "enum": [0, 1, 2]},
                        "minItems": 4,
                        "maxItems": 4
                    },
                    "minItems": 2,
                    "maxItems": 2,
                    "description": "2x4 matrix representing the K-Map. Values: 0=false, 1=true, 2=don't care"
                }
            },
            "required": ["map_data"]
        }
    ),
    Tool(
        name="solve_kmap_4",
        description="Solve a 4-variable Karnaugh Map. Input should be a 4x4 matrix with values 0, 1, or 2 (don't care).",
        inputSchema={
            "type": "object",
            "properties": {
                "map_data": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {"type": "integer", "enum": [0, 1, 2]},
                        "minItems": 4,
                        "maxItems": 4
                    },
                    "minItems": 4,
                    "maxItems": 4,
                    "description": "4x4 matrix representing the K-Map. Values: 0=false, 1=true, 2=don't care"
                }
            },
            "required": ["map_data"]
        }
    ),
    Tool(
        name="get_kmap_info",
        description="Get information about Karnaugh Maps and how to use this solver.",
        inputSchema={
            "type": "object",
            "properties": {},
            "additionalProperties": False
        }
    )
]

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """List available tools."""
    return ListToolsResult(tools=TOOLS)

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls."""
    try:
        if name == "solve_kmap_2":
            return await solve_kmap_2(arguments)
        elif name == "solve_kmap_3":
            return await solve_kmap_3(arguments)
        elif name == "solve_kmap_4":
            return await solve_kmap_4(arguments)
        elif name == "get_kmap_info":
            return await get_kmap_info()
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Unknown tool: {name}")]
            )
    except Exception as e:
        logger.error(f"Error in tool {name}: {str(e)}")
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error: {str(e)}")]
        )

async def solve_kmap_2(arguments: Dict[str, Any]) -> CallToolResult:
    """Solve 2-variable K-Map."""
    map_data = arguments.get("map_data")
    if not map_data or len(map_data) != 2 or any(len(row) != 2 for row in map_data):
        return CallToolResult(
            content=[TextContent(type="text", text="Error: Invalid input. Expected 2x2 matrix.")]
        )
    
    try:
        solver = KMapSolver2(map_data)
        solver.solve()
        result = solver.get_result()
        
        # Create visual representation
        visual_map = create_visual_map(map_data, 2)
        
        return CallToolResult(
            content=[
                TextContent(type="text", text=f"K-Map Input:\n{visual_map}\n\nSimplified Boolean Expression: F(A,B) = {result}")
            ]
        )
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error solving K-Map: {str(e)}")]
        )

async def solve_kmap_3(arguments: Dict[str, Any]) -> CallToolResult:
    """Solve 3-variable K-Map."""
    map_data = arguments.get("map_data")
    if not map_data or len(map_data) != 2 or any(len(row) != 4 for row in map_data):
        return CallToolResult(
            content=[TextContent(type="text", text="Error: Invalid input. Expected 2x4 matrix.")]
        )
    
    try:
        solver = KMapSolver3(map_data)
        solver.solve()
        result = solver.get_result()
        
        # Create visual representation
        visual_map = create_visual_map(map_data, 3)
        
        return CallToolResult(
            content=[
                TextContent(type="text", text=f"K-Map Input:\n{visual_map}\n\nSimplified Boolean Expression: F(A,B,C) = {result}")
            ]
        )
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error solving K-Map: {str(e)}")]
        )

async def solve_kmap_4(arguments: Dict[str, Any]) -> CallToolResult:
    """Solve 4-variable K-Map."""
    map_data = arguments.get("map_data")
    if not map_data or len(map_data) != 4 or any(len(row) != 4 for row in map_data):
        return CallToolResult(
            content=[TextContent(type="text", text="Error: Invalid input. Expected 4x4 matrix.")]
        )
    
    try:
        solver = KMapSolver4(map_data)
        solver.solve()
        result = solver.get_result()
        
        # Create visual representation
        visual_map = create_visual_map(map_data, 4)
        
        return CallToolResult(
            content=[
                TextContent(type="text", text=f"K-Map Input:\n{visual_map}\n\nSimplified Boolean Expression: F(A,B,C,D) = {result}")
            ]
        )
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error solving K-Map: {str(e)}")]
        )

async def get_kmap_info() -> CallToolResult:
    """Get information about K-Maps."""
    info = """
# Karnaugh Map (K-Map) Solver

## What is a Karnaugh Map?
A Karnaugh Map (K-Map) is a graphical method used to simplify Boolean algebra expressions. It's a visual way to minimize logic functions.

## How to use this solver:

### 2-Variable K-Map (2x2 matrix)
- Variables: A, B
- Matrix layout:
  ```
  A\\B  0  1
   0  [0][0]
   1  [0][0]
  ```

### 3-Variable K-Map (2x4 matrix)
- Variables: A, B, C
- Matrix layout:
  ```
  A\\BC 00  01  11  10
   0   [0][0][0][0]
   1   [0][0][0][0]
  ```

### 4-Variable K-Map (4x4 matrix)
- Variables: A, B, C, D
- Matrix layout:
  ```
  AB\\CD 00  01  11  10
    00  [0][0][0][0]
    01  [0][0][0][0]
    11  [0][0][0][0]
    10  [0][0][0][0]
  ```

## Input Values:
- 0: False (0)
- 1: True (1)
- 2: Don't care (X)

## Example Usage:
For a 2-variable K-Map with F(A,B) = A'B + AB':
```
map_data: [[1, 0], [0, 1]]
```

The solver will return the simplified Boolean expression.
"""
    
    return CallToolResult(
        content=[TextContent(type="text", text=info)]
    )

def create_visual_map(map_data: List[List[int]], num_vars: int) -> str:
    """Create a visual representation of the K-Map."""
    if num_vars == 2:
        return f"""
A\\B  0  1
 0  [{map_data[0][0]}][{map_data[0][1]}]
 1  [{map_data[1][0]}][{map_data[1][1]}]
"""
    elif num_vars == 3:
        return f"""
A\\BC 00  01  11  10
 0   [{map_data[0][0]}][{map_data[0][1]}][{map_data[0][2]}][{map_data[0][3]}]
 1   [{map_data[1][0]}][{map_data[1][1]}][{map_data[1][2]}][{map_data[1][3]}]
"""
    elif num_vars == 4:
        return f"""
AB\\CD 00  01  11  10
  00  [{map_data[0][0]}][{map_data[0][1]}][{map_data[0][2]}][{map_data[0][3]}]
  01  [{map_data[1][0]}][{map_data[1][1]}][{map_data[1][2]}][{map_data[1][3]}]
  11  [{map_data[2][0]}][{map_data[2][1]}][{map_data[2][2]}][{map_data[2][3]}]
  10  [{map_data[3][0]}][{map_data[3][1]}][{map_data[3][2]}][{map_data[3][3]}]
"""
    return ""

async def main():
    """Main function to run the MCP server."""
    # Create stdio server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="kmap-solver",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main()) 