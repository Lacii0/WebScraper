import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


if not os.path.exists('data'):
    os.mkdir('data')

url = "http://books.toscrape.com/index.html"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

books = []
for item in soup.find_all('article', class_='product_pod'):
    title = item.h3.a['title']
    price = item.find('p', class_='price_color').text
    books.append({'Cím': title, 'Ár': price})

df = pd.DataFrame(books)
df.to_csv('data/könyvek.csv', index=False, encoding='utf-8')

print("A könyv adatai lementve: data/könyvek.csv")