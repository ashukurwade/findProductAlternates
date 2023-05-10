import requests
from bs4 import BeautifulSoup
import json



def FindAlternateGroups(store_domain):
    # retrieve product links
    page = requests.get(store_domain)
    soup = BeautifulSoup(page.content, 'html.parser')
    products = soup.find_all('div', class_='product-item')
    links = [product.find('a')['href'] for product in products]

    # find alternate groups
    alternates = []
    for link in links:
        alternate_group = [link]
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        product_name = soup.find('h1', class_='product-name').text.strip().lower()
        product_description = soup.find('div', class_='product-description').text.strip().lower()
        related_products = soup.find_all('a', class_='related-product-link')
        
        for related_product in related_products:
            related_product_link = related_product['href']
            page = requests.get(related_product_link)
            soup = BeautifulSoup(page.content, 'html.parser')
            related_product_name = soup.find('h1', class_='product-name').text.strip().lower()
            related_product_description = soup.find('div', class_='product-description').text.strip().lower()
            
            if product_name == related_product_name or product_description == related_product_description:
                if related_product_link not in alternate_group:
                    alternate_group.append(related_product_link)
        
        if len(alternate_group) > 1:
            alternates.append({"product alternates": alternate_group})
    
    return json.dumps(alternates)


store_domain = 'https://sartale2022.myshopify.com/products/adam-suede-penny-loafer-in-navy-blue'
alternates = FindAlternateGroups(store_domain)
print(alternates)

