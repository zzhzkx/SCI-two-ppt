# Step 6-10: 制作输出工作流

## Step 8: 逐页制作PPT

### 预览方式

1. **HTML预览**：浏览器中查看，支持交互操作
2. **图片预览**：生成PNG图片
3. **PPT预览**：直接用PowerPoint打开

### 修改方式

1. **对话式修改**：用户通过对话提出修改意见
2. **标注式修改**：用户在预览中标注修改位置
3. **手动修改反馈**：用户在PowerPoint中手动修改，系统检测变化

### 反馈学习系统

```python
# 检测用户手动修改
changes = detect_changes(original, modified)

# 学习反馈模式
feedback_patterns = learn_from_feedback(changes, slide_index)

# 生成反馈总结
summary = generate_feedback_summary(feedback_patterns)

# 应用反馈到后续页面
blueprint = apply_feedback_to_next_slides(feedback_patterns, blueprint)
```

### 完整流程

```
生成第N页 → 预览 → 用户审查 → 修改/确认
    ↓
检测手动修改 → 学习反馈 → 生成总结
    ↓
应用反馈到后续页面 → 继续第N+1页
```

详见完整文档。