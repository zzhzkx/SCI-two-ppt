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
1. parse_papers - 解析论文PDF
2. extract_figures - 提取图表
3. read_pptx - 读取PPTX状态
4. diff_pptx - 对比PPTX差异
5. build_slide - 生成单页幻灯片
6. render_preview - 渲染预览图
7. generate_pptx - 最终打包
8. cleanup_workspace - 清理文件
9. get_academic_style - 学术规范
10. get_slide_template - 页面模板
11. get_citation_format - 引用格式

## 测试
- 运行测试: `python -m pytest tests/`
- 验证MCP Server: `python -m src.mcp_server`
