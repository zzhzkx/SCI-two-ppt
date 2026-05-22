"""引用格式规范库."""

CITATION_FORMATS = {
    "IEEE": {
        "inline_format": "[{number}]",
        "reference_format": "{author}, \"{title},\" {journal}, vol. {volume}, no. {issue}, pp. {pages}, {year}.",
        "description": "IEEE格式 - 工程和计算机科学常用",
        "examples": [
            "[1] A. Author, \"Title of Paper,\" Journal Name, vol. 1, no. 2, pp. 10-20, 2024.",
            "[2] B. Author and C. Author, \"Another Paper,\" in Proc. Conference, 2024, pp. 100-110."
        ],
        "punctuation": {
            "author_separator": ",",
            "title_quotes": True,
            "journal_italic": False,
            "year_position": "end"
        }
    },
    "APA": {
        "inline_format": "({author}, {year})",
        "reference_format": "{author} ({year}). {title}. {journal}, {volume}({issue}), {pages}.",
        "description": "APA格式 - 社会科学和心理学常用",
        "examples": [
            "Author, A. (2024). Title of paper. Journal Name, 1(2), 10-20.",
            "Author, A., & Author, B. (2024). Title of paper. Journal Name, 1(2), 10-20."
        ],
        "punctuation": {
            "author_separator": ",",
            "title_quotes": False,
            "journal_italic": True,
            "year_position": "after_author"
        }
    },
    "MLA": {
        "inline_format": "({author} {page})",
        "reference_format": "{author}. \"{title}.\" {journal}, vol. {volume}, no. {issue}, {year}, pp. {pages}.",
        "description": "MLA格式 - 人文学科常用",
        "examples": [
            "Author, A. \"Title of Paper.\" Journal Name, vol. 1, no. 2, 2024, pp. 10-20."
        ],
        "punctuation": {
            "author_separator": "and",
            "title_quotes": True,
            "journal_italic": False,
            "year_position": "end"
        }
    },
    "Chicago": {
        "inline_format": "({author} {year}, {page})",
        "reference_format": "{author}. \"{title}.\" {journal} {volume}, no. {issue} ({year}): {pages}.",
        "description": "Chicago格式 - 历史和艺术学科常用",
        "examples": [
            "Author, A. \"Title of Paper.\" Journal Name 1, no. 2 (2024): 10-20."
        ],
        "punctuation": {
            "author_separator": "and",
            "title_quotes": True,
            "journal_italic": False,
            "year_position": "parenthetical"
        }
    },
    "Harvard": {
        "inline_format": "({author}, {year})",
        "reference_format": "{author} ({year}) '{title}', {journal}, {volume}({issue}), pp. {pages}.",
        "description": "Harvard格式 - 英国和澳大利亚常用",
        "examples": [
            "Author, A. (2024) 'Title of paper', Journal Name, 1(2), pp. 10-20."
        ],
        "punctuation": {
            "author_separator": "and",
            "title_quotes": True,
            "journal_italic": False,
            "year_position": "after_author"
        }
    }
}


async def get_citation_format(format_type: str = "IEEE") -> dict:
    """获取引用格式规范。

    Args:
        format_type: 格式名称 (IEEE/APA/MLA/Chicago/Harvard)

    Returns:
        dict: 引用格式规范
    """
    fmt = CITATION_FORMATS.get(format_type, CITATION_FORMATS["IEEE"])
    return {
        "format_type": format_type,
        **fmt
    }


async def get_available_formats() -> list[str]:
    """获取所有可用的引用格式。"""
    return list(CITATION_FORMATS.keys())
