"""
Setup script for the exo multi-agent system.
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("exo/requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="exo-agent",
    version="0.1.0",
    author="exo Team",
    author_email="info@example.com",
    description="A multi-agent AI system with hierarchical agent architecture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/exo",
    packages=["exo"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "exo=exo.__main__:main",
        ],
    },
    include_package_data=True,
)
