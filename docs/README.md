# SCI-two-ppt

AI-powered scientific paper to presentation PPT generator.

## 特性

- **智能论文解析**：使用LLM分析论文结构、提取关键信息
- **多角色协作**：7个专业角色并行执行任务
- **设计规范系统**：design_spec + spec_lock 双文件确保一致性
- **学术规范库**：支持多个学科领域的配色和排版规范
- **子Agent并行**：使用Claude Code子Agent并行执行任务
- **交互式制作**：逐页生成、用户确认、实时修改

## 安装

```bash
# 克隆仓库
git clone https://github.com/zzhzkx/SCI-two-ppt.git
cd SCI-two-ppt

# 安装依赖
pip install -r requirements.txt

# 配置API密钥
cp config/settings.yaml config/settings.local.yaml
# 编辑 settings.local.yaml 填入你的 API key
```

## 在 Claude Code 中使用

### 配置 MCP Server

在 Claude Code 设置中添加：

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

### 使用方法

在 Claude Code 中说：

```
帮我把这篇论文做成PPT：F:\papers\paper.pdf
```

Claude 会自动执行 10 步工作流：
1. 解析论文
2. 收集需求
3. 构建目标文档
4. 双角色审查
5. 子Agent并行执行
6. 审查确认
7. 生成蓝图
8. 逐页制作
9. 最终打包
10. 整理文件

## 项目结构

```
SCI-two-ppt/
├── skills/                    # Skill文档
│   └── sci-two-ppt/
│       ├── SKILL.md          # 主入口
│       ├── references/       # 7个角色规范
│       ├── workflows/        # 6个工作流文档
│       └── templates/        # 设计规范模板
├── src/                       # 核心代码
│   ├── mcp_server.py         # MCP Server入口
│   ├── parsers/              # 论文解析
│   ├── generators/           # PPT生成
│   └── styles/               # 学术规范
├── examples/                  # 示例项目
│   └── optics_paper/         # 光学论文示例
├── templates/                 # PPT模板
├── workspace/                 # 用户工作区
│   ├── input/               # 输入文件
│   ├── agent_results/       # Agent产出
│   ├── papers/              # 论文分析
│   └── output/              # 最终输出
└── docs/                      # 文档
```

## 工作流程

### Step 1: 论文解析
- 调用 `parse_papers` 提取原始文本
- spawn子Agent智能分析论文
- 生成检索式用于后续文献补充

### Step 2: 需求收集
- 智能推荐PPT用途
- 分层询问需求
- 生成结构化需求文档

### Step 3: 目标构建
- spawn子Agent构建goal.md
- 综合论文分析和用户需求
- 识别信息缺失并提供建议

### Step 4: 双角色审查
- 领域专家：学术严谨性审查
- PPT制作师：展示效果审查
- 综合两方面建议

### Step 5: 子Agent并行执行
- 7个子Agent并行执行任务
- 每个Agent有独立的角色规范
- 通过workspace共享结果

### Step 6-10: 制作输出
- 审查确认
- 生成PPT蓝图
- 逐页制作PPT
- 最终打包输出

## 角色系统

| 角色 | 职责 | 输出 |
|------|------|------|
| Paper Analyzer | 论文分析专家 | analysis.json |
| Content Strategist | 内容策略师 | goal.md |
| Visual Designer | 视觉设计师 | spec_lock.md |
| Slide Builder | 幻灯片构建师 | slide_*.pptx |
| Quality Reviewer | 质量审查员 | review_report.md |
| Professor Reviewer | 论文教授审查员 | expert_review.md |
| Material Collector | 素材搜集员 | materials/ |

## MCP 工具

| 工具名 | 用途 |
|--------|------|
| `parse_papers` | 提取论文原始文本 |
| `extract_figures` | 提取图表 |
| `build_goal` | 构建目标文档 |
| `generate_blueprint` | 生成PPT蓝图 |
| `build_slide` | 生成单页幻灯片 |
| `generate_pptx` | 最终打包 |
| `get_academic_style` | 学术规范 |
| `get_slide_template` | 页面模板 |

## 示例项目

查看 `examples/` 目录了解完整的工作流执行示例：

- `optics_paper/` - 光学论文示例

## 文档

- [技术设计文档](docs/technical-design.md)
- [工作流指南](docs/workflow-guide.md)
- [常见问题](docs/faq.md)

## License

MIT
