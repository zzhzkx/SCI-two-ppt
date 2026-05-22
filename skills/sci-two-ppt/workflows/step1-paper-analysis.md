# Step 1: 论文解析工作流

## 概述

Step 1 是整个工作流的起点，负责解析用户提供的论文，提取结构化信息，为后续PPT制作提供基础数据。

## 角色

**主要角色**：Paper Analyzer (论文分析专家)

## 输入

- 用户提供的论文文件（PDF/Word）
- 文件路径

## 输出

- `workspace/papers/analysis.json` - 结构化论文分析
- `workspace/papers/search_queries.json` - 专业检索式
- `workspace/papers/quality_report.md` - 质量评估报告

## 工作流程

### 1.1 接收论文文件

```python
# 用户提供论文路径
paper_path = "F:\papers\optics_paper.pdf"

# 调用MCP工具提取原始文本
result = parse_papers([paper_path])

# 返回结果
{
  "papers": [
    {
      "path": "F:\papers\optics_paper.pdf",
      "format": "pdf",
      "raw_text": "完整原始文本...",
      "page_count": 10,
      "word_count": 5000,
      "char_count": 25000
    }
  ],
  "errors": [],
  "total": 1,
  "failed": 0
}
```

### 1.2 spawn子Agent智能分析

```python
# spawn论文分析专家子Agent
Agent(
    description="论文智能分析",
    prompt="""
    你是一个学术论文分析专家。请分析以下论文内容，提取结构化信息，并生成该领域的专业检索式。

    论文原始文本：
    {raw_text}

    请完成以下任务：

    【任务1：论文内容分析】
    1. 标题（title）
    2. 摘要（abstract）
    3. 研究背景（background）
    4. 研究方法（methods）
    5. 实验结果（results）
    6. 关键发现（key_findings）- 至少3条
    7. 创新点（innovations）- 至少2条
    8. 结论（conclusions）
    9. 图表描述（figures）- 如有

    【任务2：检索式生成】
    10. 研究领域（research_field）
    11. 核心关键词（core_keywords）- 5-10个
    12. 中文检索式（search_queries.chinese）- 3-5个
    13. 英文检索式（search_queries.english）- 3-5个
    14. 推荐检索数据库（recommended_databases）
    15. 相关研究主题（related_topics）

    输出JSON格式：
    {
      "title": "...",
      "abstract": "...",
      "background": "...",
      "methods": "...",
      "results": "...",
      "key_findings": ["发现1", "发现2", ...],
      "innovations": ["创新点1", "创新点2", ...],
      "conclusions": "...",
      "figures": [{"caption": "...", "description": "..."}],

      "research_field": "根据论文内容智能识别的研究领域",
      "core_keywords": ["从论文中提取的核心关键词"],
      "search_queries": {
        "chinese": ["基于论文内容生成的中文检索式"],
        "english": ["Based on paper content generated English queries"]
      },
      "recommended_databases": ["根据研究领域推荐的数据库"],
      "related_topics": ["与论文相关的研究主题"]
    }

    注意：
    - research_field：根据论文实际内容识别，不要预设
    - core_keywords：从论文中提取核心术语，5-10个
    - search_queries：基于论文内容生成专业检索式，中英文各3-5个
    - recommended_databases：根据研究领域推荐适合的数据库
    - related_topics：与论文研究方向相关的主题

    【检索式生成原则】
    - 精确性：检索式要能准确反映论文核心内容
    - 灵活性：不能过于精确导致检索结果太少
    - 平衡点：使用2-3个核心关键词组合，避免过长的检索式
    - 示例：
      ✅ 好的检索式："micro-pulse lidar aerosol" (2-3个关键词)
      ❌ 太精确："micro-pulse lidar 532nm 1064nm dual-wavelength aerosol detection SPAD" (太长)
      ❌ 太宽泛："lidar" (太短)
    - 建议：每个检索式包含2-3个核心概念，用AND连接

    请将结果写入：workspace/papers/analysis.json
    """,
    run_in_background=True
)
```

### 1.3 保存结构化结果

