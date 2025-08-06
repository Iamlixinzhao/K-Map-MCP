#!/usr/bin/env python3

import asyncio
import json
import subprocess
import sys
from typing import Dict, Any

async def test_mcp_server():
    """测试MCP服务器的功能"""
    
    # 启动MCP服务器
    process = subprocess.Popen(
        [sys.executable, "mcp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # 发送初始化请求
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        # 发送初始化请求
        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.flush()
        
        # 读取响应
        response = process.stdout.readline()
        print("初始化响应:", response)
        
        # 发送list_tools请求
        list_tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        process.stdin.write(json.dumps(list_tools_request) + "\n")
        process.stdin.flush()
        
        response = process.stdout.readline()
        print("工具列表响应:", response)
        
        # 测试2变量K-Map求解
        test_kmap_2_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "solve_kmap_2",
                "arguments": {
                    "map_data": [[1, 0], [0, 1]]
                }
            }
        }
        
        process.stdin.write(json.dumps(test_kmap_2_request) + "\n")
        process.stdin.flush()
        
        response = process.stdout.readline()
        print("2变量K-Map测试响应:", response)
        
        # 测试3变量K-Map求解
        test_kmap_3_request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "solve_kmap_3",
                "arguments": {
                    "map_data": [[1, 0, 0, 1], [0, 1, 1, 0]]
                }
            }
        }
        
        process.stdin.write(json.dumps(test_kmap_3_request) + "\n")
        process.stdin.flush()
        
        response = process.stdout.readline()
        print("3变量K-Map测试响应:", response)
        
        # 测试4变量K-Map求解
        test_kmap_4_request = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "solve_kmap_4",
                "arguments": {
                    "map_data": [
                        [1, 0, 0, 1],
                        [0, 1, 1, 0],
                        [0, 1, 1, 0],
                        [1, 0, 0, 1]
                    ]
                }
            }
        }
        
        process.stdin.write(json.dumps(test_kmap_4_request) + "\n")
        process.stdin.flush()
        
        response = process.stdout.readline()
        print("4变量K-Map测试响应:", response)
        
    except Exception as e:
        print(f"测试过程中出错: {e}")
    finally:
        # 关闭进程
        process.terminate()
        process.wait()

if __name__ == "__main__":
    asyncio.run(test_mcp_server()) 