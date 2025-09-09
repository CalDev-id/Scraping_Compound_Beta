from googlesearch import search
from newspaper import Article
import json

def get_top_links(query, num_results=10):
    """Cari link dari Google Search"""
    links = []
    for url in search(query, num_results=num_results, lang="id"):
        links.append(url)
    return links

def scrape_article(url):
    """Scraping isi artikel dengan newspaper3k"""
    try:
        article = Article(url, language="id")
        article.download()
        article.parse()

        return {
            "judul": article.title,
            "tanggal": str(article.publish_date) if article.publish_date else "Unknown",
            "author": ", ".join(article.authors) if article.authors else "Unknown",
            "link": url,
            "content": article.text
        }
    except Exception as e:
        return {
            "judul": "ERROR",
            "tanggal": "ERROR",
            "author": "ERROR",
            "link": url,
            "content": f"ERROR scraping: {e}"
        }

def cari_dan_scrape(query):
    hasil = []
    links = get_top_links(query, num_results=10)
    for url in links:
        hasil.append(scrape_article(url))
    return hasil

# 🔹 Contoh pemakaian
query = "presiden halimah di tolak warga etnis china sultan brunei ancam beli singapura"
data = cari_dan_scrape(query)

# Print JSON hasil
print(json.dumps(data, indent=2, ensure_ascii=False))