```python
# 保存analysis.json
save_json("workspace/papers/analysis.json", analysis_result)

# 保存search_queries.json
save_json("workspace/papers/search_queries.json", search_queries)

# 生成质量评估报告
quality_report = generate_quality_report(analysis_result)
save_file("workspace/papers/quality_report.md", quality_report)
```

### 1.4 质量评估

```python
def generate_quality_report(analysis):
    report = """
    # 论文解析质量报告

    ## 解析结果
    - 标题：{title}
    - 摘要长度：{abstract_length} 字符
    - 方法长度：{methods_length} 字符
    - 结果长度：{results_length} 字符
    - 关键发现：{key_findings_count} 条
    - 创新点：{innovations_count} 条

    ## 质量评估
    - 完整性：{completeness}
    - 清晰度：{clarity}
    - 数据充分性：{data_sufficiency}

    ## 建议
    {suggestions}
    """.format(**analysis)
    
    return report
```

## 输出文件说明

### analysis.json
```json
{
  "title": "微脉冲激光雷达系统设计",
  "abstract": "为实现大气气溶胶光学特性的高精度...",
  "background": "随着全球气候变迁...",
  "methods": "基于米氏散射理论...",
  "results": "白天探测距离3.5~4.2km...",
  "key_findings": [
    "双波长协同设计有效提升白天探测鲁棒性",
    "消光系数与滤光片带宽是主导误差源",
    "1064nm通道鲁棒性优于532nm通道"
  ],
  "innovations": [
    "双波长同轴收发架构设计",
    "多误差源耦合影响首次系统量化"
  ],
  "conclusions": "系统满足大气监测与云物理研究需求",
  "figures": [
    {
      "caption": "图3.1 微脉冲激光雷达系统设计",
      "description": "系统架构图"
    }
  ],
  "quality_assessment": {
    "completeness": "良好",
    "clarity": "清晰",
    "data_sufficiency": "充分"
  }
}
```

### search_queries.json
```json
{
  "research_field": "光学工程/激光雷达/大气遥感",
  "core_keywords": [
    "微脉冲激光雷达",
    "气溶胶",
    "米氏散射",
    "双波长",
    "偏振探测"
  ],
  "search_queries": {
    "chinese": [
      "微脉冲激光雷达 AND 气溶胶探测",
      "双波长激光雷达 AND 大气遥感",
      "Mie散射 AND 气溶胶光学特性"
    ],
    "english": [
      "micro-pulse lidar AND aerosol detection",
      "dual-wavelength lidar AND atmospheric remote sensing",
      "Mie scattering AND aerosol optical properties"
    ]
  },
  "recommended_databases": [
    "Web of Science",
    "CNKI (中国知网)",
    "IEEE Xplore",
    "Google Scholar"
  ],
  "related_topics": [
    "激光雷达系统设计",
    "大气气溶胶探测",
    "偏振探测技术"
  ]
}
```

## 后续使用

### 文献补充功能
当用户觉得文献支撑不足时：
1. 读取 `search_queries.json`
2. 使用 `WebSearch` 工具检索相关文献
3. 解析新文献，补充到 `workspace/papers/`
4. 更新Agent产出

### 与其他步骤的衔接
- **Step 2**：读取 analysis.json 了解论文内容
- **Step 3**：读取 analysis.json 构建目标文档
- **Step 5**：子Agent读取 analysis.json 执行任务

## 注意事项

1. **优先使用LLM智能分析**：不要用正则表达式
2. **保留原始文本**：便于后续验证和修正
3. **生成检索式**：为文献补充做准备
4. **质量评估**：识别缺失信息并标注
5. **结构化输出**：确保JSON格式规范

## 错误处理

### 常见问题
1. **文件不存在**：提示用户检查路径
2. **格式不支持**：提示用户转换格式
3. **解析失败**：记录错误并提示用户
4. **内容缺失**：在质量报告中标注

### 错误报告
```json
{
  "errors": [
    "文件不存在：F:\papers\nonexistent.pdf",
    "不支持的格式：.doc"
  ],
  "total": 2,
  "failed": 2
}
```
