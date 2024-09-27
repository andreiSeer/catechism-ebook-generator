import os
import requests
from bs4 import BeautifulSoup
from ebooklib import epub

BASE_URL = "https://www.vatican.va"
PAGE_URL = f"{BASE_URL}/archive/cathechism_po/index_new/prima-pagina-cic_po.html"
OUTPUT_FOLDER = "catechism_pages"
OUTPUT_FILE = 'catecismo.epub'
WIDTHS_TO_REPLACE = ["609", "599", "598"]

def create_epub_book():
    """Cria e configura o livro EPUB"""
    book = epub.EpubBook()
    book.set_title('Catecismo da Igreja Católica')
    book.set_language('pt')
    book.add_author('Vaticano')
    return book

def fetch_page_content(url):
    """Faz a requisição HTTP e retorna o conteúdo HTML"""
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')

def clean_page_content(soup):
    """Remove imagens e ajusta larguras das tabelas"""
    for img in soup.find_all('img'):
        img.decompose()
    
    for width in WIDTHS_TO_REPLACE:
        for tag in soup.find_all(attrs={"width": width}):
            tag['width'] = "100%"  # Ajusta a largura
    
    return soup

def extract_chapter_title(soup, chapter_count):
    """Extrai o título do capítulo ou cria um título padrão"""
    if soup.title and soup.title.string:
        return f"{chapter_count} - {soup.title.string}"
    
    meta_title = soup.find('meta', attrs={'name': 'title'})
    if meta_title and 'content' in meta_title.attrs:
        return f"{chapter_count} - {meta_title['content']}"
    
    return f"{chapter_count} - Título não informado"

def extract_content_table(soup):
    """Extrai a segunda tabela de conteúdo da página, se existir"""
    tables = soup.find_all("table")
    return str(tables[1]) if len(tables) > 1 else None

def process_links(links, book):
    """Processa os links e retorna os capítulos EPUB"""
    visited_pages = set()
    chapters = []
    content_list = []
    chapter_count = 1

    for link in links:
        href = link.get('href')
        if href and not href.startswith("/") and ".html" in href:
            full_url = f"{BASE_URL}/archive/cathechism_po/index_new/{href}"
        else:
            continue

        if full_url in visited_pages:
            continue

        visited_pages.add(full_url)

        try:
            page_soup = clean_page_content(fetch_page_content(full_url))
            content_table_html = extract_content_table(page_soup)
            
            if not content_table_html or content_table_html in content_list:
                continue

            content_list.append(content_table_html)
            title = extract_chapter_title(page_soup, chapter_count)

            chapter = epub.EpubHtml(title=title, file_name=f'chapter_{chapter_count}.xhtml', lang='pt')
            chapter.content = content_table_html
            book.add_item(chapter)
            chapters.append(chapter)

            chapter_count += 1

        except Exception as e:
            print(f"Erro ao acessar {full_url}: {e}")

    return chapters

def save_epub(book, chapters):
    """Salva o livro EPUB com os capítulos fornecidos"""    
    book.toc = (chapters)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ['nav'] + chapters
    epub.write_epub(OUTPUT_FILE, book)
    print(f'EPUB salvo como {OUTPUT_FILE}')


def main():   
    
    soup = fetch_page_content(PAGE_URL)
    links = soup.find_all('a')
    
    book = create_epub_book()
    
    chapters = process_links(links, book)
    save_epub(book, chapters)

if __name__ == "__main__":
    main()
