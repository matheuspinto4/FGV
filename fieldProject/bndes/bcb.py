from bs4 import BeautifulSoup
import requests


def get_normativo(numero_normativo):
    url = f"https://www.bcb.gov.br/api/conteudo/app/normativos/exibeoutrasnormas?p1=COMUNICADO&p2={numero_normativo}"
    headers = {
    "Host": "www.bcb.gov.br",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Connection": "keep-alive",
    "Referer": f"https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Comunicado&numero={numero_normativo}",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    }
    page = requests.get(url, headers=headers)
    conteudo_lei = BeautifulSoup(page.json()['conteudo'][0]['Texto'], 'lxml')
    texto_lei = conteudo_lei.get_text(separator='\n', strip=True)

    return texto_lei
    