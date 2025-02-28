"""
Setup script for the Aika AI System package.
"""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="aika",
    version="0.1.0",
    author="Aiko Group",
    author_email="info@aikogroup.com",
    description="AI-powered insurance platform orchestration system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AikoGroup/Aika-v1",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: Other/Proprietary License",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "aika=src.cli:main",
        ],
    },
)
