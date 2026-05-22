# sci-two-ppt: 科研论文转PPT工具

将科研论文转换为专业学术PPT的工具。使用 MCP Server 提供的工具，配合 Claude Code 子 Agent 完成整个流程。

## 工作流程（10步）

### Step 1: 输入论文
- 用户提供论文PDF路径
- 调用 `parse_papers` 工具解析论文
- 调用 `extract_figures` 工具提取图表
- 保存结果到 `workspace/papers/analysis.json`

### Step 2: 多轮询问需求
- 与用户对话，收集以下信息：
  - PPT目的（组会/会议/答辩/项目汇报）
  - 展示时长限制
  - 听众背景（专家/跨学科/评审）
  - 展示重点和核心创新点
  - 风格偏好（简约学术/丰富图解）
- 将需求保存到 `workspace/requirements.md`

### Step 3: 构建 goal.md
- 分析 Step 1+2 的信息，识别缺失部分
- 通过 WebSearch 补充缺失信息
- 调用 `build_goal` 工具构建目标文档
- 保存到 `workspace/goal.md`

### Step 4: 批判性审查
- 以批判视角审查 goal.md
- 检查完整性、合理性、可行性
- 与用户确认或修改

### Step 5: 分派子 Agent
- spawn 多个 Claude Code 子 Agent 执行任务：
  - **Agent 1**: 论文要点提取 - 深度分析论文核心内容
  - **Agent 2**: 核心创新点提炼 - 提炼创新点+研究定位
  - **Agent 3**: 仿真代码优化 - 分析仿真代码
  - **Agent 4**: 学术配图搜集 - 搜集/优化论文配图
  - **Agent 5**: 美术图片/icon - 搜集美术素材
  - **Agent 6**: UI风格设计 - 确定配色、字体、排版
  - **Agent 7**: 章节结构安排 - 规划PPT章节和节奏
  - **Agent 8**: 讲解备注 - 为每页写讲解备注
- 每个 Agent 结果保存到 `workspace/agent_results/`

### Step 6: 批判审查 + 用户确认
- 读取所有 Agent 产出
- 批判性审查一致性、完整性、质量
- 与用户逐项确认
- 不满意的部分重新执行对应 Agent

### Step 7: 撰写 PPT 制作报告
- 整合所有确认后的 Agent 产出
- 调用 `generate_blueprint` 工具生成蓝图
- 保存到 `workspace/ppt_blueprint.yaml`

### Step 8: 逐页制作 + PPT 预览
- 对每一页幻灯片：
  1. 调用 `build_slide` 工具生成单页PPTX
  2. 用户用 PowerPoint 打开查看
  3. 用户手动修改后，调用 `diff_pptx` 检测变化
  4. 根据反馈调整，重新 build 或继续下一页
- 循环直到所有页确认

### Step 9: 生成正式 PPTX
- 调用 `generate_pptx` 工具打包所有幻灯片
- 生成到 `workspace/output.pptx`

### Step 10: 整理文件
- 调用 `cleanup_workspace` 清理中间文件
- 保留重要文档和资源

## MCP 工具清单

| 工具名 | 用途 |
|--------|------|
| `parse_papers` | 解析论文PDF |
| `extract_figures` | 提取图表 |
| `read_pptx` | 读取PPTX状态 |
| `diff_pptx` | 对比PPTX差异 |
| `build_slide` | 生成单页幻灯片 |
| `render_preview` | 渲染预览图 |
| `generate_pptx` | 最终打包 |
| `cleanup_workspace` | 清理文件 |
| `build_goal` | 构建目标文档 |
| `run_subagent` | 调度子Agent |
| `generate_blueprint` | 蓝图生成 |
| `get_academic_style` | 学术规范 |
| `get_slide_template` | 页面模板 |
| `get_citation_format` | 引用格式 |

## 使用示例

```
用户: 帮我把这篇论文做成PPT
Claude: 好的，请提供论文PDF路径。
用户: F:\papers\optics_paper.pdf
Claude: [调用 parse_papers 解析论文]
        [调用 extract_figures 提取图表]
        论文解析完成。接下来我需要了解您的PPT需求...
        [多轮对话收集需求]
        [构建 goal.md]
        [分派子Agent]
        [逐页制作PPT]
        PPT已生成：workspace/output.pptx
```
