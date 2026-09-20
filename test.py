import pandas as pd

df = pd.read_csv("data.csv")

print("5 brs pertamaa:")
print(df.head())

print("\nStatistik Deskriptif:")
print(df.describe())