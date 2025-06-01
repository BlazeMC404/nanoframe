from nanoframe import NanoFrame

df = NanoFrame([
    {"name": "Alice", "score": 88},
    {"name": "Bob", "score": 75},
    {"name": "Clara", "score": 92}
])

print("Mean Score:", df["score"].mean())
print("Max Score:", df["score"].max())
print("Min Score:", df["score"].min())