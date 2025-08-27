from bs4 import BeautifulSoup
import requests

def get_normativo(numero_normativo):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Connection": "keep-alive",
    }

    url = f"https://www.planalto.gov.br/ccivil_03/_Ato2023-2026/2025/Decreto/D{numero_normativo}.htm"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'lxml')
    texto_lei = soup.get_text(separator='\n', strip=True)

    return texto_lei




