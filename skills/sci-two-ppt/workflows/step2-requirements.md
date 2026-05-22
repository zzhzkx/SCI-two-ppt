# Step 2: 智能需求收集工作流

## 概述

Step 2 负责与用户交互，收集PPT制作需求，智能推荐PPT用途，生成结构化需求文档。

## 角色

**主要角色**：Content Strategist (内容策略师)

## 输入

- `workspace/papers/analysis.json` - 论文分析结果

## 输出

- `workspace/requirements.md` - 结构化需求文档

## 工作流程

### 2.1 读取论文分析
```python
analysis = read_json("workspace/papers/analysis.json")
research_field = analysis["research_field"]
innovations = analysis["innovations"]
```

### 2.2 智能推荐PPT用途
根据论文内容推荐：
```
根据论文分析，这是一篇关于[研究领域]的研究，推荐以下PPT用途：

1. 学术会议汇报 - 适合展示研究成果
2. 组会汇报 - 适合阶段性工作进展
3. 学位答辩 - 适合毕业论文展示
4. 项目汇报 - 适合项目进展展示

请选择或告诉我您的具体用途：
```

### 2.3 分层询问需求
**核心问题（必问）**：
- PPT用途
- 展示时长
- 听众背景

**细节问题（可选）**：
- 风格偏好
- 重点展示内容
- 特殊要求

### 2.4 生成需求文档
保存到 `workspace/requirements.md`

## 输出示例

```markdown
# PPT需求文档

## 基本信息
- 论文标题：[论文标题]
- 研究领域：[领域示例]

## PPT配置
- 用途：学术会议汇报
- 时长：10分钟
- 听众：课程老师、同学

## 风格偏好
- 整体风格：丰富图解风格
- 重点内容：工作原理、系统构成、误差分析、仿真结果

## 特殊要求
- 需要配图展示系统构成
- 公式需要清晰标注
- 误差分析用图表展示
```
