import requests
import warnings
import pandas as pd
from bs4 import BeautifulSoup
from utils import FLIPKART_LINK, FETCH_PERCENT, get_product_pages
from data import BRANDS
warnings.filterwarnings('ignore')


df = pd.DataFrame(columns=['Brand', 'Name', 'Price', 'Link', 'Features'])
index = 0
for brand in BRANDS.keys():
    try:
        if brand not in ['Lenovo Mobile', 'HTC Mobile', 'LG Mobile', 'Panasonic Mobile', 'Micromax Mobile', 'Gionee Mobile']:
            print('\nBrand:', brand)
            product_pages = get_product_pages(brand)

            for product_page in product_pages:
                response = requests.get(product_page)
                soup = BeautifulSoup(response.content, 'lxml')
                pages = soup.find('span', attrs={'class': '_2tDckM'}).text
                total_products = int(pages.split()[6])
                print('Total Products:', total_products)
                page, count = 1, 0
                while(count < total_products * FETCH_PERCENT):
                    page_link = product_page + '&page=' + str(page)
                    response = requests.get(page_link)
                    page += 1
                    soup = BeautifulSoup(response.content, 'lxml')
                    products = soup.find_all('div', attrs={'class': '_2kHMtA'})

                    for product in products:
                        name = product.find(
                            'div', attrs={'class': '_4rR01T'}).text
                        price = product.find(
                            'div', attrs={'class': '_30jeq3 _1_WHN1'}).text[1:]
                        link = FLIPKART_LINK + product.find('a').get('href')
                        fs = product.find('div', attrs={'class': 'fMghEO'}).find_all(
                            'li', attrs={'class': 'rgWa7D'})
                        features = [f.text for f in fs]

                        res = [brand, name, price, link, features]
                        df.loc[index] = res
                        index += 1

                        print(count, end=', ')
                        count += 1
    except:
        continue

df.to_csv('products.csv', index=False)
