import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL of the web page you want to scrape
url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"  # Replace with your actual URL

# Send an HTTP GET request to the URL and parse the HTML content
response = requests.get(url)
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')

# Find all div elements with the specified class and data-component-id
result_items = soup.find_all('div', {'class': 'rush-component s-featured-result-item ',
                                      'data-component-id': '2'})

# Create empty lists to store extracted data
links = []
titles = []
ratings = []
prices = []
num_reviews_list = []
product_urls = []

# Loop through the found div elements and extract the desired information
for item in result_items:
    img = item.find('img', {'class': 's-image'})
    link = img['src'] if img and 'src' in img.attrs else ''

    span_title = item.find('span', {'class': 'a-size-medium a-color-base a-text-normal'})
    title = span_title.text.strip() if span_title else ''

    span_rating = item.find('span', {'class': 'a-icon-alt'})
    rating = span_rating.text.strip() if span_rating else ''

    span_price = item.find('span', {'class': 'a-price-whole'})
    price = span_price.text.strip() if span_price else ''

    span_reviews = item.find('span', {'class': 'a-size-base s-underline-text'})
    num_reviews = span_reviews.text.strip() if span_reviews else ''

    a_link = item.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    product_url = a_link['href'] if a_link and 'href' in a_link.attrs else ''

    # Append extracted data to the respective lists
    links.append(link)
    titles.append(title)
    ratings.append(rating)
    prices.append(price)
    num_reviews_list.append(num_reviews)
    product_urls.append(product_url)

# Create a DataFrame using pandas
data = {
    'Link': links,
    'Title': titles,
    'Rating': ratings,
    'Price': prices,
    'Number of Reviews': num_reviews_list,
    'Product URL': product_urls
}
df = pd.DataFrame(data)

# Write the DataFrame to a CSV file
df.to_csv('products_data.csv', index=False)

print("Data extraction and writing to products_data.csv complete.")
