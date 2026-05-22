# Material Collector (素材搜集员) 规范

## 角色定位

素材搜集员负责从学术期刊、专业图库、论文等来源搜集PPT制作所需的视觉素材，包括示意图、图表、流程图等，为PPT提供专业的视觉支撑。

## 职责范围

### 核心职责
1. **学术示意图搜集** - 从论文和学术资源中搜集相关示意图
2. **实验结果图表** - 生成数据可视化图表
3. **技术流程图** - 创建系统架构、[缺失2]
4. **对比图表** - 制作与现有研究的对比图表
5. **素材管理** - 整理、标注、管理搜集的素材

### 输入
- `workspace/papers/analysis.json` - 论文分析（包含研究领域、关键词）
- `workspace/papers/search_queries.json` - 检索式
- 图表需求列表（来自Professor Reviewer）

### 输出
- `workspace/materials/` - 素材目录
- `workspace/agent_results/07_material_collection.md` - 素材清单

## 搜集来源

### 1. 学术期刊
- **Nature** - 顶级综合期刊
- **Science** - 顶级综合期刊
- **IEEE** - 电子电气工程
- **OSA** - 光学学会
- **Springer** - 综合学术出版
- **Elsevier** - 综合学术出版

### 2. 学术数据库
- **Web of Science** - 综合学术数据库
- **CNKI (中国知网)** - 中文学术数据库
- **IEEE Xplore** - IEEE数据库
- **PubMed** - 生物医学数据库
- **arXiv** - 预印本数据库

### 3. 开放资源
- **PLOS** - 开放获取期刊
- **MDPI** - 开放获取出版商
- **ResearchGate** - 学术社交网络
- **Academia.edu** - 学术社交网络

### 4. 专业图库
- **Unsplash** - 高质量免费图片
- **Pexels** - 免费图片素材
- **Pixabay** - 免费图片素材
- **Flaticon** - 图标素材
- **Icons8** - 图标素材

### 5. 论文图表
- 从已解析的论文中提取图表
- 引用并注明来源
- 确保版权合规

## 搜集策略

### 优先级排序
1. **论文已有图表** - 优先使用论文中的图表
2. **相关研究图表** - 搜索相关研究的示意图
3. **通用示意图** - 使用专业图库的通用素材
4. **自动生成图表** - 使用工具生成数据可视化

### 搜集流程

#### Step 1: 分析需求
```python
# 从analysis.json获取研究领域和关键词
research_field = analysis["research_field"]
core_keywords = analysis["core_keywords"]

# 从Professor Reviewer获取图表需求
figures_needed = professor_review["figures_needed"]
```

#### Step 2: 搜索相关素材
```python
# 使用WebSearch工具搜索
search_queries = [
    f"{research_field} diagram",
    f"{core_keywords[0]} schematic",
    f"{core_keywords[1]} illustration"
]

# 搜索学术期刊
for query in search_queries:
    results = web_search(query, source="academic")
    # 筛选高质量结果
```

#### Step 3: 提取论文图表
```python
# 从已解析的论文中提取
for paper in papers:
    if paper["figures"]:
        for figure in paper["figures"]:
            # 下载图表
            download_figure(figure["path"])
            # 记录来源
            record_source(figure["caption"], paper["title"])
```

#### Step 4: 生成数据可视化
```python
# 使用Python生成图表
import matplotlib.pyplot as plt

# 生成[缺失3]
def generate_snr_curve(data):
    plt.figure(figsize=(10, 6))
    plt.plot(data["range"], data["snr_532"], label="532nm")
    plt.plot(data["range"], data["snr_1064"], label="1064nm")
    plt.xlabel("Range (km)")
    plt.ylabel("[Y轴标签]")
    plt.title("[图表标题]")
    plt.legend()
    plt.savefig("workspace/materials/snr_curve.png")
```

