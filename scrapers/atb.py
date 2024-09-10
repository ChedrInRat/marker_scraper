from typing import Generator
from db import Product
from .scraper import SyncScraper 
import bs4



class ATB(SyncScraper):

    name = 'ATB'
    start_url = 'https://www.atbmarket.com'
    reload_driver = True
    
    def __init__(self) -> None:
        super().__init__()
    
    def get_product(self) -> Generator[Product]:
        for product_url in self.get_product_url():
            url = self.start_url + product_url
            page = self.get_page(self.start_url + product_url)
            soup = bs4.BeautifulSoup(page, 'html.parser') 

            name = soup.select_one('h1').text
            price = float(soup.select_one('div.product-price span').text)

            product = Product(url=url, name=name, price=price)

            yield product
    

    def get_product_url(self):
        for products in self.get_products():
            for product in products:
                yield product['href']

    
    def get_products(self):
        for page in self.get_products_page():
            soup = bs4.BeautifulSoup(page, 'html.parser')
            products_block = soup.select_one('div.catalog-list')

            products_list = products_block.select('article div.catalog-item__info a[href]') if products_block else set()

            yield products_list
    

    def get_products_page(self):
        for subcategory_url in self.get_subcategory_url():
            page = self.get_page(self.start_url + subcategory_url)
            soup = bs4.BeautifulSoup(page, 'html.parser')

            if pagination := soup.select_one('ul.product-pagination__list'):
                prev_page = 0

                page_num_block = pagination.select_one('ul.product-pagination__item.active')
                page_num = page_num_block.get_text() if page_num_block else 0
                
                while page_num != prev_page:
                    prev_page = page_num
                    url = self.start_url + subcategory_url + f'?page={int(page_num) + 1}'
                    page = self.get_page(url)

                    yield page
            else:
                yield page

            
    def get_subcategory_url(self):
        for subcategories in self.get_subcategories():
            for subcategory in subcategories:
                if subcategory_url_block := subcategory.find('a', href=True):
                    subcategory_url = subcategory_url_block['href']
                    yield subcategory_url 
        

    def get_subcategories(self):
        '''
        Returns a List[bs4 objects] with category
        '''
        for category_url in self.get_category_url():
            page = self.get_page(self.start_url + category_url)

            soup = bs4.BeautifulSoup(page, 'html.parser')
            if subcategory_list := soup.select('div.catalog-subcategory-list span.custom-tag:not(.custom-tag--white-active)'):
                yield subcategory_list
        

    def get_category_url(self):
        '''
        Generator category url
        '''
        for category in self.get_category():
            if category_url := category.find('a', href=True)['href']:
                yield category_url 


    def get_category(self):
        '''
        Generator bs4 object with category 
        '''
        for category in self.get_categories():
            if category:
                yield category 
    
    def get_categories(self):
        '''
        Returns a List[bs4 objects] with categories
        '''

        page = self.get_page(self.start_url)

        soup = bs4.BeautifulSoup(page, 'html.parser')
        category_menu = soup.select_one('ul.category-menu')
        
        categories = category_menu.select('li.category-menu__item:not(.category-menu__item--not-dropdown)') if category_menu else set() 

        return categories
    


if __name__ == '__main__':
    scraper = ATB()

    for product in scraper.get_product():
        print(product)
