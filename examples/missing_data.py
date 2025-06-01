from nanoframe import NanoFrame

df = NanoFrame([
    {"name": "Alice", "age": 28},
    {"name": "Bob", "age": None},
    {"name": "Clara", "age": 30}
])

print("Original:")
print(df)

print("\nFill missing with 0:")
print(df.fillna(0))

print("\nDrop missing rows:")
print(df.dropna())