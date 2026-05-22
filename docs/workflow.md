# SCI-two-ppt: MCP Server 架构 & 开发里程碑

## 架构概述

```
┌─────────────────────────────────────────────┐
│              Claude Code (大脑)               │
│  - 多轮对话收集需求（Phase 2）                │
│  - 批判性审查（Phase 3/5）                   │
│  - 编排调度各 MCP 工具                       │
│  - 逐页确认交互（Phase 7）                   │
└────────────────┬────────────────────────────┘
                 │ MCP Protocol (stdio)
                 ▼
┌─────────────────────────────────────────────┐
│         SCI-two-ppt MCP Server (Python)      │
│                                             │
│  Tools:                                     │
│  ├─ parse_papers        → 论文解析          │
│  ├─ build_goal          → 构建目标文档      │
│  ├─ run_subagent        → 执行子Agent任务   │
│  ├─ generate_blueprint  → PPT蓝图生成       │
│  ├─ build_slide         → 单页PPT构建+预览  │
│  └─ generate_pptx       → 最终PPTX生成      │
│                                             │
│  Resources:                                 │
│  ├─ goal.md             → 目标文档          │
│  ├─ blueprint.yaml      → PPT蓝图           │
│  └─ agent_results/      → Agent产出         │
└─────────────────────────────────────────────┘
```

## 核心设计理念

- **Claude 是大脑**：多轮对话、需求分析、批判审查、创意决策都由 Claude 完成
- **MCP Server 是手脚**：PDF 解析、PPT 生成等确定性操作由 Python 工具完成
- **Skill 是剧本**：可选的 skill 文件指导 Claude 如何有序调用工具
- **渐进增强**：先在 Claude Code 内验证效果，后续可封装为独立应用

## 8 阶段工作流（Claude 编排视角）

### Phase 1: 输入与解析
- **Claude**：接收用户提供的论文 PDF 路径
- **Claude 调用**：`parse_papers(papers=["path/to/paper.pdf"])`
- **MCP Server**：解析 PDF → 提取结构（标题、摘要、方法、结果、图表）→ 保存图表
- **Claude**：分析结果质量，提示用户补充
- **产出**：workspace/input_analysis.md

### Phase 2: 需求对齐（纯 Claude 对话，不调用工具）
- **Claude**：与用户多轮对话，收集：
  - PPT 目的（组会/会议/答辩/汇报）
  - 时长限制、听众背景
  - 展示重点、核心创新点
  - 风格偏好
- **产出**：requirements.md（Claude 直接写入 workspace）

### Phase 3: 构建 goal.md
- **Claude 调用**：`build_goal(paper_analysis, requirements)`
- **MCP Server**：综合分析 + 需求 → 生成结构化 goal.md
- **Claude**：批判性审查 goal.md（检查完整性、合理性）
- **Claude**：与用户确认 goal.md，必要时修改
- **产出**：workspace/goal.md

### Phase 4: 子 Agent 并行执行
- **Claude 调用**：`run_subagent(agent_type, goal, context)`
  - agent_type: "content_extract" / "visual_resources" / "ui_design" / "speaker_notes"
  - 可并行调用多个 agent
- **MCP Server**：执行对应 Agent 任务，产出 markdown + 图片
- **产出**：workspace/agent_results/

### Phase 5: 审查与迭代
- **Claude**：批判性审查所有 Agent 产出
- **Claude**：与用户逐项确认
- **Claude**：不满意的部分重新调用 `run_subagent` → 最多 3 轮
- **产出**：workspace/review_report.md

### Phase 6: PPT 蓝图生成
- **Claude 调用**：`generate_blueprint(goal, agent_results)`
- **MCP Server**：整合所有资源 → 生成每页幻灯片详细定义
- **产出**：workspace/blueprint.yaml

### Phase 7: 逐页构建 & 确认
- **Claude 调用**：`build_slide(blueprint, slide_index)`
- **MCP Server**：生成单页 PPT + HTML 预览截图
- **Claude**：展示预览，用户确认/修改
- **Claude**：修改意见 → 重新调用 `build_slide`
- 循环直到所有页确认
- **产出**：workspace/preview/ + 确认版本

### Phase 8: 最终生成
- **Claude 调用**：`generate_pptx(confirmed_slides)`
- **MCP Server**：生成最终 .pptx 文件 + 制作报告
- **Claude**：整理文件结构
- **产出**：workspace/output.pptx + 制作报告.md

## MCP 工具设计

