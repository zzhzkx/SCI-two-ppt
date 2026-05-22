# SCI-two-ppt 技术设计文档

## 架构概述

SCI-two-ppt 是一个基于 MCP Server 的学术论文转PPT工具，采用"Claude是大脑，MCP是手脚"的架构设计。

### 核心设计理念

1. **Claude 是大脑**：多轮对话、需求分析、批判审查、创意决策由 Claude 完成
2. **MCP Server 是手脚**：PDF解析、PPT生成等确定性操作由 Python 工具完成
3. **子 Agent 自由协作**：通过共享 workspace 传递结果

### 架构图

```
┌─────────────────────────────────────────────────┐
│              Claude Code (编排层)                  │
│                                                   │
│  主 Agent ──── 多轮对话收集需求                    │
│       │       批判性审查各阶段产出                  │
│       │       编排调度子 Agent 和 MCP 工具         │
│       │                                           │
│       ├─ spawn 子 Agent 1: 论文分析专家            │
│       ├─ spawn 子 Agent 2: 内容策略师              │
│       ├─ spawn 子 Agent 3: 视觉设计师              │
│       ├─ spawn 子 Agent 4: 幻灯片构建师            │
│       ├─ spawn 子 Agent 5: 质量审查员              │
│       ├─ spawn 子 Agent 6: 论文教授审查员          │
│       └─ spawn 子 Agent 7: 素材搜集员              │
└───────────────────────┬─────────────────────────┘
                        │ MCP Protocol (stdio)
                        ▼
┌─────────────────────────────────────────────────┐
│          MCP Server (Python 工具 + 规范库)        │
│                                                   │
│  工具层:                                           │
│  ├─ parse_papers()      解析论文 PDF/Word         │
│  ├─ extract_figures()   提取图表                  │
│  ├─ build_slide()       生成单页幻灯片            │
│  ├─ generate_pptx()     最终打包                  │
│  └─ ...                                           │
│                                                   │
│  规范库:                                           │
│  ├─ get_academic_style() 学术规范                 │
│  ├─ get_slide_template() 页面模板                 │
│  └─ get_citation_format() 引用格式                │
└─────────────────────────────────────────────────┘
```

## 角色系统

### 7个核心角色

1. **Paper Analyzer (论文分析专家)**
   - 职责：解析论文、提取关键信息、生成检索式
   - 输入：原始论文文本
   - 输出：analysis.json, search_queries.json

2. **Content Strategist (内容策略师)**
   - 职责：分析创新点、规划章节结构、分配时间
   - 输入：analysis.json, requirements.md
   - 输出：goal.md, chapter_structure.md

3. **Visual Designer (视觉设计师)**
   - 职责：设计配色、规划布局、选择图表风格
   - 输入：goal.md, research_field
   - 输出：ui_design.md, spec_lock.md

4. **Slide Builder (幻灯片构建师)**
   - 职责：逐页生成PPT、添加动画、优化细节
   - 输入：blueprint.yaml, spec_lock.md
   - 输出：slide_*.pptx, preview

5. **Quality Reviewer (质量审查员)**
   - 职责：学术审查、视觉审查、听众体验审查
   - 输入：goal.md, slides, requirements
   - 输出：review_report.md

6. **Professor Reviewer (论文教授审查员)**
   - 职责：专业学术审查、成果完整性评估
   - 输入：analysis.json, agent_results, goal.md
   - 输出：expert_review.md

7. **Material Collector (素材搜集员)**
   - 职责：从学术期刊搜集PPT素材
   - 输入：research_field, core_keywords
   - 输出：materials/, material_collection.md

### 角色协作流程

```
Paper Analyzer → Content Strategist → Visual Designer
      ↓                ↓                    ↓
  analysis.json    goal.md           spec_lock.md
      ↓                ↓                    ↓
Professor Reviewer ← Material Collector ← Slide Builder
      ↓                ↓                    ↓
  review_report    materials/          slides
      ↓                ↓                    ↓
      └────────────────┴────────────────────┘
                       ↓
              Quality Reviewer (最终审查)
```

## 设计规范系统

### 双文件模式

