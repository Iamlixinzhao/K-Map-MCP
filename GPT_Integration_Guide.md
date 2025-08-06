# GPT-4o and K-Map Solver Integration Guide

## Overview

This project integrates a Karnaugh Map (K-Map) solver with OpenAI's GPT-4o model, enabling large models to intelligently handle K-Map related problems.

## File Description

### 1. `simple_gpt_test.py` - Simplified Test Version
- Directly simulates MCP tool calls
- Suitable for quick testing and verification
- Includes basic 2 and 3 variable K-Map solving functionality

### 2. `openai_kmap_client.py` - Complete MCP Integration Version
- Communicates with real MCP server
- Supports complete K-Map solving functionality
- Includes all 2, 3, 4 variable K-Map solving tools

## Usage

### Quick Test (Recommended first)

```bash
python simple_gpt_test.py
```

### Complete Function Test

```bash
python openai_kmap_client.py
```

## Features

### 1. Intelligent Dialogue
- Users can describe K-Map problems in natural language
- GPT-4o automatically recognizes and calls appropriate tools

### 2. Supported Question Types

#### Knowledge Inquiry
```
User: "What is K-Map?"
GPT-4o: Calls get_kmap_info tool, returns detailed explanation
```

#### 2-Variable K-Map Solving
```
User: "Help me solve this 2-variable K-Map: [[1, 0], [0, 1]]"
GPT-4o: Calls solve_kmap_2 tool, returns result
```

#### 3-Variable K-Map Solving
```
User: "Solve 3-variable K-Map: [[1, 0, 0, 1], [0, 1, 1, 0]]"
GPT-4o: Calls solve_kmap_3 tool, returns result
```

#### 4-Variable K-Map Solving (Full Version)
```
User: "Solve 4-variable K-Map: [[1, 0, 0, 1], [0, 1, 1, 0], [0, 1, 1, 0], [1, 0, 0, 1]]"
GPT-4o: Calls solve_kmap_4 tool, returns result
```

## 示例对话

### 示例1：询问K-Map知识
```
用户: 什么是K-Map？
GPT-4o: Karnaugh Map (K-Map) 是一种用于简化布尔代数表达式的图形方法...

[详细说明包括布局、使用方法等]
```

### 示例2：求解2变量K-Map
```
用户: 帮我求解这个2变量K-Map: [[1, 0], [0, 1]]
GPT-4o: 
K-Map Input:
A\B  0  1
 0  [1][0]
 1  [0][1]

Simplified Boolean Expression: F(A,B) = A'B + AB'
```

### 示例3：求解3变量K-Map
```
用户: 求解3变量K-Map: [[1, 0, 0, 1], [0, 1, 1, 0]]
GPT-4o: 
K-Map Input:
A\BC 00  01  11  10
 0   [1][0][0][1]
 1   [0][1][1][0]

Simplified Boolean Expression: F(A,B,C) = A'B'C' + A'BC + AB'C + ABC'
```

## 技术架构

### 简化版本架构
```
用户输入 → GPT-4o分析 → 调用本地工具函数 → 返回结果给GPT-4o → 生成最终回答
```

### 完整版本架构
```
用户输入 → GPT-4o分析 → 调用MCP服务器 → MCP服务器调用真实K-Map求解器 → 返回结果给GPT-4o → 生成最终回答
```

## 配置说明

### API密钥设置
在代码中设置你的OpenAI API密钥：
```python
OPENAI_API_KEY = "your-api-key-here"
```

### 依赖安装
```bash
pip install openai mcp wxPython
```

## 优势

### 1. 智能理解
- GPT-4o能够理解用户的自然语言描述
- 自动识别K-Map的变量数量和数据结构

### 2. 专业求解
- 使用真实的K-Map求解算法
- 提供准确的布尔表达式简化结果

### 3. 可视化输出
- 返回格式化的K-Map可视化
- 清晰显示输入和输出

### 4. 教育价值
- 可以解释K-Map的概念和原理
- 提供学习指导和示例

## 使用建议

### 1. 输入格式
- 使用标准的矩阵格式：`[[1, 0], [0, 1]]`
- 确保矩阵大小正确（2x2, 2x4, 4x4）
- 值只能是0、1或2（don't care）

### 2. 问题类型
- 知识询问：直接问"什么是K-Map？"
- 求解请求：提供矩阵数据
- 学习指导：询问如何使用K-Map

### 3. 输出理解
- 可视化部分：显示K-Map的布局
- 结果部分：简化的布尔表达式
- 解释部分：GPT-4o的额外说明

## 故障排除

### 常见问题

1. **API密钥错误**
   - 确保API密钥正确设置
   - 检查API密钥的有效性

2. **网络连接问题**
   - 确保网络连接正常
   - 检查防火墙设置

3. **依赖包问题**
   - 运行 `pip install -r requirements.txt`
   - 确保所有依赖都已安装

### 调试模式
在代码中添加调试信息：
```python
print(f"调用工具: {tool_name}")
print(f"参数: {arguments}")
```

## 扩展功能

### 1. 批量处理
可以扩展支持批量处理多个K-Map：
```python
kmap_list = [
    [[1, 0], [0, 1]],
    [[1, 0, 0, 1], [0, 1, 1, 0]]
]
```

### 2. 文件输入
可以支持从文件读取K-Map数据：
```python
# 从JSON文件读取K-Map数据
with open('kmap_data.json', 'r') as f:
    kmap_data = json.load(f)
```

### 3. 结果保存
可以将求解结果保存到文件：
```python
# 保存结果到文件
with open('results.txt', 'w') as f:
    f.write(result)
```

## 总结

这个集成方案将GPT-4o的智能理解能力与专业的K-Map求解算法相结合，为用户提供了一个强大而智能的布尔代数简化工具。用户可以用自然语言描述问题，系统会自动调用相应的工具来求解，并返回格式化的结果。 