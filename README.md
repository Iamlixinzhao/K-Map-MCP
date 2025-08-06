# K-Map Solver with GPT-4o Integration

A comprehensive Karnaugh Map (K-Map) solver that integrates with OpenAI's GPT-4o model, enabling intelligent Boolean algebra simplification through natural language interaction.

> **Note**: This project is based on the original [KMapSolver](https://github.com/salmanmorshed/KMapSolver) by salmanmorshed, which is licensed under the GNU General Public License v2.0. This enhanced version adds GPT-4o integration and MCP server capabilities while maintaining the core K-Map solving functionality.

## Features

- **Multiple Variable Support**: Solves 2, 3, and 4 variable K-Maps
- **AI Integration**: Powered by GPT-4o for intelligent problem understanding
- **Dual Interface**: Both GUI and MCP API interfaces
- **Visual Output**: Provides formatted K-Map visualizations
- **Educational**: Includes detailed explanations and usage guides

## Quick Start

```bash
python working_gpt_client.py
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd KMapSolver
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key in the code files:
```python
OPENAI_API_KEY = "your-api-key-here"
```

## Usage Examples

### Basic K-Map Solving
```
User: "Help me solve this 2-variable K-Map: [[1, 0], [0, 1]]"
GPT-4o: Returns simplified Boolean expression 
```

### Knowledge Queries
```
User: "What is a K-Map?"
GPT-4o: Provides detailed explanation and usage instructions
```

### Complex Problems
```
User: "Solve this 3-variable K-Map: [[1, 0, 0, 1], [0, 1, 1, 0]]"
GPT-4o: Analyzes and returns optimized solution
```

## Project Structure

```
KMapSolver/
├── main.py                    # Original GUI program
├── guis.py                    # GUI interface code
├── solvers.py                 # Core K-Map solving algorithms
├── helpers.py                 # Helper functions
├── mcp_server.py              # MCP server implementation
├── simple_gpt_test.py         # Simplified GPT integration test
├── openai_kmap_client.py      # Full OpenAI integration
├── start_gpt_kmap.py          # Interactive launcher
├── test_mcp.py                # MCP server test
├── requirements.txt           # Python dependencies
├── kmap-solver.json          # MCP configuration
├── README.md                 # This file
├── README_MCP.md             # MCP server documentation
├── GPT_Integration_Guide.md   # GPT integration guide
└── GUI_vs_MCP_Comparison.md  # Interface comparison
```

## MCP Server Tools

The MCP server provides the following tools:

- `solve_kmap_2`: Solve 2-variable K-Maps (2x2 matrix)
- `solve_kmap_3`: Solve 3-variable K-Maps (2x4 matrix)
- `solve_kmap_4`: Solve 4-variable K-Maps (4x4 matrix)
- `get_kmap_info`: Get detailed K-Map information and usage guide

## Input Format

K-Map data should be provided as matrices:
- **2 variables**: 2x2 matrix `[[1, 0], [0, 1]]`
- **3 variables**: 2x4 matrix `[[1, 0, 0, 1], [0, 1, 1, 0]]`
- **4 variables**: 4x4 matrix

Values:
- `0`: False
- `1`: True
- `2`: Don't care (X)

## Examples

### 2-Variable K-Map
Input: `[[1, 0], [0, 1]]`
Output: `F(A,B) = A'B + AB'`

### 3-Variable K-Map
Input: `[[1, 0, 0, 1], [0, 1, 1, 0]]`
Output: `F(A,B,C) = A'B'C' + A'BC + AB'C + ABC'`

## Architecture

### GUI Interface
- Interactive graphical interface
- Real-time visualization
- Manual input through clicking
- Immediate feedback

### MCP API Interface
- Programmatic API calls
- Text-based output
- Automated processing
- Integration capabilities

### GPT-4o Integration
- Natural language understanding
- Intelligent tool selection
- Contextual responses
- Educational explanations

## Dependencies

- `wxPython`: GUI framework
- `openai`: OpenAI API client
- `mcp`: Model Context Protocol
- `asyncio`: Asynchronous programming

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the GNU General Public License v2.0 (GPL-2.0) - see the LICENSE.txt file for details.

## Acknowledgments

This project is based on the original K-Map Solver implementation by [salmanmorshed](https://github.com/salmanmorshed/KMapSolver), which is licensed under the GNU General Public License v2.0.

### Original Project
- **Source**: [https://github.com/salmanmorshed/KMapSolver](https://github.com/salmanmorshed/KMapSolver)
- **Original Author**: salmanmorshed
- **Original License**: GNU General Public License v2.0

### Additional Acknowledgments
- OpenAI GPT-4o API for AI integration
- Model Context Protocol (MCP) specification
- wxPython GUI framework

## Support

For issues and questions:
1. Check the documentation files
2. Review the example usage
3. Test with the simplified version first
4. Open an issue on GitHub

---

**Note**: Make sure to set your OpenAI API key before running the GPT integration features.
