# 光学论文示例：微脉冲激光雷达系统设计

## 项目概述

本示例展示如何使用 SCI-two-ppt 将一篇光学工程领域的学术论文转换为专业的学术PPT。

### 论文信息
- **标题**：微脉冲激光雷达系统设计
- **作者**：张寒逸
- **单位**：中国科学技术大学 物理学院
- **领域**：光学工程 / 激光雷达 / 大气遥感
- **课程**：激光大气遥感原理及其应用

### PPT配置
- **用途**：学术会议汇报
- **时长**：10分钟
- **听众**：课程老师、同学
- **风格**：丰富图解风格

## 工作流执行记录

### Step 1: 论文解析
- 输入：张寒逸-SC25038039-物理学院-微脉冲激光雷达系统设计.docx
- 产出：analysis.json, search_queries.json
- 子Agent：Paper Analyzer

### Step 2: 需求收集
- 与用户对话收集需求
- 产出：requirements.md

### Step 3: 目标构建
- spawn子Agent构建goal.md
- 产出：goal.md

### Step 4: 双角色审查
- 领域专家审查：04_expert_review.md
- PPT制作师审查：04_designer_review.md

### Step 5: 子Agent并行执行
- 7个子Agent并行执行
- 产出：agent_results/ 下7个文件

### Step 6-10: 制作输出
- 生成PPT蓝图
- 逐页制作
- 最终打包

## 产出文件

```
examples/optics_paper/
├── README.md                          # 本文件
├── design_spec.md                     # 设计规范
├── spec_lock.md                       # 执行锁
└── workspace/
    ├── papers/
    │   ├── analysis.json              # 论文分析
    │   ├── search_queries.json        # 检索式
    │   ├── requirements.md            # 需求文档
    │   ├── goal.md                    # 目标文档
    │   ├── blueprint.yaml             # PPT蓝图
    │   └── spec_lock.md               # 视觉规范
    ├── agent_results/
    │   ├── 01_paper_keypoints.md      # 论文要点
    │   ├── 02_innovation_points.md    # 创新点
    │   ├── 03_simulation_code.md      # 仿真分析
    │   ├── 04_visual_resources.md     # 配图需求
    │   ├── 05_ui_design.md            # UI设计
    │   ├── 06_chapter_structure.md    # 章节结构
    │   └── 07_speaker_notes.md        # 讲解备注
    └── output/
        └── output_final.pptx          # 最终PPT
```

## 学习要点

### 1. 论文解析
- 如何使用LLM智能分析论文
- 如何生成专业检索式
- 如何评估论文质量

### 2. 需求收集
- 如何智能推荐PPT用途
- 如何分层询问需求
- 如何生成结构化需求文档

### 3. 目标构建
- 如何综合论文分析和用户需求
- 如何规划章节结构
- 如何分配时间节奏

### 4. 双角色审查
- 领域专家审查学术严谨性
- PPT制作师审查展示效果
- 如何综合两方面建议

### 5. 子Agent执行
- 如何并行执行多个子Agent
- 如何管理子Agent产出
- 如何确保产出质量

### 6. 制作输出
- 如何生成PPT蓝图
- 如何逐页制作PPT
- 如何确保视觉一致性

## 复用指南

### 复用设计规范
```bash
# 复制设计规范模板
cp examples/optics_paper/design_spec.md workspace/papers/

# 根据新论文修改内容
# 修改：标题、作者、研究领域、创新点等
```

### 复用执行锁
```bash
# 复制视觉规范
cp examples/optics_paper/spec_lock.md workspace/papers/

# 根据新领域调整配色
# 修改：colors、fonts、layouts等
```

### 复用工作流
```bash
# 参考工作流文档
cat skills/sci-two-ppt/workflows/step1-paper-analysis.md

# 按照流程执行
# 每个步骤都有详细的说明
```

## 注意事项

1. **通用性**：本示例展示的是通用工作流，可应用于任何学术论文
2. **可定制性**：可根据具体需求调整设计规范和工作流
3. **可扩展性**：可添加更多示例项目到examples目录
4. **学习性**：本示例用于学习和理解SCI-two-ppt的工作原理

## 相关文档

- [SCI-two-ppt Skill](../../skills/sci-two-ppt/SKILL.md) - 主工作流入口
- [Paper Analyzer](../../skills/sci-two-ppt/references/paper-analyzer.md) - 论文分析专家规范
- [Content Strategist](../../skills/sci-two-ppt/references/content-strategist.md) - 内容策略师规范
- [Visual Designer](../../skills/sci-two-ppt/references/visual-designer.md) - 视觉设计师规范
