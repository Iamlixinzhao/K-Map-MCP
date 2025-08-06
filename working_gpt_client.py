#!/usr/bin/env python3

import asyncio
import json
from openai import AsyncOpenAI

# Set OpenAI API key
OPENAI_API_KEY = "your-api-key-here"

class WorkingKMapAssistant:
    """Working K-Map assistant that directly simulates tool calls"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    
    def solve_kmap_2(self, map_data):
        """Solve 2-variable K-Map using real solver"""
        try:
            from solvers import KMapSolver2
            solver = KMapSolver2(map_data)
            solver.solve()
            result = solver.get_result()
        except Exception as e:
            result = f"Error: {str(e)}"
        
        visual = f"""
A\\B  0  1
 0  [{map_data[0][0]}][{map_data[0][1]}]
 1  [{map_data[1][0]}][{map_data[1][1]}]
"""
        
        return f"K-Map Input:\n{visual}\n\nSimplified Boolean Expression: F(A,B) = {result}"
    
    def solve_kmap_3(self, map_data):
        """Solve 3-variable K-Map using real solver"""
        try:
            from solvers import KMapSolver3
            solver = KMapSolver3(map_data)
            solver.solve()
            result = solver.get_result()
        except Exception as e:
            result = f"Error: {str(e)}"
        
        visual = f"""
A\\BC 00  01  11  10
 0   [{map_data[0][0]}][{map_data[0][1]}][{map_data[0][2]}][{map_data[0][3]}]
 1   [{map_data[1][0]}][{map_data[1][1]}][{map_data[1][2]}][{map_data[1][3]}]
"""
        return f"K-Map Input:\n{visual}\n\nSimplified Boolean Expression: F(A,B,C) = {result}"
    
    def solve_kmap_4(self, map_data):
        """Solve 4-variable K-Map using real solver"""
        try:
            from solvers import KMapSolver4
            solver = KMapSolver4(map_data)
            solver.solve()
            result = solver.get_result()
        except Exception as e:
            result = f"Error: {str(e)}"
        
        visual = f"""
AB\\CD 00  01  11  10
  00  [{map_data[0][0]}][{map_data[0][1]}][{map_data[0][2]}][{map_data[0][3]}]
  01  [{map_data[1][0]}][{map_data[1][1]}][{map_data[1][2]}][{map_data[1][3]}]
  11  [{map_data[2][0]}][{map_data[2][1]}][{map_data[2][2]}][{map_data[2][3]}]
  10  [{map_data[3][0]}][{map_data[3][1]}][{map_data[3][2]}][{map_data[3][3]}]
"""
        return f"K-Map Input:\n{visual}\n\nSimplified Boolean Expression: F(A,B,C,D) = {result}"
    
    def get_kmap_info(self):
        return """
# Karnaugh Map (K-Map) Solver

## What is a Karnaugh Map?
A Karnaugh Map (K-Map) is a graphical method used to simplify Boolean algebra expressions.

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
"""
    
    async def chat_with_gpt(self, user_message: str) -> str:
        """Chat with GPT-4o"""
        
        # Define tools
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "solve_kmap_2",
                    "description": "Solve a 2-variable Karnaugh Map. Input should be a 2x2 matrix with values 0, 1, or 2 (don't care).",
                    "parameters": {
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
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "solve_kmap_3",
                    "description": "Solve a 3-variable Karnaugh Map. Input should be a 2x4 matrix with values 0, 1, or 2 (don't care).",
                    "parameters": {
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
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "solve_kmap_4",
                    "description": "Solve a 4-variable Karnaugh Map. Input should be a 4x4 matrix with values 0, 1, or 2 (don't care).",
                    "parameters": {
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
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_kmap_info",
                    "description": "Get information about Karnaugh Maps and how to use this solver.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False
                    }
                }
            }
        ]
        
        try:
            # Call GPT-4o
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a Karnaugh Map (K-Map) solving assistant. You can help users:

1. Explain what K-Map is and how to use it
2. Solve 2, 3, 4 variable K-Maps
3. Provide K-Map examples and exercises

When users provide K-Map data, you should call the appropriate tools to solve it.
When users ask about K-Map knowledge, you should call the get_kmap_info tool to get detailed information.

Please always use the provided tools to help users, don't calculate K-Maps yourself."""
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                tools=tools,
                tool_choice="auto"
            )
            
            # Process response
            message = response.choices[0].message
            
            if message.tool_calls:
                # Has tool calls
                tool_results = []
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)
                    
                    print(f"Calling tool: {tool_name}")
                    print(f"Parameters: {arguments}")
                    
                    # Call corresponding tools
                    if tool_name == "solve_kmap_2":
                        result = self.solve_kmap_2(arguments["map_data"])
                    elif tool_name == "solve_kmap_3":
                        result = self.solve_kmap_3(arguments["map_data"])
                    elif tool_name == "solve_kmap_4":
                        result = self.solve_kmap_4(arguments["map_data"])
                    elif tool_name == "get_kmap_info":
                        result = self.get_kmap_info()
                    else:
                        result = f"Unknown tool: {tool_name}"
                    
                    tool_results.append(result)
                
                # Send tool results to GPT
                messages = [
                    {
                        "role": "system",
                        "content": """You are a Karnaugh Map (K-Map) solving assistant."""
                    },
                    {
                        "role": "user",
                        "content": user_message
                    },
                    message,
                    {
                        "role": "tool",
                        "tool_call_id": message.tool_calls[0].id,
                        "content": "\n\n".join(tool_results)
                    }
                ]
                
                # Get final response
                final_response = await self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages
                )
                
                return final_response.choices[0].message.content
            else:
                # No tool calls, return response directly
                return message.content
                
        except Exception as e:
            return f"Error: {str(e)}"

async def main():
    """Main function"""
    assistant = WorkingKMapAssistant()
    
    print("=== K-Map GPT Assistant (Working Version) ===")
    print("You can ask the following types of questions:")
    print("1. 'What is K-Map?'")
    print("2. 'Help me solve this 2-variable K-Map: [[1, 0], [0, 1]]'")
    print("3. 'Solve 3-variable K-Map: [[1, 0, 0, 1], [0, 1, 1, 0]]'")
    print("4. 'Solve 4-variable K-Map: [[1, 0, 0, 1], [0, 1, 1, 0], [0, 1, 1, 0], [1, 0, 0, 1]]'")
    print("5. 'exit' to end the program")
    print("=" * 50)
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        
        print("GPT-4o: Processing...")
        response = await assistant.chat_with_gpt(user_input)
        print(f"GPT-4o: {response}")

if __name__ == "__main__":
    asyncio.run(main()) 