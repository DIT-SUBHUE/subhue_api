from setuptools import find_packages, setup

setup(
    name="subhue",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "python-dotenv",
        "requests",
        "beautifulsoup4",
    ],
    author="Subhue - DIID",
    description="Integração com a API Subhue",
)
