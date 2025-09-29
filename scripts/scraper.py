"""
Script de scraping para extração de dados dos livros.
Execute este script para coletar e salvar os dados localmente.
"""
import sys
import os
import logging
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from infrastructure.scraper import scrape_books

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def main():
    logging.info("Scraping script started")
    books = scrape_books()
    logging.info(f"{len(books)} books were collected.")

    for book in books[:3]:
        logging.info(f"Book details: {book}")


if __name__ == '__main__':
    main()