from nanoframe import NanoFrame

df = NanoFrame([
    {"name": "Alice", "age": 28},
    {"name": "Bob", "age": 35},
    {"name": "Clara", "age": 22}
])

print("People older than 30:")
print(df[df["age"] > 30])