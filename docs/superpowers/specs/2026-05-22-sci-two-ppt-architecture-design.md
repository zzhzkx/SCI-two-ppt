# SCI-two-ppt 架构设计文档

**日期**: 2026-05-22
**版本**: v1.0
**状态**: 已确认

---

## 1. 项目概述

### 1.1 解决的痛点
1. SVG格式输出无法编辑
2. 缺乏科研PPT专业性
3. AI不懂科研展示重点
4. 无预留学术部分（引用、公式、参考文献）
5. 科研图片绘制不美观

### 1.2 核心设计理念
- **Claude 是大脑**：多轮对话、需求分析、批判审查、创意决策
- **MCP Server 是手脚**：PDF解析、PPT生成等确定性操作
- **子 Agent 自由协作**：通过共享 workspace 传递结果

---

## 2. 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                    用户 (PowerPoint + Claude Code)              │
│  与 Claude 对话 ←→ 在 PowerPoint 中手动修改 ←→ 查看预览         │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    Claude Code (编排层)                        │
│                                                             │
│  主 Agent ──── 多轮对话收集需求                                │
│       │       批判性审查各阶段产出                              │
│       │       编排调度子 Agent 和 MCP 工具                     │
│       │                                                     │
│       ├─ spawn 子 Agent 1: "论文解析 & 要点提取"               │
│       ├─ spawn 子 Agent 2: "核心创新点 & 原理提炼"             │
│       ├─ spawn 子 Agent 3: "仿真代码 & 结果展示"              │
│       ├─ spawn 子 Agent 4: "学术配图 & 美术搜集"              │
│       ├─ spawn 子 Agent 5: "UI风格 & 模板设计"                │
│       ├─ spawn 子 Agent 6: "章节结构 & 节奏安排"              │
│       └─ spawn 子 Agent 7: "讲解备注 & 时间分配"              │
└───────────────────────────┬─────────────────────────────────┘
                            │ MCP Protocol (stdio)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              MCP Server (Python 工具 + 规范库)                 │
│                                                             │
│  工具层:                                                     │
│  ├─ parse_papers()         解析论文 PDF → 结构化内容            │
│  ├─ extract_figures()      提取论文中的图表/图片                │
│  ├─ read_pptx()            读取现有 PPTX 文件状态              │
│  ├─ diff_pptx()            对比两版 PPTX 差异                 │
│  ├─ build_slide()          生成单页幻灯片                      │
│  ├─ render_preview()       渲染幻灯片为图片（预览用）            │
│  ├─ generate_pptx()        最终打包生成 PPTX                   │
│  └─ cleanup_workspace()    整理清理中间文件                     │
│                                                             │
│  规范库层:                                                    │
│  ├─ get_academic_style()   获取学术PPT配色/字体/排版规范         │
│  ├─ get_slide_template()   获取页面模板（封面/内容/图表/总结）    │
│  └─ get_citation_format()  获取引用格式规范                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. 10 步工作流

### Step 1: 输入论文/数据/配图
- **执行者**: Claude 主 Agent
- **流程**: 用户提供PDF → `parse_papers()` → `extract_figures()` → 保存到 workspace
- **产出**: `workspace/papers/analysis.json` + `workspace/inputs/figures/`

### Step 2: 多轮询问需求
- **执行者**: Claude 主 Agent（纯对话）
- **询问维度**: PPT目的、时长、听众、重点、创新点、风格
- **产出**: `workspace/requirements.md`

### Step 3: 分析不足 + 信息补全 → 构建 goal.md
- **执行者**: Claude 主 Agent
- **流程**: 分析缺失 → 模型推理/WebSearch补全 → 构建goal.md
- **产出**: `workspace/goal.md`（初稿）

### Step 4: 批判性审查 + 用户确认
- **执行者**: Claude 主 Agent（批判角色）+ 用户
- **流程**: 批判审查 → 多轮对话确认/修改
- **产出**: `workspace/goal.md`（最终版）

### Step 5: 分派多个子 Agent
- **执行者**: Claude 主 Agent spawn 子 Agent
- **Agent清单**:

| Agent | 任务 | 依赖 | 可用工具 |
|-------|------|------|---------|
| 1. 论文要点提取 | 深度分析论文核心内容 | Step 1 | parse_papers, Read |
| 2. 核心创新点提炼 | 提炼创新点+研究定位 | Agent 1 | WebSearch, parse_papers |
| 3. 仿真代码优化 | 分析仿真代码，优化展示图 | Step 1 | Read, Bash |
| 4. 学术配图搜集 | 搜集/优化论文配图 | Agent 1 | extract_figures, WebSearch |
| 5. 美术图片/icon | 搜集美术素材和图标 | goal.md | WebSearch |
| 6. UI风格设计 | 确定配色、字体、排版 | goal.md | get_academic_style |
| 7. 章节结构安排 | 规划PPT章节和节奏 | Agent 1,2 | Read, Write |
| 8. 讲解备注 | 为每页写讲解备注 | Agent 7 | Read, Write |

- **信息传递**: Agent 间通过 workspace 文件共享结果
- **产出**: `workspace/agent_results/` 下多个 .md 和图片

