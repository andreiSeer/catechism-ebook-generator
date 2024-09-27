# catechism-ebook-generator
# Catechism eBook Generator

Um gerador de eBooks que transforma o Catecismo da Igreja Católica em um formato EPUB, permitindo acesso fácil e organizado ao conteúdo.

## Descrição

Este projeto coleta o conteúdo do Catecismo da Igreja Católica diretamente do site oficial do Vaticano e gera um arquivo EPUB. O eBook resultante contém uma tabela de conteúdos e navegação para facilitar a leitura. É uma ferramenta útil para quem deseja acessar o Catecismo de forma digital e portátil.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação utilizada.
- **Requests**: Biblioteca para realizar requisições HTTP.
- **BeautifulSoup**: Biblioteca para fazer parsing de HTML.
- **EbookLib**: Biblioteca para criar e manipular arquivos EPUB.

## Instalação

Para utilizar o projeto, siga os passos abaixo:

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/catechism-ebook-generator.git
   cd catechism-ebook-generator
2. **Instale as dependências:**
  É recomendado utilizar um ambiente virtual. Você pode criar um ambiente virtual e instalar as dependências usando pip:
   ```bash
    python -m venv venv
    source venv/bin/activate  # Para Linux/Mac
    venv\Scripts\activate     # Para Windows
    pip install -r requirements.txt
## Uso
Para gerar o eBook, execute o seguinte comando:
```bash
  python generate_ebook.py
