"""
Script de scraping para extração de dados dos livros.
Execute este script para coletar e salvar os dados localmente.
"""
from infrastructure.scraper import scrape_books

def main():
    print('Script de scraping inicial')
    books = scrape_books()
    print(f'Foram coletados {(books)} livros.')

    for book in books[:3]:
        print(book)


if __name__ == '__main__':
    main()