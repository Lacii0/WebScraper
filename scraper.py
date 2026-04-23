import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup

URL = "http://books.toscrape.com/index.html"
OUTPUT_FILE = "books.csv"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


def fetch_page(url: str) -> str:
    """Letölti az oldal HTML tartalmát."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logging.info("Oldal sikeresen letöltve.")
        return response.text
    except requests.RequestException as e:
        logging.error(f"Hiba az oldal betöltésekor: {e}")
        raise


def parse_books(html: str) -> list[dict]:
    """Kinyeri a könyvek címét és árát."""
    soup = BeautifulSoup(html, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    data = []

    for book in books:
        title_tag = book.h3.a
        price_tag = book.find("p", class_="price_color")

        title = title_tag["title"].strip() if title_tag and title_tag.has_attr("title") else "N/A"
        price = price_tag.text.strip() if price_tag else "N/A"

        data.append({
            "Cím": title,
            "Ár": price
        })

    logging.info(f"{len(data)} könyv feldolgozva.")
    return data


def save_to_csv(data: list[dict], filename: str) -> None:
    """CSV fájlba menti az adatokat."""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    logging.info(f"Adatok elmentve ide: {filename}")


def main() -> None:
    try:
        html = fetch_page(URL)
        books_data = parse_books(html)
        save_to_csv(books_data, OUTPUT_FILE)
        print("Az adatok sikeresen elmentve.")
    except Exception as e:
        print(f"Hiba történt: {e}")


if __name__ == "__main__":
    main()