#!/usr/bin/env python3

import asyncio
import json
import subprocess
import sys
from typing import Dict, Any, List
import openai
from openai import AsyncOpenAI

# 设置OpenAI API密钥
OPENAI_API_KEY = "your-api-key-here"

class KMapMCPClient:
    """K-Map MCP client for communicating with MCP server"""
    
    def __init__(self):
        self.process = None
        self.request_id = 1
    
    async def start_server(self):
        """Start MCP server"""
        self.process = subprocess.Popen(
            [sys.executable, "simple_mcp_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 发送初始化请求
        init_request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "openai-client",
                    "version": "1.0.0"
                }
            }
        }
        
        await self._send_request(init_request)
        self.request_id += 1
    
    async def _send_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Send request to MCP server"""
        if not self.process:
            raise RuntimeError("MCP server not started")
        
        # Send request
        self.process.stdin.write(json.dumps(request) + "\n")
        self.process.stdin.flush()
        
        # Read response
        response = self.process.stdout.readline()
        return json.loads(response)
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """Get available tools list"""
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/list"
        }
        
        response = await self._send_request(request)
        self.request_id += 1
        
        if "result" in response:
            return response["result"]["tools"]
        else:
            raise Exception(f"Failed to get tools list: {response}")
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> str:
        """Call MCP tool"""
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments
            }
        }
        
        response = await self._send_request(request)
        self.request_id += 1
        
        if "result" in response:
            # Extract text content
            content = response["result"]["content"]
            if content and len(content) > 0:
                return content[0]["text"]
            return "No result"
        else:
            raise Exception(f"Failed to call tool: {response}")
    
    async def stop_server(self):
        """Stop MCP server"""
        if self.process:
            self.process.terminate()
            self.process.wait()

class OpenAIKMapAssistant:
    """K-Map assistant using OpenAI GPT-4o"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        self.mcp_client = KMapMCPClient()
        self.tools = []
    
    async def initialize(self):
        """Initialize MCP server and tools list"""
        await self.mcp_client.start_server()
        self.tools = await self.mcp_client.list_tools()
        print(f"Available tools: {[tool['name'] for tool in self.tools]}")
    
    async def chat_with_gpt(self, user_message: str) -> str:
        """Chat with GPT-4o, handle K-Map related requests"""
        
        # Build tool call format
        tools = []
        for tool in self.tools:
            tools.append({
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["inputSchema"]
                }
            })
        
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
                    
                    # Call MCP tool
                    result = await self.mcp_client.call_tool(tool_name, arguments)
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
    
    async def close(self):
        """Close connection"""
        await self.mcp_client.stop_server()

async def main():
    """Main function"""
    assistant = OpenAIKMapAssistant()
    
    try:
        print("Initializing K-Map assistant...")
        await assistant.initialize()
        print("Initialization complete!")
        print("\n=== K-Map Assistant Ready ===")
        print("You can ask the following types of questions:")
        print("1. 'What is K-Map?'")
        print("2. 'Help me solve this 2-variable K-Map: [[1, 0], [0, 1]]'")
        print("3. 'Solve 3-variable K-Map: [[1, 0, 0, 1], [0, 1, 1, 0]]'")
        print("4. 'exit' to end the program")
        print("=" * 40)
        
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            
            print("GPT-4o: Processing...")
            response = await assistant.chat_with_gpt(user_input)
            print(f"GPT-4o: {response}")
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await assistant.close()
        print("Program exited")

if __name__ == "__main__":
    asyncio.run(main()) 