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

## MCP 工具清单（25个工具）

### 论文解析
1. `parse_papers` - 提取论文原始文本
2. `extract_figures` - 提取图表

### 内容规划
3. `build_goal` - 构建PPT目标文档
4. `run_subagent` - 执行7种类型的子Agent任务

### SVG引擎
5. `generate_svg_slide` - 生成幻灯片SVG
6. `generate_svg_chart` - 生成图表SVG
7. `svg_to_pptx` - SVG转PPTX
8. `check_svg_quality` - 质量检查

### PPT生成
9. `build_slide` - 生成单页幻灯片
10. `generate_blueprint` - 生成PPT蓝图YAML
11. `generate_pptx` - 最终打包
12. `read_pptx` - 读取PPTX状态
13. `diff_pptx` - 对比PPTX差异

### 规范库
14. `get_academic_style` - 学术规范
15. `get_slide_template` - 页面模板
16. `get_citation_format` - 引用格式

### 预览系统
17. `generate_preview` - 生成HTML预览
18. `generate_preview_from_pptx` - 从PPTX生成HTML预览
19. `render_preview` - 渲染幻灯片预览图片
20. `start_preview_server` - 启动WebSocket

### 反馈系统
21. `detect_modifications` - 检测修改
22. `learn_feedback` - 学习反馈
23. `get_feedback_patterns` - 获取反馈模式

### 工作空间
- `cleanup_workspace` - 清理文件
- `get_latest_feedback` - 获取反馈

## 测试
- 运行测试: `python -m pytest tests/`
- 验证MCP Server: `python -m src.mcp_server`
