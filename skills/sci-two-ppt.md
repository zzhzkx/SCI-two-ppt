# sci-two-ppt Skill

将科研论文转换为专业学术PPT的工具。

## 工作流程

当用户要求将论文转换为PPT时，按以下10步流程执行：

### Step 1: 解析论文（LLM智能解析 + 检索式生成）

**流程**：
1. 调用 `parse_papers` 工具提取原始文本
   - 支持 PDF 和 Word 文档
   - 返回原始文本和基础元数据

2. spawn子Agent智能分析论文 + 生成检索式
   ```
   Agent: 论文智能分析
   description: "分析论文内容，提取结构化信息，生成专业检索式"
   prompt: |
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

     请将结果写入：{workspace}/papers/analysis.json
   ```

3. 保存结构化结果到 `workspace/papers/analysis.json`

**产出**：`workspace/papers/analysis.json`（包含论文分析 + 检索式）

**后续使用**：
- 当用户觉得文献支撑不足时，可使用生成的检索式进行文献补充
- 使用 `WebSearch` 工具检索相关文献
- 解析新文献，补充到 `workspace/papers/`

### Step 2: 收集需求
与用户对话，收集以下信息：
- PPT用途（组会/会议/答辩/汇报）
- 展示时长
- 听众背景
- 风格偏好
- 重点展示内容
- 保存到 `workspace/requirements.md`

### Step 3: 构建目标文档
- 综合论文解析结果和用户需求
- 构建详细的PPT目标文档 `workspace/goal.md`

### Step 4: 批判性审查
- 审查目标文档的完整性、合理性
- 与用户确认

### Step 5: 分派子 Agent（关键步骤）
**必须使用子 Agent 并行执行以下任务：**

使用 `Agent` 工具 spawn 以下子 Agent：

```
Agent 1: 论文要点提取
- description: "提取论文核心内容和关键发现"
- prompt: "阅读论文解析结果，提取核心内容、关键发现、创新点"
- 产出: workspace/agent_results/01_paper_keypoints.md

Agent 2: 核心创新点提炼
- description: "提炼研究创新点"
- prompt: "分析论文的创新性贡献，提炼核心创新点"
- 产出: workspace/agent_results/02_innovation_points.md

Agent 3: 仿真代码分析
- description: "分析仿真内容"
- prompt: "分析论文中的仿真方法和结果"
- 产出: workspace/agent_results/03_simulation_code.md

Agent 4: 学术配图搜集
- description: "搜集需要的图表资源"
- prompt: "确定PPT需要的图表和配图资源"
- 产出: workspace/agent_results/04_visual_resources.md

Agent 5: UI风格设计
- description: "设计PPT视觉风格"
- prompt: "根据学术规范设计PPT的配色、字体、排版风格"
- 产出: workspace/agent_results/05_ui_design.md

Agent 6: 章节结构安排
- description: "规划PPT章节结构"
- prompt: "设计PPT的章节结构和时间分配"
- 产出: workspace/agent_results/06_chapter_structure.md

Agent 7: 讲解备注
- description: "编写每页讲解备注"
- prompt: "为PPT每一页编写详细的讲解备注"
- 产出: workspace/agent_results/07_speaker_notes.md
```

**重要**：这些子 Agent 应该并行执行，每个子 Agent 独立完成任务并将结果写入对应的文件。

### Step 6: 审查与确认
- 读取所有子 Agent 产出
- 向用户展示结果摘要
- 用户确认或要求修改

### Step 7: 生成PPT蓝图
- 使用 `generate_blueprint` 工具生成详细的PPT蓝图
- 保存到 `workspace/ppt_blueprint.yaml`

### Step 8: 逐页制作PPT
- 对每一页幻灯片：
  1. 使用 `build_slide` 工具生成单页PPTX
  2. 展示给用户预览
  3. 用户确认或修改
  4. 循环直到所有页确认

### Step 9: 生成最终PPT
- 使用 `generate_pptx` 工具打包所有幻灯片
- 生成到 `workspace/output.pptx`

### Step 10: 整理文件
- 使用 `cleanup_workspace` 清理中间文件
- 保留重要文档和最终产出

## MCP 工具清单

| 工具名 | 用途 |
|--------|------|
| `parse_papers` | 解析论文（PDF/Word） |
| `extract_figures` | 提取图表 |
| `build_goal` | 构建目标文档 |
| `run_subagent` | 调度子Agent |
| `generate_blueprint` | 生成PPT蓝图 |
| `build_slide` | 生成单页幻灯片 |
| `generate_pptx` | 最终打包 |
| `read_pptx` | 读取PPTX状态 |
| `diff_pptx` | 对比PPTX差异 |
| `get_academic_style` | 学术规范 |
| `get_slide_template` | 页面模板 |
| `get_citation_format` | 引用格式 |

## 使用示例

用户: "帮我把这篇论文做成PPT：F:\papers\paper.pdf"

Claude 应该:
1. 调用 `parse_papers` 解析论文
2. 与用户对话收集需求
3. spawn 7个子 Agent 并行执行任务
4. 展示子 Agent 结果供用户确认
5. 逐页生成PPT
6. 最终打包输出

## 注意事项

1. **子 Agent 必须真正使用 Agent 工具 spawn**，不能模拟
2. **子 Agent 可以并行执行**，提高效率
3. **每个子 Agent 独立完成任务**，写入对应文件
4. **主 Agent 负责编排和审查**，不直接执行子任务
5. **用户交互贯穿全程**，每步都需要确认
