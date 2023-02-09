import requests
from bs4 import BeautifulSoup


FETCH_PERCENT = 0.2
FLIPKART_LINK = 'https://www.flipkart.com'
BRANDS_PAGE = 'https://www.flipkart.com/mobile-phones-store?otracker=nmenu_sub_Electronics_0_Mobiles'


def get_brands():
    response = requests.get(BRANDS_PAGE)
    soup = BeautifulSoup(response.content, 'lxml')
    table = soup.find('div', attrs={'class': '_1Vtd9D'}).find(
        'table').find('tbody')

    brands = {}
    trs = table.find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        for td in tds:
            brands[td.text] = FLIPKART_LINK + td.find('a').get('href')
    return brands


def get_all_product_pages():
    product_pages = []
    brands = get_brands()
    for brand in brands.keys():
        response = requests.get(brands[brand])
        soup = BeautifulSoup(response.content, 'lxml')
        columns = soup.find_all('div', attrs={'class': '_1xCO19'})

        if len(columns) > 0:
            for column in columns:
                try:
                    product_page = FLIPKART_LINK + column.find('a').get('href')
                    product_pages.append(product_page)
                except:
                    continue
        else:
            product_pages.append(brands[brand])
    return product_pages


def get_product_pages(brand):
    product_pages = []
    brands = get_brands()
    response = requests.get(brands[brand])
    soup = BeautifulSoup(response.content, 'lxml')
    columns = soup.find_all('div', attrs={'class': '_1xCO19'})

    if len(columns) > 0:
        for column in columns:
            try:
                product_page = FLIPKART_LINK + column.find('a').get('href')
                product_pages.append(product_page)
            except:
                continue
    else:
        product_pages.append(brands[brand])
    return product_pages
