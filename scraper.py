import requests
from abrev import *
from itertools import groupby
from bs4 import BeautifulSoup as bs

def main():
    response = requests.get('https://obituarios.curitiba.pr.gov.br/publico/falecimentos.aspx')
    if response.status_code != 200:
        print('ERRO: Página não disponível! Abortando...')
        quit()
    html = response.text

    soup = bs(html, 'html.parser')
    table = soup.find('table')
    
    items = table.find_all('tr')
    items = [i.text.strip().replace('\n', ' ') for i in items]
    print(groupby(items, lambda z: z == ''))
    people = [list(y) for x,y in groupby(items, lambda z: z == '') if not x]
    
    for p in people:
        for i in p:
            phrase = ': '.join([w.strip() for w in i.split(':', 2)])
            words = phrase.split(' ')
            words = [w.lower() if w.lower() in preposicoes else w.capitalize() for w in words] 
            phrase = ' '.join(words)
            phrase = phrase.replace('Ano(s)', 'anos')
            print(phrase)
        print()

if __name__ == '__main__':
    main()
