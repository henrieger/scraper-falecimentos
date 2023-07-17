import requests
from abrev import *
from itertools import groupby
from bs4 import BeautifulSoup as bs

def extract_attr(s: str):
    return s.split(':', 1)[1]

class Person(object):
    def __init__(self, attrs: list):
        self.name = extract_attr(attrs[0])
        self.date = extract_attr(attrs[1])
        self.age = extract_attr(attrs[2])
        self.job = extract_attr(attrs[3])
        self.father = extract_attr(attrs[4])
        self.mother = extract_attr(attrs[5])

        self.passing = extract_attr(attrs[-5])
        self.funeral = extract_attr(attrs[-4])
        self.burial = extract_attr(attrs[-3])
        self.burial_date = extract_attr(attrs[-2])

    def format_burial(self):
        burial_date = format_date(self.burial_date)
        burial_hour = format_hour(self.burial_date)
        burial_place = self.burial.strip()

        if burial_hour is None:
            return f'{burial_date}, {burial_place}'
        
        return f'{burial_date}, {burial_hour}, {burial_place}'

    def beautify(self):
        attrs = {
                'Nome': self.name,
                'Data': format_date(self.date),
                'Idade': self.age,
                'Profissão': self.job,
                'Filiação': self.father.strip() + ' e ' + self.mother.strip(),
                'Falecimento': self.passing,
                'Velório': self.funeral,
                'Sepultamento': self.format_burial()
            }
        return '\n'.join([a + ': ' + deabrev(capitalize(b.strip())) for a, b in attrs.items() if b.strip() != '' ])

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
    people = [list(y) for x,y in groupby(items, lambda z: z == '') if not x]
    
    for person in people:
        p = Person(person)
        print(p.beautify())
        print()

def capitalize(sentence: str):
            words = sentence.split(' ')
            
            words = [
                        w.lower() if w.lower() in preposicoes
                        else w.upper() if w in ['CIC', 'UPA']
                        else '('+(w.split('(')[-1].capitalize()) if len(w) and (w[0] == '(')
                        else w.capitalize()
                        for w in words
                    ] 

            words = [deabrev(w) for w in words]
            sentence = ' '.join(words)
            
            sentence = sentence.replace('Ano(s)', 'anos')
            
            sentence = sentence.replace('-pr', '-PR')
            sentence = sentence.replace('/pr', '/PR')
            sentence = sentence.replace(' - Pr', ' - PR')

            return sentence

def deabrev(word: str):
    if (len(word) == 0) or (word[-1] != '.') :
        return word

    if word[0] == '(':
        word = word[1:]

    return siglas.get(word[:-1], word.upper())

def format_date(sentence: str):
    tokens = sentence.split(', ')
    weekday = tokens[0].strip()
    month_day = tokens[1].split(' de ')[0]

    return f'{weekday} ({month_day})'

def format_hour(sentence: str):
    tokens = sentence.split(' às ')
    if len(tokens) <= 1: return None
    
    hour = tokens[1].split(':')
    return f'{hour[0]}h{hour[1][:-1] if hour[1] != "00h" else ""}'

if __name__ == '__main__':
    main()
