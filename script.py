import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
url = "https://books.toscrape.com/"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find all the book containers
books = soup.find_all('article', class_='product_pod')

# Iterate over each book and extract UPC, title, description, review rating, category, image URL, quantity available, product page URL, price including tax, and price excluding tax
for book in books:
    # Extract UPC
    upc = book.select_one('h3 a')['href'].split('/')[2]
    
    # Extract title
    title = book.select_one('h3 a')['title']
    
    # Extract URL for the book detail page
    book_url = url + book.select_one('h3 a')['href']
    
    # Send a GET request to the book detail page
    book_response = requests.get(book_url)
    
    # Parse the HTML content of the book detail page
    book_soup = BeautifulSoup(book_response.text, 'html.parser')
    
    # Extract description
    description = book_soup.find('meta', attrs={'name': 'description'})['content']
    
    # Extract review rating
    rating = book_soup.find('p', class_='star-rating')['class'][1]
    
    # Extract category
    category = book_soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
    
    # Extract image URL
    img_url = url + book_soup.find('div', class_='item active').img['src'].replace('../', '')
    
    # Extract quantity available
    quantity = book_soup.find('p', class_='instock availability').text.strip()
    
    # Extract price including tax
    price_tax = book_soup.find('p', class_='price_color').text
    
    # Extract price excluding tax
    price_excluding_tax = book_soup.find('p', class_='price_color').find_next_sibling('p').text
    
    # Print UPC, title, description, review rating, category, image URL, quantity available, product page URL, price including tax, and price excluding tax
    print("UPC:", upc)
    print("Title:", title)
    print("Description:", description)
    print("Review Rating:", rating)
    print("Category:", category)
    print("Image URL:", img_url)
    print("Quantity Available:", quantity)
    print("Product Page URL:", book_url)
    print("Price (Including Tax):", price_tax)
    print("Price (Excluding Tax):", price_excluding_tax)
    print()














 








