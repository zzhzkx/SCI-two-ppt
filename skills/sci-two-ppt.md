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

     【检索式生成原则】
     - 精确性：检索式要能准确反映论文核心内容
     - 灵活性：不能过于精确导致检索结果太少
     - 平衡点：使用2-3个核心关键词组合，避免过长的检索式
     - 示例：
       ✅ 好的检索式："micro-pulse lidar aerosol" (2-3个关键词)
       ❌ 太精确："micro-pulse lidar 532nm 1064nm dual-wavelength aerosol detection SPAD" (太长)
       ❌ 太宽泛："lidar" (太短)
     - 建议：每个检索式包含2-3个核心概念，用AND连接

     请将结果写入：{workspace}/papers/analysis.json
   ```

3. 保存结构化结果到 `workspace/papers/analysis.json`

**产出**：`workspace/papers/analysis.json`（包含论文分析 + 检索式）

**后续使用**：
- 当用户觉得文献支撑不足时，可使用生成的检索式进行文献补充
- 使用 `WebSearch` 工具检索相关文献
- 解析新文献，补充到 `workspace/papers/`

### Step 2: 智能需求收集

**流程**：
1. **读取论文分析结果**
   - 读取 `workspace/papers/analysis.json`
   - 了解论文的研究领域、核心内容、创新点

2. **智能推荐PPT用途**
   根据论文内容，推荐最可能的PPT用途：
   ```
   根据论文分析，这是一篇关于[研究领域]的研究，我推荐以下PPT用途：

   1. 学术会议汇报 - 适合展示研究成果
   2. 组会汇报 - 适合阶段性工作进展
   3. 学位答辩 - 适合毕业论文展示
   4. 项目汇报 - 适合项目进展展示

   请选择或告诉我您的具体用途：
   ```

3. **分层询问需求**
   **核心问题（必问）**：
   - PPT用途（从推荐中选择或自定义）
   - 展示时长（推荐根据论文复杂度）
   - 听众背景（专家/跨学科/评审）

   **细节问题（可选）**：
   - 风格偏好（简约学术/丰富图解）
   - 重点展示内容（根据论文创新点推荐）
   - 特殊要求（动画、配图、公式等）

4. **生成需求文档**
   保存到 `workspace/requirements.md`，格式：
   ```markdown
   # PPT需求文档

   ## 基本信息
   - 论文标题：[从analysis.json读取]
   - 研究领域：[从analysis.json读取]

   ## PPT配置
   - 用途：[用户选择]
   - 时长：[用户指定]
   - 听众：[用户指定]

   ## 风格偏好
   - 整体风格：[用户选择]
   - 重点内容：[根据创新点推荐]

   ## 特殊要求
   - [用户补充]
   ```

**产出**：`workspace/requirements.md`（结构化需求文档）

### Step 3: 智能构建目标文档

**流程**：
1. **spawn子Agent构建goal.md**
   ```
   Agent: 目标文档构建
   description: "综合论文分析和用户需求，构建PPT目标文档"
   prompt: |
     你是一个学术PPT规划专家。请根据以下信息，构建详细的PPT目标文档。

     【论文分析结果】
     {analysis_json}

     【用户需求】
     {requirements_md}

     请构建PPT目标文档，包含：

     1. **PPT概述**
        - 标题、作者、单位
        - 用途、时长、听众

     2. **内容结构**
        - 章节划分（根据论文结构和用户需求）
        - 每章重点内容
        - 时间分配建议

     3. **核心要点**
        - 必须展示的创新点
        - 关键数据和结论
        - 重要图表和公式

     4. **视觉设计**
        - 推荐配色方案
        - 页面布局建议
        - 图表风格

     5. **讲解策略**
        - 开场白建议
        - 重点强调内容
        - 过渡语设计

     6. **信息补全**
        - 识别缺失的信息
        - 建议补充的内容
        - 需要搜集的资源

     输出格式：
     # PPT目标文档

     ## 1. PPT概述
     [内容]

     ## 2. 内容结构
     [章节列表和时间分配]

     ## 3. 核心要点
     [必须展示的内容]

     ## 4. 视觉设计
     [设计建议]

     ## 5. 讲解策略
     [讲解建议]

     ## 6. 信息补全
     [缺失信息和补充建议]

     请将结果写入：{workspace}/goal.md
   ```

2. **保存目标文档**
   - 保存到 `workspace/goal.md`

**产出**：`workspace/goal.md`（详细的PPT目标文档）

**特点**：
- 综合论文分析和用户需求
- 自动识别信息缺失
- 提供补全建议
- 结构化、可执行

### Step 4: 双角色批判性审查

**流程**：
spawn两个子Agent，分别从不同角度审查目标文档：

```
Agent 1: 领域专家审查
description: "以专业学者视角审查研究内容"
prompt: |
  你是一位[研究领域]的资深教授/院士，拥有丰富的学术研究经验。

  请从专业学者角度审查以下PPT目标文档：

  【目标文档】
  {goal_md}

  【论文分析】
  {analysis_json}

  请重点审查：

  1. **学术严谨性**
     - 研究方法是否科学合理
     - 实验数据是否充分可靠
     - 结论是否有足够支撑

  2. **内容完整性**
     - 是否遗漏重要研究内容
     - 关键图表是否齐全
     - 公式推导是否完整

  3. **创新点呈现**
     - 创新点是否突出展示
     - 与现有研究对比是否清晰
     - 技术优势是否明确

  4. **学术规范**
     - 引用是否规范
     - 术语是否准确
     - 格式是否符合学术要求

  5. **改进建议**
     - 需要补充哪些内容
     - 哪些部分需要加强
     - 是否需要更多实验数据支撑

  输出格式：
  # 领域专家审查报告

  ## 总体评价
  [整体评价]

  ## 学术严谨性
  [审查结果和建议]

  ## 内容完整性
  [审查结果和建议]

  ## 创新点呈现
  [审查结果和建议]

  ## 学术规范
  [审查结果和建议]

  ## 必须补充内容
  [列表]

  ## 改进建议
  [具体建议]

  请将结果写入：{workspace}/agent_results/04_expert_review.md


