import requests
from bs4 import BeautifulSoup
import csv

def scrape_books(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', class_='product_pod')
    data = []
    for book in books:
        title = book.h3.a['title']
        product_url = url.rsplit('/', 2)[0] + '/' + book.h3.a['href']
        price = book.find('p', class_='price_color').text
        rating = book.find('p', class_='star-rating')['class'][1]
        category = soup.find('ul', class_='breadcrumb').find_all('li')[-1].text.strip()
        image_url = url.rsplit('/', 2)[0] + '/' + book.img['src']
        data.append((title, product_url, price, rating, category, image_url))
    return data

def save_to_csv(data):
    with open('books.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Product URL', 'Price', 'Rating', 'Category', 'Image URL'])
        for item in data:
            title = item[0].replace(',', '')  # Remove commas from title
            writer.writerow([title] + list(item[1:]))

if __name__ == "__main__":
    url = "https://books.toscrape.com/catalogue/category/books/christian-fiction_34/index.html"
    book_data = scrape_books(url)
    save_to_csv(book_data)
    print("Scraping and saving complete!")










 








