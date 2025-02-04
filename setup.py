from setuptools import setup, find_packages

setup(
    name="deep-research-cli",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"":"src"},
    install_requires=[
        "click>=8.0.0",
        "rich>=10.0.0"
    ],
    entry_points={
        "console_scripts": [
            "deep-research=deep_research.cli.main:main",
        ],
    },
    author="Xiaowen.Z",
    author_email="",
    description="A Python CLI tool for deep research",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.8"
)