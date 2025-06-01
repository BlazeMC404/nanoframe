# Nanoframe

**Nanoframe** is a minimalist, dependency-free Python data processing library. It offers intuitive, performant in-memory data structures (`NanoFrame` and `NanoSeries`) for handling tabular and columnar data efficiently and easily.

---

## Features

- Core data structures for frames (`NanoFrame`) and series (`NanoSeries`)
- CSV and JSON input/output
- Intelligent type inference and formatting
- Missing data handling (fill, drop)
- Arithmetic, aggregation, and filtering operations
- Chainable, Pythonic APIs for clear code
- Lightweight with no heavy dependencies
- Easy to extend and customize

---

## Installation

```bash
pip install nanoframe  # (coming soon on PyPI)
```

Or install from source:

```bash
git clone https://github.com/BlazeMC404/nanoframe.git
cd nanoframe/dist
pip install nanoframe-0.0.1-py3-none-any.whl
```

---

## Quick Start

```python
from nanoframe import NanoFrame

data = [
    {"name": "Alice", "age": 30, "score": 85.5},
    {"name": "Bob", "age": 25, "score": 91.2},
    {"name": "Charlie", "age": 35, "score": 78.0}
]

df = NanoFrame(data)

print(df)

print("Average score:", df["score"].mean())
```

---

## Documentation

- See the [Usage Guide](docs/usage.md)
- API references:
  - [`NanoFrame`](docs/frame.md)
  - [`NanoSeries`](docs/series.md)
  - [`I/O`](docs/io.md)

---

## Examples

Examples include:
- Creating frames and series
- Accessing data by rows and columns
- Filtering and arithmetic operations
- Handling missing data
- Saving and loading CSV/JSON files

Check the `examples/` directory for scripts.

---

## Contributing

Contributions, bug reports, and feature requests are welcome!

Please fork the repo and submit pull requests or open issues on GitHub:  
https://github.com/BlazeMC404/nanoframe

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## Contact

Created by BlazeMC404  
GitHub: https://github.com/BlazeMC404  
Email: blazemc404@gmail.com

---

## Note

This project is still in development. You may face some issues. Report the issues on [Issue](https://github.com/BlazeMC404/nanoframe/issues) or email.

---

If you like this project, don't forget to give a star.
