# SCI-two-ppt

AI-powered scientific paper to presentation PPT generator.

## Features

- **论文解析**: 自动解析PDF论文，提取标题、摘要、方法、结果、关键发现
- **图表提取**: 从PDF中提取图片和表格
- **学术规范库**: 6个学科领域的配色/字体/排版规范
- **9种页面模板**: 标题页、内容页、图表页、对比页、总结页等
- **5种引用格式**: IEEE/APA/MLA/Chicago/Harvard
- **逐页构建**: 像真人一样逐页制作PPT
- **差异检测**: 自动检测PowerPoint中的手动修改

## 安装

```bash
# 克隆仓库
git clone https://github.com/zzhzkx/SCI-two-ppt.git
cd SCI-two-ppt

# 安装依赖
pip install -r requirements.txt

# 配置API密钥
cp config/settings.yaml config/settings.local.yaml
# 编辑 settings.local.yaml 填入你的 API key
```

## 在 Claude Code 中使用

### 配置 MCP Server

在 Claude Code 设置中添加:

```json
{
  "mcpServers": {
    "sci-two-ppt": {
      "command": "python",
      "args": ["-m", "src.mcp_server"],
      "cwd": "/path/to/SCI-two-ppt"
    }
  }
}
```

### 使用方法

1. 在 Claude Code 中说: "帮我把这篇论文做成PPT"
2. 提供论文PDF路径
3. Claude 会自动执行10步工作流:
   - 解析论文
   - 询问需求
   - 构建目标文档
   - 分派子Agent
   - 逐页生成PPT

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
| `get_academic_style` | 学术规范 |
| `get_slide_template` | 页面模板 |
| `get_citation_format` | 引用格式 |
| `build_goal` | 构建目标文档 |
| `run_subagent` | 调度子Agent |
| `generate_blueprint` | 蓝图生成 |

## 项目结构

```
SCI-two-ppt/
├── src/
│   ├── mcp_server.py      # MCP Server 入口
│   ├── core/              # 核心配置
│   ├── parsers/           # 论文解析
│   ├── generators/        # PPT生成
│   └── styles/            # 学术规范库
├── templates/             # PPT模板
├── skills/                # Skill文件
├── tests/                 # 测试
└── docs/                  # 文档
```

## 运行测试

```bash
python tests/test_e2e.py
```

## 学术规范库

支持的领域:
- `optics` - 光学
- `physics` - 物理学
- `chemistry` - 化学
- `computer_science` - 计算机科学
- `biology` - 生物学
- `general` - 通用

## 引用格式

- IEEE - 工程和计算机科学
- APA - 社会科学
- MLA - 人文学科
- Chicago - 历史和艺术
- Harvard - 英国和澳大利亚

## License

MIT
