# K-Map Solver MCP Server

This is a project that encapsulates a Karnaugh Map (K-Map) solver into an MCP (Model Context Protocol) server.

## Features

- Supports 2, 3, 4 variable K-Map solving
- Provides simplified Boolean expressions
- Visualizes K-Map input
- Supports "don't care" conditions (value 2)

## Installation

```bash
pip install -r requirements.txt
```

## MCP Server Tools

### 1. solve_kmap_2
Solve 2-variable K-Map
- **Input**: 2x2 matrix
- **Values**: 0=false, 1=true, 2=don't care
- **Example**: `[[1, 0], [0, 1]]`

### 2. solve_kmap_3
Solve 3-variable K-Map
- **Input**: 2x4 matrix
- **Values**: 0=false, 1=true, 2=don't care
- **Example**: `[[1, 0, 0, 1], [0, 1, 1, 0]]`

### 3. solve_kmap_4
Solve 4-variable K-Map
- **Input**: 4x4 matrix
- **Values**: 0=false, 1=true, 2=don't care
- **Example**: `[[1, 0, 0, 1], [0, 1, 1, 0], [0, 1, 1, 0], [1, 0, 0, 1]]`

### 4. get_kmap_info
Get K-Map usage instructions and information

## Usage

### 1. Run MCP server directly

```bash
python mcp_server.py
```

### 2. Test MCP server

```bash
python test_mcp.py
```

### 3. Configure in MCP client

Add the following configuration to your MCP client configuration file:

```json
{
  "mcpServers": {
    "kmap-solver": {
      "command": "python",
      "args": ["mcp_server.py"],
      "env": {
        "PYTHONPATH": "."
      }
    }
  }
}
```

## K-Map Layout Description

### 2-Variable K-Map (2x2)
```
A\B  0  1
 0  [0][0]
 1  [0][0]
```

### 3-Variable K-Map (2x4)
```
A\BC 00  01  11  10
 0   [0][0][0][0]
 1   [0][0][0][0]
```

### 4-Variable K-Map (4x4)
```
AB\CD 00  01  11  10
  00  [0][0][0][0]
  01  [0][0][0][0]
  11  [0][0][0][0]
  10  [0][0][0][0]
```

## Examples

### 2-Variable K-Map Example
Input: `[[1, 0], [0, 1]]`
Output: `F(A,B) = A'B + AB'`

### 3-Variable K-Map Example
Input: `[[1, 0, 0, 1], [0, 1, 1, 0]]`
Output: `F(A,B,C) = A'B'C' + A'BC + AB'C + ABC'`

## Integration with Large Models

Once the MCP server is configured, large models can call it in the following ways:

1. **List available tools**: Models can view all available K-Map solving tools
2. **Call solver**: Models can pass K-Map data and get simplified Boolean expressions
3. **Get help information**: Models can get K-Map usage instructions

## Error Handling

- Input validation: Ensure matrix size is correct
- Value validation: Ensure all values are 0, 1, or 2
- Exception handling: Provide clear error messages

## File Structure

```
KMapSolver/
├── main.py              # Original GUI program
├── guis.py              # GUI interface code
├── solvers.py           # K-Map solver core
├── helpers.py           # Helper functions
├── mcp_server.py        # MCP server
├── test_mcp.py          # Test script
├── requirements.txt     # Dependencies
├── kmap-solver.json    # MCP configuration file
└── README_MCP.md       # This file
``` 