# SCI-two-ppt 示例项目库

## 概述

本目录包含 SCI-two-ppt 的示例项目，展示完整的论文转PPT工作流程。

## 示例项目

### 1. optics_paper - 光学论文示例
- **论文**：微脉冲激光雷达系统设计
- **作者**：张寒逸
- **领域**：光学工程/激光雷达
- **用途**：学术会议汇报
- **时长**：10分钟

**示例内容**：
- 完整的工作流执行记录
- 所有Agent产出文件
- 设计规范文档
- 最终PPT输出

### 2. physics_paper - 物理论文示例（待添加）

### 3. computer_science_paper - 计算机论文示例（待添加）

## 使用方法

### 查看示例
```bash
# 进入示例目录
cd examples/optics_paper

# 查�示例说明
cat README.md

# 查看设计规范
cat design_spec.md

# 查看最终PPT
ls output/
```

### 学习工作流
1. 阅读 `README.md` 了解项目背景
2. 查看 `design_spec.md` 学习设计规范
3. 查看 `agent_results/` 了解各Agent产出
4. 查看 `output/` 看最终效果

### 复用模板
- 复制 `design_spec.md` 作为模板
- 参考 `spec_lock.md` 设置视觉规范
- 使用 `blueprint.yaml` 作为蓝图参考

## 示例结构

```
examples/
├── README.md                    # 本文件
├── optics_paper/                # 光学论文示例
│   ├── README.md               # 示例说明
│   ├── design_spec.md          # 设计规范
│   ├── spec_lock.md            # 执行锁
│   └── workspace/              # 完整工作空间
│       ├── papers/
│       ├── agent_results/
│       └── output/
├── physics_paper/               # 物理论文示例
└── computer_science_paper/      # 计算机论文示例
```

## 贡献指南

欢迎添加新的示例项目：
1. 创建新的示例目录
2. 添加 README.md 说明
3. 添加完整的执行记录
4. 提交 Pull Request
