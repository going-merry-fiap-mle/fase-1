"""
Módulo de web scraping.
Implemente aqui a lógica para extrair dados de fontes externas.
"""

import os
import logging
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

load_dotenv()
def scrape_books():
    options = webdriver.FirefoxOptions()
    if os.environ.get("FLASK_ENV", "dev") != "dev":
        options.add_argument("--headless")
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

    url = "https://books.toscrape.com/"
    driver.get(url)

    books_data = []

    while True:
        books = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")

        for book in books:
            title = book.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").get_attribute("title")
            price = book.find_element(By.CLASS_NAME, "price_color").text
            rating = book.find_element(By.CSS_SELECTOR, "p.star-rating").get_attribute("class").replace("star-rating", "").strip()
            availability = book.find_element(By.CSS_SELECTOR, "p.instock.availability").text.strip()
            img_url = book.find_element(By.TAG_NAME, "img").get_attribute("src")

            book_link = book.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").get_attribute("href")

            driver.get(book_link)
            category = driver.find_element(By.CSS_SELECTOR, "ul.breadcrumb li:nth-child(3) a").text

            driver.back()

            books_data.append({
                "title": title,
                "price": price,
                "rating": rating,
                "availability": availability,
                "category": category,
                "image": img_url
            })

            logging.info(f"Book {title} scraped successfully")
       
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "li.next > a")
            next_page_url = next_button.get_attribute("href")
            driver.get(next_page_url)
        except NoSuchElementException:
            break  

    driver.quit()
    return books_data


