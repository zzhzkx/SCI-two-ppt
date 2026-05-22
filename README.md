# SCI-two-ppt

AI-powered scientific paper to presentation PPT generator.

## 项目结构

```
F:\sci_two_ppt\
├── workspace/                    # 用户工作区（核心）
│   ├── input/                   # 📥 用户输入文件
│   ├── agent_results/           # 🤖 子Agent输出
│   ├── papers/                  # 📄 论文解析结果
│   ├── output/                  # 📤 最终PPT输出
│   ├── preview/                 # 👁️ 预览文件
│   └── temp/                    # 🗑️ 临时文件
│
├── src/                         # 核心代码
│   ├── mcp_server.py           # MCP Server入口
│   ├── core/                   # 核心模块
│   ├── parsers/                # 论文解析
│   ├── generators/             # PPT生成
│   └── styles/                 # 学术规范库
│
├── templates/                   # PPT模板
├── skills/                      # Skill文件
├── tests/                       # 测试
├── docs/                        # 文档
├── .claude/                     # Claude配置
└── config/                      # 配置文件
```

## 快速开始

### 1. 输入论文
将论文文件放入 `workspace/input/` 目录

### 2. 在 Claude Code 中使用
```
帮我把 workspace/input/ 下的论文做成PPT
```

### 3. 查看结果
- **最终PPT**：`workspace/output/output_final.pptx`
- **Agent产出**：`workspace/agent_results/`
- **过程文档**：`workspace/papers/`

## 工作流程（10步）

1. **论文解析** - 解析PDF/Word文档
2. **需求收集** - 与用户对话收集需求
3. **目标构建** - 构建goal.md
4. **批判审查** - 审查目标文档
5. **子Agent执行** - 并行spawn多个子Agent
6. **用户确认** - 确认Agent产出
7. **蓝图生成** - 生成PPT蓝图
8. **逐页制作** - 生成单页PPT
9. **最终打包** - 合并为完整PPT
10. **文件整理** - 清理和归档

## 子Agent并行执行

使用Claude Code的Agent工具spawn独立会话：
- **论文要点提取** - 分析论文核心内容
- **创新点提炼** - 提炼研究创新性
- **UI风格设计** - 设计PPT视觉风格
- **章节结构安排** - 规划PPT结构
- **讲解备注编写** - 编写演讲备注

## MCP工具

| 工具名 | 用途 |
|--------|------|
| parse_papers | 解析论文（PDF/Word） |
| extract_figures | 提取图表 |
| build_slide | 生成单页PPT |
| generate_pptx | 最终打包 |
| get_academic_style | 学术规范 |
| get_slide_template | 页面模板 |

## 安装

```bash
git clone https://github.com/zzhzkx/SCI-two-ppt.git
cd SCI-two-ppt
pip install -r requirements.txt
```

## 配置MCP Server

在Claude Code设置中添加：
```json
{
  "mcpServers": {
    "sci-two-ppt": {
      "command": "python",
      "args": ["-m", "src.mcp_server"],
      "cwd": "F:\\sci_two_ppt"
    }
  }
}
```

## License

MIT
