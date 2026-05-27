# Step 4: 双角色批判性审查工作流

## 概述

Step 4 负责使用两个专业角色从不同角度审查目标文档，确保学术严谨性和展示效果。

## 角色

- **Professor Reviewer** (论文教授审查员) - 学术审查
- **Quality Reviewer** (质量审查员) - 视觉审查

## 输入

- `workspace/goal.md` - PPT目标文档
- `workspace/papers/analysis.json` - 论文分析结果
- `workspace/requirements.md` - 用户需求

## 输出

- `workspace/agent_results/04_expert_review.md` - 领域专家审查报告（Professor Reviewer）
- `workspace/agent_results/04_designer_review.md` - PPT制作师审查报告（Quality Reviewer）

文件命名规则：`Step编号_角色简写.md`

## 工作流程

### 4.1 spawn领域专家审查
```
Agent 1: 领域专家审查
description: "以专业学者视角审查研究内容"
prompt: |
  你是一位[研究领域]的资深教授/院士。

  请从专业学者角度审查以下PPT目标文档：

  【目标文档】
  {goal_md}

  【论文分析】
  {analysis_json}

  请重点审查：
  1. 学术严谨性（研究方法、实验数据、结论支撑）
  2. 内容完整性（是否遗漏重要内容）
  3. 创新点呈现（是否突出展示）
  4. 学术规范（引用、术语、格式）

  请将结果写入：workspace/agent_results/04_expert_review.md
```

### 4.2 spawn PPT制作师审查
```
Agent 2: PPT制作师审查
description: "以专业PPT设计师视角审查展示效果"
prompt: |
  你是一位资深PPT设计师。

  请从PPT设计和展示效果角度审查以下目标文档：

  【目标文档】
  {goal_md}

  【用户需求】
  {requirements_md}

  请重点审查：
  1. 视觉设计（配色、字体、布局）
  2. 内容呈现（信息密度、重点突出）
  3. 听众体验（是否符合听众背景）
  4. 演示效果（开场、过渡、结尾）

  请将结果写入：workspace/agent_results/04_designer_review.md
```

### 4.3 综合审查结果
- 读取两份审查报告
- 综合两位角色的建议
- 与用户讨论需要改进的部分

## 审查维度对比

| 维度 | 领域专家 | PPT制作师 |
|------|----------|-----------|
| 关注点 | 学术内容 | 展示效果 |
| 视角 | 专业严谨 | 用户体验 |
| 重点 | 数据支撑 | 视觉呈现 |
| 目标 | 学术正确 | 表达清晰 |

## 后续处理

根据审查结果：
1. 如果需要补充内容 → 返回Step 5重新执行相关Agent
2. 如果需要调整设计 → 返回Step 3重新构建目标文档
3. 如果审查通过 → 生成 `workspace/design_spec.md`（设计决策文档），然后进入Step 5

**design_spec.md 的角色**：综合两位审查员的意见，确定最终配色、字体、布局等设计决策。Visual Designer 在 Step 5 读取 design_spec.md，生成机器可读的 `workspace/papers/spec_lock.md`。
