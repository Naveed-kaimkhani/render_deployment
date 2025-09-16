# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager

# def scrape_daraz(query, max_pages=1):
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless")   # run in background
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")

#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#     data = []

#     for page in range(1, max_pages + 1):
#         url = f"https://www.daraz.pk/catalog/?q={query}&page={page}"
#         print(f"Scraping page {page}: {url}")
#         driver.get(url)
#         time.sleep(4)

#         # Find product anchors
#         products = driver.find_elements(By.XPATH, "//a[contains(@href, '/products/')]")
#         print(f"  Found {len(products)} products")

#         for product in products:
#             title = product.get_attribute("title")
#             link = product.get_attribute("href")
#             if link and link.startswith("//"):
#                 link = "https:" + link

#             price, rating, image = "", "", ""
#             try:
#                 container = product.find_element(By.XPATH, "./ancestor::div[contains(@class,'gridItem')]")

#                 # Extract price
#                 try:
#                     price = container.find_element(By.XPATH, ".//span[contains(@class,'currency')]").text
#                 except:
#                     pass

#                 # Extract rating
#                 try:
#                     rating = container.find_element(By.XPATH, ".//span[contains(@class,'rating')]").text
#                 except:
#                     pass

#                 # Extract image
#                 try:
#                     img_tag = container.find_element(By.XPATH, ".//img")
#                     image = img_tag.get_attribute("src") or img_tag.get_attribute("data-src")
#                 except:
#                     pass

#             except:
#                 pass

#             if title and link:
#                 data.append({
#                     "title": title,
#                     "price": price,
#                     "rating": rating,
#                     "image": image,
#                     "link": link,
#                     "page": page
#                 })

#     driver.quit()
#     return data

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def scrape_daraz(query, max_pages=1):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    data = []

    for page in range(1, max_pages + 1):
        url = f"https://www.daraz.pk/catalog/?q={query}&page={page}"
        print(f"Scraping page {page}: {url}")
        driver.get(url)
        time.sleep(4)  # wait for JS to render

        # product cards (each <a> with product link)
        products = driver.find_elements(By.XPATH, "//a[contains(@href, '/products/')]")
        print(f"  Found {len(products)} products")

        for product in products:
            try:
                # Title
                title = product.get_attribute("title") or ""

                # Link
                link = product.get_attribute("href") or ""
                if link.startswith("//"):
                    link = "https:" + link

                # Image (avoid base64 placeholder)
                image = ""
                try:
                    img_elem = product.find_element(By.XPATH, ".//img[@type='product']")
                    image = img_elem.get_attribute("src") or ""
                    if image.startswith("data:image"):  # placeholder, check lazy-load
                        image = img_elem.get_attribute("data-src") or img_elem.get_attribute("srcset") or ""
                except:
                    pass

                # Price
                price = ""
                try:
                    price_elem = product.find_element(By.XPATH, ".//span[contains(@class, 'currency') or contains(@class, 'price')]")
                    price = price_elem.text.strip()
                except:
                    pass

                # Rating
                rating = ""
                try:
                    rating_elem = product.find_element(By.XPATH, ".//span[contains(@class, 'rating')]")
                    rating = rating_elem.text.strip()
                except:
                    pass

                data.append({
                    "title": title,
                    "link": link,
                    "price": price,
                    "rating": rating,
                    "image": image,
                    "page": page
                })
            except Exception as e:
                print("Error parsing product:", e)

    driver.quit()
    return data
