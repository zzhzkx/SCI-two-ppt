from setuptools import setup, find_packages

setup(
    name="sci-two-ppt",
    version="0.1.0",
    description="AI-powered scientific paper to presentation PPT generator",
    author="twotwo",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "python-pptx>=0.6.23",
        "anthropic>=0.30.0",
        "PyYAML>=6.0",
        "aiohttp>=3.9.0",
        "Pillow>=10.0.0",
        "PyMuPDF>=1.24.0",
        "rich>=13.0.0",
    ],
)
