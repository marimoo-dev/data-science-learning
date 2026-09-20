import requests
from bs4 import BeautifulSoup
import pdfplumber
import pandas as pd
from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent

URL_BPS = (
    "https://okukab.bps.go.id/id/publication/2025/09/26/"
    "fcc6fbfd6ef8af85d1e2c65c/"
    "kecamatan-baturaja-timur-dalam-angka-2025.html"
)

PDF_FILE = BASE_DIR / "kecamatan-baturaja-timur-dalam-angka-2025.pdf"
CSV_FILE = BASE_DIR / "data_penduduk_baturaja_timur_2024.csv"
LINK_FILE = BASE_DIR / "hasil_parsing_bps.csv"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/153.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8"
}


def angka(teks):
    teks = str(teks).replace("\n", " ").strip()
    hasil = re.sub(r"[^\d]", "", teks)
    return int(hasil) if hasil else 0


response = requests.get(
    URL_BPS,
    headers=HEADERS,
    timeout=15
)

print("Status Code:", response.status_code)

if response.status_code == 200:

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1")

    print("\nJudul Halaman:")
    print(title.get_text(strip=True) if title else "Tidak ditemukan")

    link_publikasi = None

    for link in soup.find_all("a", href=True):
        text = link.get_text(" ", strip=True)

        if "Unduh Publikasi" in text:
            link_publikasi = link["href"]
            break

    data_link = [{
        "Nama": "Unduh Publikasi",
        "Link": link_publikasi
    }]

    df_link = pd.DataFrame(data_link)

    df_link.to_csv(
        LINK_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nHasil Parsing:")
    print(df_link)

    if not PDF_FILE.exists() and link_publikasi:

        pdf_response = requests.get(
            link_publikasi,
            headers=HEADERS,
            timeout=30
        )

        if pdf_response.status_code == 200:
            PDF_FILE.write_bytes(pdf_response.content)
            print("\nPDF berhasil diunduh.")
        else:
            print("\nPDF gagal diunduh.")
            print("Status:", pdf_response.status_code)
            exit()

    data = []

    with pdfplumber.open(PDF_FILE) as pdf:

        halaman = pdf.pages[57]
        tabel = halaman.extract_tables()[0]

        for row in tabel:

            if len(row) < 4:
                continue

            nama = str(row[0]).replace("\n", " ").strip()

            if not re.match(r"^\d+\.", nama):
                continue

            laki = angka(row[1])
            perempuan = angka(row[2])
            total = angka(row[3])

            if laki > 0 and perempuan > 0 and total > 0:
                data.append({
                    "Desa_Kelurahan": nama,
                    "Laki_Laki": laki,
                    "Perempuan": perempuan,
                    "Jumlah_Penduduk": total
                })

    df = pd.DataFrame(data)

    df["Desa_Kelurahan"] = (
        df["Desa_Kelurahan"]
        .str.replace(r"^\d+\.\s*", "", regex=True)
    )

    print("\nData Penduduk Baturaja Timur 2024:")
    print(df)

    df.to_csv(
        CSV_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nDataset berhasil diproses.")
    print("File tersimpan:", CSV_FILE)

    print("\n[ANALISIS 1 - STATISTIK DASAR]")

    print(
        df["Jumlah_Penduduk"].describe()
    )

    print("\n[ANALISIS 2 - MEDIAN & PERSENTIL]")

    print("Median :", df["Jumlah_Penduduk"].median())
    print("P25    :", df["Jumlah_Penduduk"].quantile(0.25))
    print("P75    :", df["Jumlah_Penduduk"].quantile(0.75))

    print("\n[ANALISIS 3 - PERINGKAT PENDUDUK]")

    ranking = (
        df[["Desa_Kelurahan", "Jumlah_Penduduk"]]
        .sort_values(
            "Jumlah_Penduduk",
            ascending=False
        )
    )

    print(ranking)

else:
    print("Request gagal:", response.status_code)