1. **design_spec.md** - 人类可读的设计叙事
   - 研究背景和目的
   - 核心创新点
   - 内容结构规划
   - 视觉设计理念
   - 讲解策略

2. **spec_lock.md** - 机器可读的执行锁
   - 颜色规范
   - 字体规范
   - 页面布局
   - 图表风格

### 执行纪律

- **每页重读spec_lock**：防止上下文压缩导致的漂移
- **逐页生成**：避免批量生成导致的问题
- **视觉一致性**：确保所有页面风格统一

## 工作流程

### 10步工作流

1. **Step 1: 论文解析**
   - 调用 parse_papers 提取原始文本
   - spawn子Agent智能分析论文
   - 生成检索式

2. **Step 2: 需求收集**
   - 智能推荐PPT用途
   - 分层询问需求
   - 生成 requirements.md

3. **Step 3: 目标构建**
   - spawn子Agent构建 goal.md
   - 综合论文分析和用户需求
   - 识别信息缺失

4. **Step 4: 双角色审查**
   - 领域专家审查学术严谨性
   - PPT制作师审查展示效果
   - 综合两方面建议

5. **Step 5: 子Agent执行**
   - 7个子Agent并行执行任务
   - 通过workspace共享结果
   - 产出多个agent_results文件

6. **Step 6: 审查确认**
   - 读取所有Agent产出
   - 向用户展示结果摘要
   - 用户确认或修改

7. **Step 7: 蓝图生成**
   - 综合所有信息
   - 生成 blueprint.yaml

8. **Step 8: 逐页制作**
   - 读取 spec_lock.md
   - 逐页生成幻灯片
   - 用户确认或修改

9. **Step 9: 最终打包**
   - 合并所有幻灯片
   - 生成 output_final.pptx

10. **Step 10: 整理文件**
    - 生成制作报告
    - 清理中间文件

## MCP 工具

### 工具列表

| 工具名 | 用途 | 输入 | 输出 |
|--------|------|------|------|
| parse_papers | 解析论文 | PDF/Word路径 | analysis.json |
| extract_figures | 提取图表 | PDF路径 | 图表文件 |
| build_slide | 生成幻灯片 | blueprint + index | slide.pptx |
| generate_pptx | 最终打包 | blueprint | output.pptx |
| get_academic_style | 学术规范 | 领域 | 配色/字体 |
| get_slide_template | 页面模板 | 类型 | 模板定义 |

### 工具接口示例

```python
@mcp.tool()
def parse_papers(papers: list[str]) -> str:
    """解析论文，提取原始文本。
    
    Input: papers - 论文文件路径列表
    Output: JSON with raw_text, metadata
    """
    # 实现...
    return json.dumps(result)
```

## 模板系统

### 布局模板

- 学术答辩风格
- 会议报告风格
- 组会汇报风格

### 图表模板

- 柱状图、折线图、散点图
- 流程图、架构图
- 对比图表

### 学术规范库

- 光学/物理领域：蓝色调
- 生物/医学领域：绿色调
- 计算机/工程领域：紫色调

## 文件结构

```
sci_two_ppt/
├── skills/                    # Skill文档
│   └── sci-two-ppt/
│       ├── SKILL.md          # 主入口
│       ├── references/       # 角色规范
│       ├── workflows/        # 工作流文档
│       └── templates/        # 设计模板
├── src/                       # 核心代码
│   ├── mcp_server.py         # MCP Server
│   ├── parsers/              # 论文解析
│   ├── generators/           # PPT生成
│   └── styles/               # 学术规范
├── examples/                  # 示例项目
├── templates/                 # PPT模板
├── workspace/                 # 用户工作区
└── docs/                      # 文档
```

## 扩展性

### 添加新角色

1. 创建 `references/new-role.md` 规范文档
2. 在 `SKILL.md` 中添加角色说明
3. 在工作流文档中添加调用方式

### 添加新工具

1. 在 `src/` 下实现工具功能
2. 在 `mcp_server.py` 中注册工具
3. 更新文档说明

### 添加新模板

1. 在 `templates/` 下添加模板文件
2. 更新模板索引
3. 更新文档说明
