from nanoframe import NanoFrame
from nanoframe.io import to_csv, read_csv

data = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

df = NanoFrame(data)

to_csv(df, "out.csv")

df2 = read_csv("out.csv")
print("Loaded from CSV:")
print(df2)