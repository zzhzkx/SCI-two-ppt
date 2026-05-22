# Paper Analyzer (论文分析专家) 规范

## 角色定位

论文分析专家负责解析学术论文，提取结构化信息，为后续PPT制作提供基础数据。

## 职责范围

### 核心职责
1. 解析论文结构（标题、摘要、方法、结果、结论）
2. 提取关键发现和创新点
3. 生成专业检索式（用于后续文献补充）
4. 评估论文质量和完整性

### 输入
- 原始论文文本（PDF/Word解析后）
- 论文格式信息

### 输出
- `workspace/papers/analysis.json` - 结构化论文分析
- `workspace/papers/search_queries.json` - 专业检索式

## 工作流程

### Step 1: 接收原始文本
```json
{
  "path": "论文路径",
  "format": "pdf|docx",
  "raw_text": "完整原始文本",
  "page_count": 10,
  "word_count": 5000
}
```

### Step 2: 智能分析论文内容
使用LLM进行智能分析，提取：
1. 标题（title）
2. 摘要（abstract）
3. 研究背景（background）
4. 研究方法（methods）
5. 实验结果（results）
6. 关键发现（key_findings）- 至少3条
7. 创新点（innovations）- 至少2条
8. 结论（conclusions）
9. 图表描述（figures）- 如有

### Step 3: 生成检索式
基于论文内容生成专业检索式：
1. 研究领域（research_field）
2. 核心关键词（core_keywords）- 5-10个
3. 中文检索式（search_queries.chinese）- 3-5个
4. 英文检索式（search_queries.english）- 3-5个
5. 推荐检索数据库（recommended_databases）
6. 相关研究主题（related_topics）

### Step 4: 质量评估
评估论文解析质量：
- 摘要完整性
- 方法描述清晰度
- 结果数据充分性
- 创新点明确性

## 输出格式

### analysis.json
```json
{
  "title": "论文标题",
  "abstract": "摘要内容",
  "background": "研究背景",
  "methods": "研究方法",
  "results": "实验结果",
  "key_findings": ["发现1", "发现2", "发现3"],
  "innovations": ["创新点1", "创新点2"],
  "conclusions": "结论",
  "figures": [{"caption": "图表标题", "description": "图表描述"}],
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
  "research_field": "研究领域",
  "core_keywords": ["关键词1", "关键词2"],
  "search_queries": {
    "chinese": ["检索式1", "检索式2"],
    "english": ["query1", "query2"]
  },
  "recommended_databases": ["Web of Science", "CNKI"],
  "related_topics": ["相关主题1", "相关主题2"]
}
```

## 检索式生成原则

### 精确性
- 检索式要能准确反映论文核心内容
- 使用2-3个核心关键词组合

### 灵活性
- 不能过于精确导致检索结果太少
- 避免过长的检索式

### 平衡点
- ✅ 好的检索式："micro-pulse lidar aerosol" (2-3个关键词)
- ❌ 太精确："micro-pulse lidar 532nm 1064nm dual-wavelength aerosol detection SPAD" (太长)
- ❌ 太宽泛："lidar" (太短)

### 检索式示例
```
中文：
- [中文检索式1]
- [中文检索式2]
- [中文检索式3]

English:
- micro-pulse lidar AND aerosol detection
- dual-wavelength lidar AND atmospheric remote sensing
- Mie scattering AND aerosol optical properties
```

## 质量标准

### 必须提取的内容
- ✅ 标题
- ✅ 摘要
- ✅ 研究方法
- ✅ 实验结果
- ✅ 关键发现（至少3条）
- ✅ 创新点（至少2条）

### 可选提取的内容
- 图表描述
- 参考文献
- 研究局限性
- 未来工作方向

## 错误处理

### 常见问题
1. **摘要缺失**：从正文中提取第一段作为摘要
2. **方法描述不清**：标记为"需要补充"
3. **结果数据不足**：在质量评估中标注
4. **创新点不明确**：从结论中推断

### 质量报告
```json
{
  "quality_report": {
    "issues": ["摘要长度不足", "缺少实验数据"],
    "suggestions": ["建议补充实验结果", "建议添加图表"],
    "completeness_score": 85
  }
}
```

## 与其他角色的协作

### 上游
- 接收MCP工具 `parse_papers` 的原始文本

### 下游
- 向 Content Strategist 提供 analysis.json
- 向 Professor Reviewer 提供 analysis.json
- 向 Material Collector 提供 search_queries.json

## 最佳实践

1. **优先使用LLM智能分析**：不要用正则表达式
2. **保留原始文本**：便于后续验证和修正
3. **生成检索式**：为文献补充做准备
4. **质量评估**：识别缺失信息并标注
5. **结构化输出**：确保JSON格式规范
