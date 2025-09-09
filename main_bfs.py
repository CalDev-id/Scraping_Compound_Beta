import requests
from bs4 import BeautifulSoup
from googlesearch import search
import json
import re
from urllib.parse import urlparse

def get_top_links(query, num_results=10):
    links = []
    for url in search(query, num_results=num_results, lang="id"):
        # skip link facebook, instagram, dll
        if any(bad in url for bad in ["facebook.com", "instagram.com", "tiktok.com"]):
            continue
        links.append(url)
    return links

def scrape_bs4(url):
    try:
        resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")

        # Judul
        judul = soup.title.string.strip() if soup.title else "Unknown"

        # Tanggal
        tanggal = "Unknown"
        time_tag = soup.find("time")
        if time_tag:
            tanggal = time_tag.get_text(strip=True)

        # Sumber → ambil dari domain
        parsed_url = urlparse(url)
        sumber = parsed_url.netloc.replace("www.", "")

        # Ambil teks (gabungan dari <p> + div khusus)
        paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
        div_candidates = soup.find_all("div", class_=re.compile("(article|content|post|isi|entry)"))
        for div in div_candidates:
            paragraphs.extend([p.get_text(" ", strip=True) for p in div.find_all("p")])

        # Buang paragraf pendek (<50 char)
        paragraphs = [p for p in paragraphs if len(p) > 50]
        content = "\n".join(paragraphs)

        return {
            "judul": judul,
            "tanggal": tanggal,
            "sumber": sumber,
            "link": url,
            "content": content if content else "Tidak berhasil ekstrak isi artikel"
        }
    except Exception as e:
        return {
            "judul": "ERROR",
            "tanggal": "ERROR",
            "sumber": "ERROR",
            "link": url,
            "content": f"Scraping error: {e}"
        }

def cari_dan_scrape(query):
    hasil = []
    links = get_top_links(query, num_results=10)
    for url in links:
        print(f"Scraping {url} ...")
        hasil.append(scrape_bs4(url))
    return hasil

# 🔹 Contoh pemakaian
query = "presiden halimah di tolak warga etnis china sultan brunei ancam beli singapura"
data = cari_dan_scrape(query)

print(json.dumps(data, indent=2, ensure_ascii=False))
