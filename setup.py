"""
Setup script for infosci-spark-client package
"""

from setuptools import setup
import os

# Read the README file if it exists
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
long_description = ""
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="infosci-spark-client",
    version="0.1.0",
    description="A simple Python client for the Information Science Department Spark API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Peter Bidoshi",
    author_email="pjb294@cornell.edu",
    url="https://github.com/mrpeterss/infosci-spark-client",
    packages=["infosci_spark_client"],
    install_requires=[
        "requests>=2.25.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords=["llm", "api", "client", "infosci", "spark"],
)
