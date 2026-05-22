# Step 5: 子Agent并行执行工作流

## 概述

Step 5 负责并行执行多个子Agent，完成论文要点提取、创新点提炼、UI设计、章节结构、讲解备注等任务。

## 角色

多个子Agent并行执行：
- Paper Analyzer (论文分析专家)
- Content Strategist (内容策略师)
- Visual Designer (视觉设计师)
- Professor Reviewer (论文教授审查员)
- Material Collector (素材搜集员)

## 输入

- `workspace/papers/analysis.json` - 论文分析结果
- `workspace/goal.md` - PPT目标文档
- `workspace/requirements.md` - 用户需求

## 输出

- `workspace/agent_results/01_paper_keypoints.md` - 论文要点
- `workspace/agent_results/02_innovation_points.md` - 创新点
- `workspace/agent_results/03_simulation_code.md` - 仿真分析
- `workspace/agent_results/04_visual_resources.md` - 配图需求
- `workspace/agent_results/05_ui_design.md` - UI设计
- `workspace/agent_results/06_chapter_structure.md` - 章节结构
- `workspace/agent_results/07_speaker_notes.md` - 讲解备注

## 工作流程

### 5.1 并行spawn子Agent

```python
# 使用Agent工具并行spawn多个子Agent

# Agent 1: 论文要点提取
Agent(
    description="提取论文核心内容和关键发现",
    prompt="阅读论文解析结果，提取核心内容、关键发现、创新点",
    run_in_background=True
)

# Agent 2: 核心创新点提炼
Agent(
    description="提炼研究创新点",
    prompt="分析论文的创新性贡献，提炼核心创新点",
    run_in_background=True
)

# Agent 3: UI风格设计
Agent(
    description="设计PPT视觉风格",
    prompt="根据学术规范设计PPT的配色、字体、排版风格",
    run_in_background=True
)

# Agent 4: 章节结构安排
Agent(
    description="规划PPT章节结构",
    prompt="设计PPT的章节结构和时间分配",
    run_in_background=True
)

# Agent 5: 讲解备注
Agent(
    description="编写每页讲解备注",
    prompt="为PPT每一页编写详细的讲解备注",
    run_in_background=True
)

# Agent 6: 论文教授审查
Agent(
    description="专业学术审查",
    prompt="从教授角度审查研究内容的完整性和严谨性",
    run_in_background=True
)

# Agent 7: 素材搜集
Agent(
    description="搜集PPT制作素材",
    prompt="从学术期刊和网站搜集相关示意图和图表",
    run_in_background=True
)
```

### 5.2 等待所有Agent完成
- 所有Agent在后台并行运行
- 完成后会自动通知
- 读取所有产出文件

### 5.3 验证产出
- 检查所有文件是否生成
- 验证内容质量
- 记录完成状态

## 子Agent任务说明

### Agent 1: 论文要点提取
- 读取 analysis.json
- 提取核心内容
- 识别关键发现
- 产出：01_paper_keypoints.md

### Agent 2: 核心创新点提炼
- 分析创新性贡献
- 提炼核心创新点
- 与现有研究对比
- 产出：02_innovation_points.md

### Agent 3: UI风格设计
- 设计配色方案
- 规划页面布局
- 选择图表风格
- 产出：05_ui_design.md

### Agent 4: 章节结构安排
- 规划章节结构
- 分配时间节奏
- 设计内容逻辑
- 产出：06_chapter_structure.md

### Agent 5: 讲解备注
- 编写开场白
- 设计过渡语
- 准备重点强调
- 产出：07_speaker_notes.md

### Agent 6: 论文教授审查
- 学术严谨性审查
- 成果完整性评估
- 图表需求建议
- 产出：06_professor_review.md

### Agent 7: 素材搜集
- 搜索学术示意图
- 生成数据图表
- 创建流程图
- 产出：07_material_collection.md

## 后续处理

所有Agent完成后：
1. 读取所有产出
2. 向用户展示结果摘要
3. 用户确认或要求修改
4. 进入Step 6
