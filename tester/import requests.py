import requests
from bs4 import BeautifulSoup
url = "https://books.toscrape.com/catalogue/"
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')