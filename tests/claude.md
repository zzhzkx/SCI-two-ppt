# tests/ 测试指南

## 测试结构
```
tests/
├── test_parsers.py       # 解析模块测试
├── test_generators.py    # 生成模块测试
├── test_styles.py        # 规范库测试
├── test_core.py          # 核心模块测试
└── fixtures/             # 测试数据
    ├── sample.pdf        # 示例论文
    └── sample.pptx       # 示例PPT
```

## 运行测试
```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python -m pytest tests/test_parsers.py

# 带详细输出
python -m pytest tests/ -v
```

## 测试规范
- 使用 pytest 框架
- 异步测试使用 `pytest-asyncio`
- 测试文件命名: `test_*.py`
- 测试函数命名: `test_*`
- 使用 fixtures 管理测试数据

## 测试覆盖率目标
- 核心模块: > 90%
- 解析模块: > 80%
- 生成模块: > 80%
