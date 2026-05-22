# SCI-two-ppt

AI-powered scientific paper to presentation PPT generator.

## 特性

- 智能论文解析：使用LLM分析论文结构
- 多角色协作：7个专业角色并行执行任务
- 设计规范系统：design_spec + spec_lock 双文件
- 学术规范库：支持多个学科领域
- 子Agent并行：使用Claude Code子Agent
- 交互式制作：逐页生成、用户确认

## 安装

```bash
git clone https://github.com/zzhzkx/SCI-two-ppt.git
cd SCI-two-ppt
pip install -r requirements.txt
```

## 使用方法

在 Claude Code 中说：
```
帮我把这篇论文做成PPT：F:\papers\paper.pdf
```

## 项目结构

```
SCI-two-ppt/
├── skills/sci-two-ppt/     # Skill文档
├── src/                     # 核心代码
├── examples/                # 示例项目
├── workspace/               # 用户工作区
└── docs/                    # 文档
```

## 角色系统

| 角色 | 职责 |
|------|------|
| Paper Analyzer | 论文分析 |
| Content Strategist | 内容策略 |
| Visual Designer | 视觉设计 |
| Slide Builder | 幻灯片构建 |
| Quality Reviewer | 质量审查 |
| Professor Reviewer | 专业审查 |
| Material Collector | 素材搜集 |

## 文档

- [技术设计文档](docs/technical-design.md)

## License

MIT
