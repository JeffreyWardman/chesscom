<div align="center">

# Chess.com Python API

<!-- Chess.com Banner -->
<img src="https://chessuniversity.com/wp-content/uploads/2020/02/c-com-logo.png" width="500">

[![Python 3.7+](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![PyPI Status](https://badge.fury.io/py/chesscom.svg)](https://badge.fury.io/py/chesscom) [![Downloads](https://pepy.tech/badge/chesscom)](https://pepy.tech/project/chesscom)

</div>

Unofficial Chess.com Python API and toolkit.

This Python API is a wrapper to the [PubAPI](https://www.chess.com/news/view/published-data-api) (a read-only REST API that responds with JSON-LD data).

## Install

Install from PyPi:

```
python3 -m pip install chesscom
```

Install locally

```
git clone git@github.com:jeffreywardman/chesscom.git
cd chesscom
python3 -m pip install -e .
```

## To Do

#### General

- Set up GitHub Actions
- API usage examples
- Unit tests done in docker container.

#### API

- Documentation
  - Codebase
    - Google-formatted docstrings
    - State frequency of endpoint updates
    - Add default values where possible
  - Read the Docs
- Model abstraction

#### Toolkit

- Plot by piece type
- Plot piece coverage
- Create game GIFs

## Final Comments

I will continue to maintain this repository so issues and pull requests are very welcome!

Feel free to add me ([jeffreywardman](https://www.chess.com/member/jeffreywardman)) on chess.com so we can play sometime!
