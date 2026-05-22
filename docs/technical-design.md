# SCI-two-ppt 技术设计文档

## 架构概述

SCI-two-ppt 是基于 MCP Server 的学术论文转PPT工具。

### 核心设计理念

1. Claude 是大脑：多轮对话、需求分析、批判审查
2. MCP Server 是手脚：PDF解析、PPT生成
3. 子 Agent 自由协作：通过共享 workspace 传递结果

### 角色系统

7个核心角色：
1. Paper Analyzer - 论文分析专家
2. Content Strategist - 内容策略师
3. Visual Designer - 视觉设计师
4. Slide Builder - 幻灯片构建师
5. Quality Reviewer - 质量审查员
6. Professor Reviewer - 论文教授审查员
7. Material Collector - 素材搜集员

### 设计规范系统

- design_spec.md：人类可读的设计叙事
- spec_lock.md：机器可读的执行锁

### 工作流程

10步工作流：
1. 论文解析
2. 需求收集
3. 目标构建
4. 双角色审查
5. 子Agent执行
6. 审查确认
7. 蓝图生成
8. 逐页制作
9. 最终打包
10. 整理文件

详见完整文档。