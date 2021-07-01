from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

VERSION = "0.0.0"

setup(
    name="chesscom",
    version=VERSION,
    license="MIT",
    description="Chess.com unofficial Python API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jeffrey Wardman",
    author_email="jeffrey.wardman@yahoo.com.au",
    maintainer="Jeffrey Wardman",
    maintainer_email="jeffrey.wardman@yahoo.com.au",
    url="https://github.com/jeffreywardman/chesscom",
    download_url=f"https://github.com/jeffreywardman/chesscom/archive/v_{VERSION}.tar.gz",
    packages=find_packages(),
    keywords=["chess", "chess.com", "api"],
    install_requires=requirements,
)
