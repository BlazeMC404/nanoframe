from nanoframe import NanoFrame

df = NanoFrame([
    {"name": "Alice", "score": 80},
    {"name": "Bob", "score": 85}
])

df["bonus"] = 5
df["total_score"] = df["score"] + df["bonus"]

print(df)