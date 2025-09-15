

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def scrape_daraz(query, max_pages=1):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")   # keep background mode for API
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    data = []

    for page in range(1, max_pages + 1):
        url = f"https://www.daraz.pk/catalog/?q={query}&page={page}"
        print(f"Scraping page {page}: {url}")
        driver.get(url)
        time.sleep(4)

        # Find product anchors
        products = driver.find_elements(By.XPATH, "//a[contains(@href, '/products/')]")
        print(f"  Found {len(products)} products")

        for product in products:
            title = product.get_attribute("title")
            link = product.get_attribute("href")
            if link and link.startswith("//"):
                link = "https:" + link

            price, rating = "", ""
            try:
                container = product.find_element(By.XPATH, "./ancestor::div[contains(@class,'gridItem')]")
                try:
                    price = container.find_element(By.XPATH, ".//span[contains(@class,'currency')]").text
                except:
                    pass
                try:
                    rating = container.find_element(By.XPATH, ".//span[contains(@class,'rating')]").text
                except:
                    pass
            except:
                pass

            if title and link:
                data.append({
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "link": link,
                    "page": page
                })

    driver.quit()
    return data


# # server.py# scraper.py
# import requests
# from bs4 import BeautifulSoup

# def scrape_daraz(query, page=1):
#     url = f"https://www.daraz.pk/catalog/?q={query}&page={page}"
#     headers = {"User-Agent": "Mozilla/5.0"}
#     r = requests.get(url, headers=headers)

#     soup = BeautifulSoup(r.text, "html.parser")

#     products = []
#     for item in soup.select(".box--pRqdD"):  # may need adjustment
#         title = item.select_one(".title--wFj93")
#         price = item.select_one(".price--NVB62")
#         if title and price:
#             products.append({
#                 "title": title.get_text(strip=True),
#                 "price": price.get_text(strip=True)
#             })

#     return products
