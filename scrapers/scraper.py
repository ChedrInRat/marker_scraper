import requests, time

from typing import Any, AsyncGenerator, Generator
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from db import Product 


class ScraperBase(ABC):

    name:str
    start_url:str
    reload_driver:bool = True

    
    @abstractmethod
    def _get_driver(self, *args, **kwargs) -> Any:
        pass
    
    
    @abstractmethod
    def get_page(self, *args, **kwargs) -> Any:
        pass


    @abstractmethod
    def get_product(self) -> Any:
        pass


class SyncScraper(ScraperBase):

    def __init__(self) -> None:
        super().__init__()
        self.driver = self._get_driver()


    def _get_driver(self) -> webdriver.Chrome:
        driver_options = Options()
        driver_options.add_argument('--disable-gpu')
        driver_options.add_argument('--no-sandbox')
        driver_options.add_argument('User-agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0')
        
        return webdriver.Chrome(options=driver_options)


    def get_page(self, url:str, timeout=1) -> str:
        print(f'{url=}')

        user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'}
        response = requests.get(url, headers=user_agent)

        if response.status_code == 200:
            content = response.text
        else:
            content = self._driver_get_page(url)
        
        time.sleep(timeout)

        return content
    

    def _driver_get_page(self, url) -> str:
        if self.reload_driver:
            with self._get_driver() as driver:
                driver.get(url)
                return driver.page_source
        else:
            self.driver.get(url)
            return self.driver.page_source


    @abstractmethod
    def get_product(self) -> Generator[Product]:
        pass


class AsyncScraper(ScraperBase):
    

    @abstractmethod
    async def get_product(self) -> AsyncGenerator[Product]:
        pass
