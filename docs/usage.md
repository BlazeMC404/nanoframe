
# 📘 Nanoframe Usage Guide

This guide covers the basic and advanced usage of the `nanoframe` library.

---

## 📥 Importing

```python
from nanoframe import NanoFrame, NanoSeries
```

---

## 📊 Creating a NanoFrame

You can create a `NanoFrame` from a list of dictionaries:

```python
data = [
    {"name": "Alice", "age": 30, "score": 88.5},
    {"name": "Bob", "age": 25, "score": 92.1},
    {"name": "Charlie", "age": 35, "score": 78.4}
]

df = NanoFrame(data)
```

---

## 📄 Viewing Data

```python
print(df)
print(df.head(2))
print(df.tail(2))
print(df.info())
```

---

## 📌 Accessing Data

### By Column

```python
df["name"]            # Returns a NanoSeries
df[["name", "score"]] # Returns a new NanoFrame
```

### By Row

```python
df.iloc[0]     # Row as dictionary
df.iloc[1:3]   # Subset of rows
```

---

## 🔁 Operations

### Filtering

```python
df[df["age"] > 30]
```

### Arithmetic

```python
df["score"] + 5
df["score"] * df["age"]
```

---

## 📈 Aggregations

```python
df["score"].mean()
df["score"].sum()
df["score"].min()
df["score"].max()
```

---

## 🧹 Handling Missing Values

```python
df.fillna(0)
df.dropna()
```

---

## 💾 I/O Operations

### Read CSV / JSON

```python
from nanoframe.io import read_csv, read_json

df_csv = read_csv("data.csv")
df_json = read_json("data.json")
```

### Write CSV / JSON

```python
from nanoframe.io import to_csv, to_json

to_csv(df, "output.csv")
to_json(df, "output.json")
```

---

## 🔬 Type Inference

```python
df.dtypes()
```

---

## 🛠️ Coming Soon

- GroupBy operations
- Merging/joining frames
- Indexing enhancements
- Backend optimizations

---

## 📎 Related

See [index.md](./index.md) for project overview.