### Tool 1: `parse_papers`
```python
Input:  papers: list[str]  # PDF 文件路径列表
Output: {
    "papers": [
        {
            "title": str,
            "abstract": str,
            "methods": str,
            "results": str,
            "figures": [{"path": str, "caption": str}],
            "tables": [{"content": str, "caption": str}],
            "key_findings": list[str],
            "innovations": list[str]
        }
    ],
    "quality_report": str  # 缺失/不足项提示
}
```

### Tool 2: `build_goal`
```python
Input:  paper_analysis: dict,   # parse_papers 的输出
        requirements: str       # requirements.md 的文本内容
Output: {
    "goal_content": str,        # goal.md 全文
    "sections": list[str],      # PPT 章节列表
    "slide_count_estimate": int
}
```

### Tool 3: `run_subagent`
```python
Input:  agent_type: str,   # "content_extract" | "visual_resources" | "ui_design" | "speaker_notes"
        goal: str,         # goal.md 内容
        context: dict      # 依赖的前置 Agent 结果
Output: {
    "agent_type": str,
    "result_md": str,      # Agent 产出的 markdown
    "assets": list[str]    # 产出的图片资源路径
}
```

### Tool 4: `generate_blueprint`
```python
Input:  goal: str,              # goal.md
        agent_results: dict     # 所有 Agent 结果
Output: {
    "blueprint_yaml": str,      # 完整蓝图 YAML
    "slide_count": int
}
```

### Tool 5: `build_slide`
```python
Input:  blueprint: str,     # 蓝图 YAML
        slide_index: int,   # 第几页（从 0 开始）
        modifications: str  # 用户修改意见（可选）
Output: {
    "slide_index": int,
    "preview_html": str,    # HTML 预览文件路径
    "preview_image": str    # 截图路径（可选）
}
```

### Tool 6: `generate_pptx`
```python
Input:  blueprint: str,         # 蓝图 YAML
        slide_dir: str,         # 确认的幻灯片目录
        output_path: str        # 输出路径
Output: {
    "pptx_path": str,
    "report_md": str,           # 制作报告
    "slide_count": int
}
```

---

## 开发里程碑

### Milestone 1: MCP Server 骨架
**目标**：可运行的空壳 MCP Server + 配置系统
- [ ] MCP Server 入口（基于 `mcp` Python SDK）
- [ ] 配置加载器（YAML settings）
- [ ] 工作空间管理器（创建/清理 workspace 目录）
- [ ] 日志系统
- [ ] 6 个 tool 的空实现（返回 mock 数据）
- [ ] Claude Code settings.json 配置（注册 MCP Server）

### Milestone 2: parse_papers 工具
**目标**：输入论文 PDF 并提取结构化内容
- [ ] PDF 解析器（PyMuPDF）
- [ ] 论文结构识别（标题、摘要、方法、结果）
- [ ] 图表提取与保存
- [ ] 质量检查报告
- [ ] 端到端：用真实 PDF 测试

### Milestone 3: build_goal 工具
**目标**：从分析结果 + 需求构建 goal.md
- [ ] goal.md 模板系统
- [ ] 信息补全逻辑
- [ ] 结构化输出
- [ ] 端到端：从 parse_papers 输出构建 goal.md

### Milestone 4: run_subagent 工具
**目标**：子 Agent 执行系统
- [ ] Agent 抽象基类
- [ ] content_extract Agent（论文要点提取）
- [ ] visual_resources Agent（配图资源搜集）
- [ ] ui_design Agent（UI 风格确定）
- [ ] speaker_notes Agent（讲解备注）
- [ ] 并行执行调度器

### Milestone 5: PPT 生成系统
**目标**：蓝图 + 构建 + 预览 + 最终输出
- [ ] generate_blueprint（蓝图 YAML 生成）
- [ ] build_slide（python-pptx 单页构建）
- [ ] HTML 预览生成
- [ ] generate_pptx（最终 pptx 输出）
- [ ] 学术 PPT 模板（封面、内容页、图表页、总结页）

### Milestone 6: 集成测试 & Skill 文件
**目标**：端到端验证 + Skill 配置
- [ ] Skill 文件（指导 Claude 8 步工作流）
- [ ] 端到端测试（真实论文 → PPT）
- [ ] README 完善
- [ ] 错误处理与回退机制
- [ ] 性能优化（大 PDF、多论文场景）

### Milestone 7: 收尾 & 发布
**目标**：可分享使用的版本
- [ ] 安装文档（pip install + MCP 配置）
- [ ] 示例论文 + 示例 PPT 产出
- [ ] 问题排查指南
- [ ] 清理代码 & 类型注解
