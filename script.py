import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape data from a single book page
def scrape_book(book_url):
    book_response = requests.get(book_url)
    book_soup = BeautifulSoup(book_response.text, 'html.parser')
    description_tag = book_soup.find('meta', attrs={'name': 'description'})
    description = description_tag['content'] if description_tag else 'None'
    rating_tag = book_soup.find('p', class_='star-rating')
    rating = rating_tag['class'][1] if rating_tag else 'None'
    breadcrumb_tag = book_soup.find('ul', class_='breadcrumb')
    breadcrumb = breadcrumb_tag.find_all('li') if breadcrumb_tag else []
    category = breadcrumb[2].text.strip() if len(breadcrumb) > 2 else 'None'
    img_tag = book_soup.find('div', class_='item active')
    img_url = base_url + img_tag.img['src'].replace('../', '') if img_tag and img_tag.img else 'None'
    quantity_tag = book_soup.find('p', class_='instock availability')
    quantity = quantity_tag.text.strip() if quantity_tag else 'None'
    price_tax_tag = book_soup.find('p', class_='price_color')
    price_tax = price_tax_tag.text if price_tax_tag else 'None'
    price_excluding_tax_tag = price_tax_tag.find_next_sibling('p') if price_tax_tag else None
    price_excluding_tax = price_excluding_tax_tag.text if price_excluding_tax_tag else 'None'
    return description, rating, category, img_url, quantity, price_tax, price_excluding_tax

# URL of the website to scrape
base_url = "https://books.toscrape.com/index.html"
initial_url = "https://books.toscrape.com/catalogue/page-1.html"
response = requests.get(initial_url)
soup = BeautifulSoup(response.text, 'html.parser')
books = soup.find_all('article', class_='product_pod')

# Define CSV file and headers
csv_file = open('books_data.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['UPC', 'Title', 'Description', 'Review Rating', 'Category', 'Image URL', 'Quantity Available', 'Product Page URL', 'Price (Including Tax)', 'Price (Excluding Tax)'])

# Iterate over each book and extract data
for book in books:
    upc = book.select_one('h3 a')['href'].split('/')[-1]
    title = book.select_one('h3 a')['title']
    book_url = base_url + book.select_one('h3 a')['href']
    description, rating, category, img_url, quantity, price_tax, price_excluding_tax = scrape_book(book_url)
    
    # Write data to CSV file
    csv_writer.writerow([upc, title, description, rating, category, img_url, quantity, book_url, price_tax, price_excluding_tax])

# Find and scrape data from the next page, if available
next_page = soup.find('li', class_='next')
if next_page:
    next_page_url = base_url + next_page.a['href']
    response_next = requests.get(next_page_url)
    soup_next = BeautifulSoup(response_next.text, 'html.parser')
    books_next = soup_next.find_all('article', class_='product_pod')
    
    for book_next in books_next:
        upc_next = book_next.select_one('h3 a')['href'].split('/')[-1]
        title_next = book_next.select_one('h3 a')['title']
        book_url_next = base_url + book_next.select_one('h3 a')['href']
        description_next, rating_next, category_next, img_url_next, quantity_next, price_tax_next, price_excluding_tax_next = scrape_book(book_url_next)
        
        # Write data to CSV file for the next page
        csv_writer.writerow([upc_next, title_next, description_next, rating_next, category_next, img_url_next, quantity_next, book_url_next, price_tax_next, price_excluding_tax_next])

csv_file.close()
print("Data saved to books_data.csv file.")

#file_name = 'books_scraped.csv'
#with open(file_name, "w", encoding="utf-8") as f:
   # f.write = csv.writer(f)
   # f.write.writerow(['UPC', 'title', 'description', 'review rating', 'category', 'image URL', 'quantity available', 'product page URL', 'price including tax', 'price excluding tax'])
   # print(csv)
#for i in range(len(price)):
   # f.write.writerow([i+1,])
