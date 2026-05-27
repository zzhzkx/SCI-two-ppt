# Step 5: 子Agent并行执行

## 概述

Step 5 是PPT制作的核心步骤，负责并行执行多个子Agent完成内容准备和SVG代码生成。

## 角色

本步骤涉及多个角色并行执行：
- **Paper Analyzer** - 论文要点提取
- **Content Strategist** - 创新点提炼、章节结构
- **Visual Designer** - UI风格设计
- **SVG Generator** - SVG代码生成
- **Material Collector** - 素材搜集

## 输入

- `workspace/papers/analysis.json` - 论文分析结果
- `workspace/goal.md` - PPT目标文档
- `workspace/requirements.md` - 用户需求
- `workspace/papers/spec_lock.md` - 视觉规范

## 输出

- `workspace/agent_results/` - Agent产出
- `workspace/preview/*.svg` - SVG文件

## 7个子Agent任务

### Agent 1: 论文要点提取
**角色**: Paper Analyzer
**任务**:
- 读取 `analysis.json`
- 深度分析论文核心内容
- 提取关键发现和创新点
- 识别研究方法和实验结果

**输出**: `workspace/agent_results/01_paper_keypoints.md`

### Agent 2: 核心创新点提炼
**角色**: Content Strategist
**任务**:
- 读取 Agent 1 的产出
- 提炼核心创新点
- 与现有研究对比
- 识别技术优势

**输出**: `workspace/agent_results/02_innovation_points.md`

### Agent 3: 仿真代码分析
**角色**: Paper Analyzer
**任务**:
- 分析论文中的仿真方法
- 识别MATLAB/Python代码
- 提取关键参数和结果

**输出**: `workspace/agent_results/03_simulation_code.md`

### Agent 4: 学术配图搜集
**角色**: Material Collector
**任务**:
- 从论文中提取图表
- 搜索相关研究的示意图
- 搜集学术配图资源

**输出**: `workspace/agent_results/04_visual_resources.md`

### Agent 5: UI风格设计
**角色**: Visual Designer
**任务**:
- 设计配色方案
- 规划页面布局
- 选择图表风格
- 生成SVG代码模板

**输出**: `workspace/agent_results/05_ui_design.md`

### Agent 6: 章节结构安排
**角色**: Content Strategist
**任务**:
- 规划PPT章节结构
- 分配时间节奏
- 设计内容逻辑

**输出**: `workspace/agent_results/06_chapter_structure.md`

### Agent 7: 讲解备注
**角色**: Content Strategist
**任务**:
- 编写开场白
- 设计过渡语
- 准备重点强调

**输出**: `workspace/agent_results/07_speaker_notes.md`

## Agent协作模式

### 并行执行
- Agent 1-4 可以并行执行（独立任务）
- Agent 5 依赖 Agent 1 的产出（需要了解论文内容）
- Agent 6 依赖 Agent 1, 2 的产出
- Agent 7 依赖 Agent 6 的产出

### 信息传递
```
Agent 1 → paper_keypoints.md
    ↓
Agent 2 → innovation_points.md
    ↓
Agent 5 → ui_design.md
Agent 6 → chapter_structure.md
    ↓
Agent 7 → speaker_notes.md
```

## 与用户交互

### 审查流程
1. 展示所有Agent产出摘要
2. 用户确认或提出修改
3. 不满意的部分重新执行对应Agent
4. 最多3轮迭代

### 用户确认要点
- 核心创新点是否准确
- 章节结构是否合理
- 时间分配是否合适

## 后续步骤

所有Agent完成后：
1. 读取所有产出
2. 向用户展示结果摘要
3. 用户确认或修改
4. 进入Step 6（审查确认）

**注意**：SVG代码生成属于 Step 8（逐页制作PPT），不在本步骤执行。
