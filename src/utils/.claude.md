# src/utils/ 工具函数指南

## 文件职责
- `pdf_utils.py` - PDF处理工具函数
- `image_utils.py` - 图片处理工具函数

## 功能示例

### pdf_utils.py
- `extract_text_block(page, bbox)` - 提取指定区域文本
- `get_page_dimensions(page)` - 获取页面尺寸
- `find_figures_in_page(page)` - 查找页面中的图表位置

### image_utils.py
- `resize_image(path, max_width)` - 调整图片大小
- `convert_to_png(path)` - 转换为PNG格式
- `optimize_image(path, quality)` - 优化图片质量

## 规范
- 纯函数，无副作用
- 参数类型注解
- 单元测试覆盖
