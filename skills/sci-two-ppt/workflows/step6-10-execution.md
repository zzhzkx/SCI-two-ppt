# Step 6-10: SVG后处理、转换和最终输出

## Step 6: SVG后处理 + 质量检查

### 6.1 SVG后处理
调用 `finalize_svg` 进行后处理：
- **嵌入图标**: 将 `<use data-icon="..."/>` 替换为实际SVG路径
- **对齐图像**: 处理 `<image>` 元素的 preserveAspectRatio
- **展平文本**: 将 `<tspan>` 转换为独立 `<text>` 元素
- **圆角转路径**: 将 `<rect rx="...">` 转换为 `<path>`

### 6.2 质量检查
调用 `check_svg_quality` 检查：
- **XML良构性**: 确保SVG是有效的XML
- **viewBox检查**: 验证格式为 `0 0 1280 720`
- **禁止元素检查**: 无 `<style>`、`<script>`、`<foreignObject>` 等
- **字体安全检查**: 使用PPT预装字体
- **spec_lock偏差**: 颜色、字体符合规范

### 6.3 检查结果处理
```
如果检查通过 → 进入Step 7
如果检查失败 → 返回Step 5修正SVG
```

---

## Step 7: SVG转PPTX

### 7.1 批量转换
```python
# 对每个SVG文件调用转换
for svg_file in svg_files:
    result = svg_to_pptx(svg_file, output_pptx)
    if not result["success"]:
        # 处理转换错误
        fix_svg_and_retry(svg_file)
```

### 7.2 转换流程
```
SVG文件 → finalize_svg后处理 → drawingml_elements转换 → PPTX文件
```

### 7.3 输出
- `workspace/output/slide_*.pptx` - 单页PPTX文件

---

## Step 8: 逐页预览确认

### 8.1 生成HTML预览
```python
# 从PPTX生成HTML预览（保持样式一致）
for pptx_file in pptx_files:
    html_path = generate_preview_from_pptx(pptx_file, slide_index)
```

### 8.2 用户预览
- 在浏览器中打开HTML预览
- 检查布局、颜色、字体是否正确
- 检查图表数据是否准确

### 8.3 修改反馈
```
用户确认 → 继续下一页
用户提出修改 → 返回Step 5重新生成SVG
```

### 8.4 修改循环
```
生成SVG → 转换PPTX → 预览 → 用户反馈
    ↑                              ↓
    └──────── 修改意见 ←───────────┘
```

---

## Step 9: 最终打包

### 9.1 合并幻灯片
```python
# 合并所有确认的PPTX文件
final_pptx = merge_pptx_files(confirmed_slides)
```

### 9.2 添加全局元素
- 页码
- 页脚
- 动画效果（可选）

### 9.3 输出
- `workspace/output/final.pptx` - 最终PPT文件

---

## Step 10: 整理文件

### 10.1 清理中间文件
```python
# 保留重要文件
keep = [
    "workspace/output/final.pptx",
    "workspace/papers/",
    "workspace/agent_results/"
]

# 清理临时文件
clean = [
    "workspace/preview/*.svg",
    "workspace/preview/*.pptx",
    "workspace/preview/*.html"
]
```

### 10.2 生成制作报告
```markdown
# PPT制作报告

## 基本信息
- 论文标题：xxx
- 制作时间：xxx
- 总页数：xxx

## SVG生成统计
- 封面页：1页
- 内容页：N页
- 图表页：M页
- 技术示意图：K页

## 质量检查结果
- 通过率：100%
- 警告数：0
- 错误数：0

## 文件清单
- final.pptx - 最终PPT
- papers/ - 论文分析结果
- agent_results/ - Agent产出
```

### 10.3 最终产出
```
workspace/
├── output/
│   └── final.pptx              # 最终PPT
├── papers/
│   ├── analysis.json           # 论文分析
│   ├── goal.md                 # 目标文档
│   ├── requirements.md         # 需求文档
│   ├── blueprint.yaml          # PPT蓝图
│   └── spec_lock.md            # 视觉规范
├── agent_results/              # Agent产出
├── production_report.md        # 制作报告
└── README.md                   # 工作区说明
```

---

## 关键流程图

```
Step 5: 子Agent生成SVG
    ↓
Step 6: SVG后处理 + 质量检查
    ↓ (通过)
Step 7: SVG转PPTX
    ↓
Step 8: 预览确认
    ↓ (用户确认)
Step 9: 最终打包
    ↓
Step 10: 整理文件
```

## 错误处理

### SVG质量检查失败
```
check_svg_quality() → 返回错误列表
    ↓
修正SVG代码（调整颜色、字体、布局）
    ↓
重新检查
```

### SVG转PPTX失败
```
svg_to_pptx() → 返回错误
    ↓
检查SVG格式
    ↓
修正后重新转换
```

### 用户不满意
```
用户反馈修改意见
    ↓
返回Step 5重新生成SVG
    ↓
重新走完流程
```