Agent 2: PPT制作师审查
description: "以专业PPT设计师视角审查展示效果"
prompt: |
  你是一位资深PPT设计师，制作过数百场学术会议、学位答辩的PPT，深谙演示设计之道。

  请从PPT设计和展示效果角度审查以下目标文档：

  【目标文档】
  {goal_md}

  【用户需求】
  {requirements_md}

  请重点审查：

  1. **视觉设计**
     - 配色方案是否专业协调
     - 字体排版是否清晰易读
     - 页面布局是否合理美观

  2. **内容呈现**
     - 信息密度是否适中
     - 重点是否突出明确
     - 逻辑是否清晰流畅

  3. **听众体验**
     - 是否符合听众背景
     - 时长分配是否合理
     - 是否有冗余内容

  4. **演示效果**
     - 开场是否吸引人
     - 过渡是否自然
     - 结尾是否有力

  5. **技术实现**
     - 动画是否恰当
     - 图表是否清晰
     - 公式是否易读

  6. **改进建议**
     - 哪些页面需要优化
     - 如何提升视觉效果
     - 如何增强演示感染力

  输出格式：
  # PPT制作师审查报告

  ## 总体评价
  [整体评价]

  ## 视觉设计
  [审查结果和建议]

  ## 内容呈现
  [审查结果和建议]

  ## 听众体验
  [审查结果和建议]

  ## 演示效果
  [审查结果和建议]

  ## 技术实现
  [审查结果和建议]

  ## 必须优化页面
  [列表]

  ## 改进建议
  [具体建议]

  请将结果写入：{workspace}/agent_results/04_designer_review.md
```

**审查维度对比**：

| 维度 | 领域专家 | PPT制作师 |
|------|----------|----------|
| 关注点 | 学术内容 | 展示效果 |
| 视角 | 专业严谨 | 用户体验 |
| 重点 | 数据支撑 | 视觉呈现 |
| 目标 | 学术正确 | 表达清晰 |

**后续处理**：
1. 读取两份审查报告
2. 综合两位角色的建议
3. 与用户讨论需要改进的部分
4. 根据反馈调整目标文档或重新执行相关Agent

**产出**：
- `workspace/agent_results/04_expert_review.md`（领域专家审查）
- `workspace/agent_results/04_designer_review.md`（PPT制作师审查）

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
| `parse_papers` | 提取论文原始文本（PDF/Word） |
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

用户: "帮我把这篇论文做成PPT：F:\\papers\\paper.pdf"

Claude 应该:
1. 调用 `parse_papers` 提取原始文本
2. spawn子Agent智能分析论文 + 生成检索式
3. 智能推荐PPT用途，分层询问需求
4. spawn子Agent构建目标文档
5. spawn双角色审查（领域专家 + PPT制作师）
6. 综合审查建议，与用户确认
7. spawn 7个子 Agent 并行执行任务
8. 展示子 Agent 结果供用户确认
9. 逐页生成PPT
10. 最终打包输出

## 文献补充功能

当用户觉得文献支撑不足时：

1. Claude 读取 `analysis.json` 中的 `search_queries`
2. 使用 `WebSearch` 工具检索相关文献
3. 解析新文献，补充到 `workspace/papers/`
4. 更新Agent产出

## 注意事项

1. **论文解析使用子Agent**：不要用正则表达式，用LLM智能分析
2. **需求收集智能化**：根据论文内容推荐PPT用途
3. **目标文档结构化**：使用子Agent构建详细的goal.md
4. **双角色审查**：领域专家 + PPT制作师，全面审查
5. **子 Agent 必须真正使用 Agent 工具 spawn**，不能模拟
6. **子 Agent 可以并行执行**，提高效率
7. **每个子 Agent 独立完成任务**，写入对应文件
8. **主 Agent 负责编排和审查**，不直接执行子任务
9. **用户交互贯穿全程**，每步都需要确认
10. **检索式自动生成**：Step 1 时自动生成专业检索式，便于后续文献补充
11. **检索式平衡原则**：精确但不过于精确，使用2-3个核心关键词
