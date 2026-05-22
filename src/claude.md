# src/ 源代码目录指南

## 模块结构
```
src/
├── mcp_server.py      # MCP Server 入口
├── core/              # 核心配置和工具
├── parsers/           # PDF/PPTX 解析模块
├── generators/        # PPT 生成模块
├── styles/            # 学术规范库
└── utils/             # 通用工具函数
```

## 开发流程
1. 在对应模块下实现功能
2. 在 `mcp_server.py` 注册为 MCP 工具
3. 在 `tests/` 添加测试

## 代码规范
- 类型注解: 使用 Python 3.10+ 类型语法
- 异步: MCP 工具使用 async/await
- 错误处理: 返回结构化 JSON 错误
- 日志: 使用 `src.core.logging` 模块

## MCP 工具注册
```python
@mcp.tool()
async def tool_name(param: str) -> str:
    """工具说明。
    
    Input: param - 参数说明
    Output: JSON 结构说明
    """
    # 实现
    return json.dumps({...})
```
