# SCI-two-ppt 项目指南

## 项目概述
AI-powered scientific paper to presentation PPT generator.

## 注意要求
回复过程中全部说中文

## 架构原则
- **Claude 是大脑**：多轮对话、批判审查、创意决策由 Claude 完成
- **MCP Server 是手脚**：PDF解析、PPT生成等确定性操作由 Python 工具完成
- **子 Agent 自由协作**：通过共享 workspace 传递结果

## 核心文件
- `src/mcp_server.py` - MCP Server 入口，注册所有工具
- `src/core/config.py` - 配置加载器
- `src/core/workspace.py` - 工作空间管理器
- `docs/superpowers/specs/2026-05-22-sci-two-ppt-architecture-design.md` - 完整设计文档

## 开发规范
- Python 3.10+
- 使用 `mcp` Python SDK（FastMCP）
- 所有工具返回 JSON 格式
- workspace 路径默认 `./workspace`
- 配置优先级: settings.local.yaml > settings.yaml

## MCP 工具清单

### 论文解析
1. `parse_papers` - 提取论文原始文本
2. `extract_figures` - 提取图表

### SVG引擎
3. `generate_svg_slide` - 生成幻灯片SVG
4. `generate_svg_chart` - 生成图表SVG
5. `svg_to_pptx` - SVG转PPTX
6. `check_svg_quality` - 质量检查

### PPT生成
7. `build_slide` - 生成单页幻灯片
8. `generate_pptx` - 最终打包
9. `read_pptx` - 读取PPTX状态
10. `diff_pptx` - 对比PPTX差异

### 规范库
11. `get_academic_style` - 学术规范
12. `get_slide_template` - 页面模板
13. `get_citation_format` - 引用格式

### 预览系统
14. `generate_preview` - 生成预览
15. `generate_preview_from_pptx` - PPTX预览
16. `start_preview_server` - 启动WebSocket

### 反馈系统
17. `detect_modifications` - 检测修改
18. `learn_feedback` - 学习反馈
19. `get_feedback_patterns` - 获取反馈模式

### 工作空间
20. `cleanup_workspace` - 清理文件
21. `get_latest_feedback` - 获取反馈

## 测试
- 运行测试: `python -m pytest tests/`
- 验证MCP Server: `python -m src.mcp_server`
