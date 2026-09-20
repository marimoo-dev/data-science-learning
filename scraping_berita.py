import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

url = "https://sumsel.antaranews.com/tag/baturaja"

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        data_berita = []

        for item in soup.select("a"):
            judul = item.get_text(" ", strip=True)
            link = item.get("href")

            if judul and link and "/berita/" in link and len(judul) > 10:
                data_berita.append({
                    "No": len(data_berita) + 1,
                    "Judul Berita": judul,
                    "Link Berita": link
                })

            if len(data_berita) >= 5:
                break

        if len(data_berita) >= 5:
            df = pd.DataFrame(data_berita[:5])

            print("5 Berita Terbaru:\n")

            for _, row in df.iterrows():
                print(f"{row['No']}. {row['Judul Berita']}")
                print(f"   {row['Link Berita']}\n")

            output_file = (
                Path(__file__).resolve().parent /
                "hasil_scraping_berita.csv"
            )

            df.to_csv(
                output_file,
                index=False,
                encoding="utf-8-sig"
            )

            print("Scraping berhasil!")
            print("File tersimpan:", output_file)

        else:
            print("Berita kurang dari 5.")

    else:
        print("Request gagal:", response.status_code)

except requests.RequestException as e:
    print("Request error:", e)

except Exception as e:
    print("Error:", e)