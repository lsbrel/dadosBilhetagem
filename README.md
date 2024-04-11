# Scripts de Extração de Dados de Sistema Legado Web

Este repositório contém scripts desenvolvidos em Python para extrair dados de um sistema legado baseado na web. Os scripts utilizam as bibliotecas `requests` e `urllib2` para realizar requisições HTTP e extrair informações das páginas HTML do sistema legado. Os dados extraídos são posteriormente processados e salvos em um outro banco de dados para fins de análise ou migração.

## Funcionalidades Principais

- **Extração de Dados**: Os scripts são capazes de realizar requisições HTTP para o sistema legado e extrair informações específicas das páginas HTML, como texto, links, tabelas, etc.

- **Processamento de Dados**: Após a extração, os dados podem passar por processamentos adicionais, como limpeza, formatação ou transformações específicas, para prepará-los para o próximo estágio.

- **Armazenamento em Banco de Dados**: Os dados extraídos e processados são salvos em um banco de dados, seja ele relacional (como MySQL, PostgreSQL) ou não relacional (como MongoDB), para posterior análise ou integração com outros sistemas.

## Tecnologias Utilizadas

- **Python**: A linguagem de programação principal utilizada para desenvolver os scripts de extração de dados.

- **Bibliotecas Python**: Os scripts fazem uso de bibliotecas como `requests` e `urllib2` para realizar requisições HTTP e `Beautiful Soup` para analisar e extrair dados das páginas HTML.


## Contribuição

Contribuições são bem-vindas! Se você tiver ideias para melhorar os scripts existentes, adicionar novas funcionalidades ou corrigir problemas, sinta-se à vontade para abrir uma issue ou enviar um pull request para o repositório.

## Recursos Adicionais

- [Documentação da biblioteca requests](https://docs.python-requests.org/en/latest/)
- [Documentação da biblioteca BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
