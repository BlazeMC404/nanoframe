
# Nanoframe: Minimalist Python DataFrame Library

**Nanoframe** is a lightweight, dependency-free data processing library designed for clarity, performance, and ease of use — similar in spirit to pandas.

---

## 🚀 Features

- Simple and fast in-memory data structures
- `NanoFrame` and `NanoSeries` for tabular and columnar data
- Built-in CSV and JSON I/O
- Type inference and formatting
- Missing value handling
- Arithmetic and aggregation operations
- Chainable APIs
- Easy to extend

---

## 📦 Installation

```bash
pip install nanoframe  # (coming soon on PyPI)
```

Or install directly from source:

```bash
git clone https://github.com/BlazeMC404/nanoframe.git
cd nanoframe/dist
pip install nanoframe-0.0.1-py3-none-any.whl
```

---

## 🧪 Quick Start

```python
from nanoframe import NanoFrame

data = [
    {"name": "Alice", "age": 30, "score": 85.5},
    {"name": "Bob", "age": 25, "score": 91.2},
    {"name": "Charlie", "age": 35, "score": 78.0}
]

df = NanoFrame(data)

print(df)

print(df["score"].mean())  # 84.9
```

---

## 📚 Modules

- [`NanoFrame`](./frame.md): The core DataFrame-like container.
- [`NanoSeries`](./series.md): Single-column data structure.
- [`I/O`](./io.md): Read/write CSV and JSON files.
- [`Utils`](./utils.md): Internal helpers for type inference, formatting, etc.

---

## 🛠️ Project Status

**Nanoframe** is under active development. Contributions and feedback are welcome!

- GitHub: [github.com/BlazeMC404/nanoframe](https://github.com/BlazeMC404/nanoframe)
- License: MIT