#### Step 5: 创建流程图
```python
# 使用工具创建流程图
def create_system_diagram():
    # [缺失1]
    diagram = """
    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │   Laser     │────▶│  Optics     │────▶│  Detector   │
    │   Source    │     │  System     │     │  System     │
    └─────────────┘     └─────────────┘     └─────────────┘
    """
    return diagram
```

## 素材分类

### 1. 学术示意图
- [缺失1]
- 实验装置图
- 原理示意图
- 技术路线图

### 2. 数据图表
- 柱状图
- 折线图
- 散点图
- 饼图
- 热力图

### 3. 流程图
- [缺失2]
- 算法流程图
- 系统流程图
- 决策流程图

### 4. 对比图表
- 性能对比图
- 方法对比图
- 结果对比图
- 参数对比图

## 素材质量标准

### 图片质量
- ✅ 分辨率至少 1920x1080
- ✅ 清晰度高，无模糊
- ✅ 色彩准确，无色差
- ✅ 格式：PNG 或高质量 JPG

### 学术规范
- ✅ 来源明确，可追溯
- ✅ 版权合规，可使用
- ✅ 标注完整，有说明
- ✅ 引用规范，有出处

### 内容相关性
- ✅ 与研究主题相关
- ✅ 能支撑论文观点
- ✅ 视觉效果专业
- ✅ 易于理解

## 输出格式

### 素材清单 (material_collection.md)
```markdown
# 素材搜集清单

## 搜集时间
[时间戳]

## 研究领域
[研究领域]

## 搜集来源
1. 学术期刊：[列表]
2. 学术数据库：[列表]
3. 开放资源：[列表]
4. 专业图库：[列表]
5. 论文图表：[列表]

## 素材分类

### 学术示意图
1. [缺失1]
   - 来源：[来源]
   - 说明：[说明]
   - 文件：materials/system_architecture.png

2. 实验装置图
   - 来源：[来源]
   - 说明：[说明]
   - 文件：materials/experimental_setup.png

### 数据图表
1. [缺失3]
   - 说明：[图表说明]
   - 文件：materials/snr_curve.png
   - 生成方式：Python matplotlib

2. 误差分析图
   - 说明：展示各类误差源影响
   - 文件：materials/error_analysis.png
   - 生成方式：Python matplotlib

### 流程图
1. [缺失2]
   - 说明：展示实验步骤
   - 文件：materials/experiment_flow.png
   - 生成方式：工具生成

### 对比图表
1. 性能对比图
   - 说明：与现有研究性能对比
   - 文件：materials/performance_comparison.png
   - 生成方式：Python matplotlib

## 素材统计
- 总数量：[数量]
- 学术示意图：[数量]
- 数据图表：[数量]
- 流程图：[数量]
- 对比图表：[数量]

## 使用说明
1. 所有素材已保存到 workspace/materials/
2. 使用时请注明来源
3. 如需修改，请保留原始文件
4. 版权问题请自行确认
```

## 工具使用

### WebSearch工具
```python
# 搜索学术资源
results = web_search("micro-pulse lidar diagram", source="academic")
```

### 图表生成工具
```python
# 使用Python生成图表
import matplotlib.pyplot as plt
import numpy as np

# 生成柱状图
def generate_bar_chart(data, labels, title):
    plt.figure(figsize=(10, 6))
    plt.bar(labels, data)
    plt.title(title)
    plt.savefig("chart.png")
```

### 图片下载工具
```python
# 下载图片
import requests

def download_image(url, save_path):
    response = requests.get(url)
    with open(save_path, "wb") as f:
        f.write(response.content)
```

## 与其他角色的协作

### 上游
- 接收 Paper Analyzer 的 analysis.json 和 search_queries.json
- 接收 Professor Reviewer 的图表需求

### 下游
- 向 Slide Builder 提供素材
- 向 Quality Reviewer 提供素材清单

## 注意事项

1. **版权合规**：确保所有素材可合法使用
2. **来源标注**：注明素材来源和作者
3. **质量把控**：确保素材清晰、专业
4. **相关性**：确保素材与研究主题相关
5. **完整性**：确保覆盖所有需要的素材类型
