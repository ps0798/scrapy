import httpx
from bs4 import BeautifulSoup
from typing import List, Optional
import os
import asyncio
from utilities.helper import extract_price_from_rupees
from Storage.json_store import JSONStorage
from constants import JSON_FILE_PATH

class Scraper:
    def __init__(self, base_url: str, proxy: Optional[str] = None):
        self.base_url = base_url
        self.proxy = proxy
        self.fetched_data = []
        self.storage = JSONStorage(file_path=JSON_FILE_PATH)
        self.previous_data = self.storage.load_data()
        self.cache = { k: v for k,v in self.previous_data.items() }

    async def fetch_page(self, url: str, retries=5, RETRY_DELAY=5) -> Optional[str]:
        attempt = 0
        while attempt < retries:
            try:
                async with httpx.AsyncClient(proxies=self.proxy) as client:
                    response = await client.get(url, timeout=10)
                    response.raise_for_status()
                    return response.text
            except (httpx.RequestError, httpx.HTTPStatusError) as exc:
                print(f"Error fetching {url}: {exc}. Retrying in {RETRY_DELAY} seconds...")
                attempt += 1
                await asyncio.sleep(RETRY_DELAY)
        print(f"Failed to fetch {url} after {retries} retries.")

    def parse_page(self, html: str) -> List[dict]:
        soup = BeautifulSoup(html, "html.parser")
        products = []

        shop_content = soup.find('div', id='mf-shop-content')
        if not shop_content:
            return []
        
        product_list = shop_content.select('ul', class_='products')
        if not product_list:
            return products
        
        product_list = product_list[0]
        items = product_list.find_all('li', class_='product')
        for item in items:
            title_tag = item.find('h2', class_='woo-loop-product__title')
            product_title = title_tag.get_text().strip() if title_tag else 'N/A'

            price_tag = item.find('span', class_='woocommerce-Price-amount')
            product_price = price_tag.get_text().strip() if price_tag else 'N/A'
            
            image_tag = item.find('img')
            image_url = image_tag['src'] if image_tag else 'N/A'
            if 'data-lazy-src' in image_tag.attrs:
                image_url = image_tag['data-lazy-src']

            if self.cache.get("product_title") and self.cache.get("price") == extract_price_from_rupees(product_price):
                # skipping because data is already existing 
                continue

            products.append({
                "product_title": product_title,
                "product_price": product_price,
                "path_to_image": image_url,
                "price": extract_price_from_rupees(product_price)
            })
        self.fetched_data = products
        return products

    async def scrape(self, skip_index_in_first_page=None, page_limit: int = 5) -> List[dict]:
        all_products = []
        for page_num in range(1, page_limit + 1):
            if page_num == 1 and skip_index_in_first_page:
                url = f"{self.base_url}"
            else:
                url = f"{self.base_url}/page/{page_num}"
            html = await self.fetch_page(url)
            if html:
                products = self.parse_page(html)
                all_products.extend(products)
            await asyncio.sleep(1)
        return all_products
    
    async def shut_down(self):
        await self.storage.save_data(self.fetched_data)
