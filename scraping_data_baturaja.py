import pandas as pd
from pathlib import Path

file = Path(__file__).resolve().parent / "data_penduduk_baturaja_timur_2024.csv"

df = pd.read_csv(file)

print("[OK] Dataset berhasil dibaca")

print("\n[INFO] INFORMASI DATASET")
print("=" * 50)
print("Jumlah Baris :", len(df))
print("Jumlah Kolom :", len(df.columns))
print("Kolom        :", list(df.columns))

print("\nTipe Data:")
print(df.dtypes)

print("\nSample Data (5 baris pertama):")
print(df.head().to_string(index=False))


print("\n[ANALISIS 1] STATISTIK DESKRIPTIF DASAR")
print("=" * 50)

penduduk = df["Jumlah_Penduduk"]

print(penduduk.describe().round(2).to_string())

print("\n>> Insight:")
print(f"Mean   = {penduduk.mean():,.2f} jiwa")
print(f"Median = {penduduk.median():,.2f} jiwa")
print(f"Min    = {penduduk.min():,.0f} jiwa")
print(f"Max    = {penduduk.max():,.0f} jiwa")


print("\n[ANALISIS 2] DISTRIBUSI & PERCENTILE")
print("=" * 50)

print(f"P25 = {penduduk.quantile(0.25):,.0f} jiwa")
print(f"P50 = {penduduk.quantile(0.50):,.0f} jiwa")
print(f"P75 = {penduduk.quantile(0.75):,.0f} jiwa")

bins = [0, 5000, 10000, 15000, float("inf")]
labels = ["Rendah (<5 ribu)", "Sedang (5-10 ribu)", "Tinggi (10-15 ribu)", "Sangat Tinggi (>15 ribu)"]

kategori = pd.cut(
    penduduk,
    bins=bins,
    labels=labels,
    right=False
)

distribusi = kategori.value_counts().sort_index()

print("\nDistribusi Kategori Penduduk:")
for kategori_nama, jumlah in distribusi.items():
    persen = jumlah / len(df) * 100
    print(f"{kategori_nama}: {jumlah} desa/kelurahan ({persen:.1f}%)")


print("\n[ANALISIS 3] RANKING JUMLAH PENDUDUK")
print("=" * 50)

ranking = df[
    ["Desa_Kelurahan", "Jumlah_Penduduk"]
].sort_values(
    by="Jumlah_Penduduk",
    ascending=False
)

print("\n5 Desa/Kelurahan dengan Penduduk Terbanyak:")
print(
    ranking.head(5).to_string(index=False)
)

print("\n5 Desa/Kelurahan dengan Penduduk Terendah:")
print(
    ranking.tail(5)
    .sort_values("Jumlah_Penduduk")
    .to_string(index=False)
)

tertinggi = ranking.iloc[0]
terendah = ranking.iloc[-1]

print("\n>> Insight:")
print(
    f"Penduduk terbanyak = {tertinggi['Desa_Kelurahan']} "
    f"({tertinggi['Jumlah_Penduduk']:,.0f} jiwa)"
)

print(
    f"Penduduk terendah = {terendah['Desa_Kelurahan']} "
    f"({terendah['Jumlah_Penduduk']:,.0f} jiwa)"
)