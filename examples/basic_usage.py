from nanoframe import NanoFrame

data = [
    {"name": "Alice", "age": 28, "salary": 50000},
    {"name": "Bob", "age": 35, "salary": 62000},
    {"name": "Clara", "age": 40, "salary": 70000}
]

df = NanoFrame(data)

print("🔹 Basic Frame:")
print(df)

print("\n🔹 Column Access:")
print(df["name"])

print("\n🔹 Row Access:")
print(df.iloc[1])  # Bob's data