### Step 6: 批判审查 + 用户确认
- **执行者**: Claude 主 Agent + 用户
- **流程**: 读取所有产出 → 批判审查 → 用户确认 → 不满意重新spawn（最多3轮）
- **产出**: 确认后的 agent_results + `workspace/review_report.md`

### Step 7: 撰写 PPT 制作报告
- **执行者**: Claude 主 Agent
- **流程**: 整合所有确认产出 → 生成详细PPT蓝图
- **产出**: `workspace/ppt_blueprint.yaml`

### Step 8: 逐页制作 + PPT 预览
- **执行者**: Claude 主 Agent + MCP 工具
- **流程**:
  1. `build_slide()` 生成单页PPTX
  2. 用户用PowerPoint打开查看
  3. 用户手动修改 → `diff_pptx()` 检测变化
  4. Claude根据反馈调整 → 重新build或继续下一页
  5. 循环直到所有页确认
- **产出**: 确认的逐页PPTX文件

### Step 9: 生成正式 PPTX
- **执行者**: MCP 工具
- **流程**: `generate_pptx()` 打包所有确认的幻灯片
- **产出**: `workspace/output.pptx`

### Step 10: 整理文件
- **执行者**: MCP 工具 + Claude
- **流程**: `cleanup_workspace()` 清理中间文件，保留有价值文档
- **最终产出**:
```
workspace/
├── output.pptx              # 最终PPT
├── production_report.md     # 制作报告
├── goal.md                  # 目标文档
├── requirements.md          # 需求文档
├── papers/                  # 论文解析结果
├── agent_results/           # Agent产出
├── assets/                  # 图片资源
└── preview/                 # 预览截图
```

---

## 4. MCP 工具设计

### 4.1 工具层（8个）

| 工具名 | 输入 | 输出 | 使用步骤 |
|--------|------|------|---------|
| `parse_papers` | PDF路径列表 | 结构化内容JSON | Step 1, Agent 1,2 |
| `extract_figures` | PDF路径 | 图表文件路径列表 | Step 1, Agent 4 |
| `read_pptx` | PPTX路径 | 幻灯片状态JSON | Step 8 |
| `diff_pptx` | 两版PPTX路径 | 差异报告JSON | Step 8 |
| `build_slide` | 蓝图YAML + 页码 | PPTX + 预览图 | Step 8 |
| `render_preview` | PPTX路径 + 页码 | 预览图片路径 | Step 8 |
| `generate_pptx` | 蓝图YAML | 最终PPTX文件 | Step 9 |
| `cleanup_workspace` | workspace路径 | 清理报告 | Step 10 |

### 4.2 规范库层（3个）

| 工具名 | 输入 | 输出 | 内容 |
|--------|------|------|------|
| `get_academic_style` | 领域 | 配色/字体/排版规范JSON | 学术PPT最佳实践 |
| `get_slide_template` | 页面类型 | 模板定义JSON | 预设页面布局 |
| `get_citation_format` | 格式 | 引用格式规范 | 引用排版规则 |

---

## 5. 项目文件结构

```
sci_two_ppt/
├── .claude/settings.local.json    # MCP注册配置
├── .gitignore
├── README.md
├── requirements.txt
├── setup.py
├── config/
│   ├── settings.yaml              # 默认配置
│   └── settings.local.yaml        # 本地配置
├── src/
│   ├── mcp_server.py              # MCP入口(11个工具)
│   ├── core/
│   │   ├── config.py              # 配置加载器
│   │   ├── workspace.py           # 工作空间管理
│   │   └── logging.py             # 日志系统
│   ├── parsers/
│   │   ├── paper_parser.py        # 论文PDF解析
│   │   ├── figure_extractor.py    # 图表提取
│   │   └── pptx_reader.py         # PPTX读取+差异
│   ├── generators/
│   │   ├── slide_builder.py       # 单页生成
│   │   ├── preview_renderer.py    # 预览渲染
│   │   └── pptx_packager.py       # 最终打包
│   ├── styles/
│   │   ├── academic_styles.py     # 学术规范库
│   │   ├── slide_templates.py     # 页面模板库
│   │   └── citation_formats.py    # 引用格式库
│   └── utils/
├── templates/                     # PPT模板文件
├── data/academic_styles.json      # 规范数据
├── tests/
└── docs/
    └── workflow.md                # 工作流文档
```

---

## 6. 开发里程碑

| 里程碑 | 目标 | 核心产出 |
|--------|------|---------|
| M1 | 基础设施 | 日志系统、修复配置 |
| M2 | 论文解析 | `parse_papers`, `extract_figures` |
| M3 | PPT读写 | `read_pptx`, `diff_pptx`, `build_slide` |
| M4 | 学术规范库 | `get_academic_style`, `get_slide_template` |
| M5 | 模板系统 | 预设模板文件 |
| M6 | 完整集成 | Skill文件 + 测试 |
| M7 | 收尾发布 | 文档 + 示例 |

---

## 7. 验证方案

- M2: 用真实PDF测试 `parse_papers`，检查提取准确性
- M3: 生成单页PPT，用PowerPoint打开验证
- M4: 查询不同领域规范，检查内容质量
- M5: 用模板生成完整PPT，检查排版

质量指标：
- 论文解析准确率 > 80%
- PPT生成成功率 100%
- 单页生成 < 30秒
- 完整流程(10页) < 10分钟
