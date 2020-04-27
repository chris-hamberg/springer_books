import pandas as pd
import lxml.html
import os, sys
import requests


xlsx = 'Free+English+textbooks.xlsx'
xfile = pd.ExcelFile(xlsx)
df = xfile.parse()


if not os.path.exists('Books'):
    os.mkdir('Books')
elif not os.path.isdir('Books'):
    print('Error: a file named "Books" cannot be in the execution directory.')
    sys.exit(0)


class Book:


    def __init__(self, idx, title, edition, subject, url):
        self.idx     = idx
        self.title   = title
        self.edition = edition
        self.name    = f'{self.title}, {self.edition}'
        self.subject = self.process(subject)
        self.url     = url
        self.epub    = None


    def __repr__(self):
        return f'{self.idx}: {self.title}, {self.edition} [{self.subject}]'


    def process(self, subject):

        subject = subject.split(';')[0]

        try:
            os.mkdir(os.path.join('Books', subject))
        except FileExistsError:
            pass
        finally:
            self.path = os.path.join('Books', subject, self.name + '.pdf')
            self.epat = os.path.join('Books', subject, self.name + '.epub')

        return subject


    def scrape(self):

        if os.path.exists(self.path) and os.path.exists(self.epat):
            print(f'Info: {self.path} already saved.')
            print(f'Info: {self.epat} already saved.')
            self.save = lambda: 0
            return 0

        response = requests.get(self.url)
        html  = lxml.html.fromstring(response.content)
        epub  = None
        try:
            xpath = html.xpath(
                '//*[@id="main-content"]/article[1]/div/div/div[2]/div/div/a'
                )
            if not bool(xpath):
                xpath = html.xpath(
                    '//*[@id="main-content"]/article[1]/div/div/div[2]/div[1]/a'
                    )
                epub  = html.xpath(
                    '//*[@id="main-content"]/article[1]/div/div/div[2]/div[2]/a'
                    )
                epub = epub[0]

            xpath = xpath[0]

        except IndexError:
            print(
                f'Error: {self.idx} {self.name} server access point missing'
                 )
            self.save = lambda: 0
            return False

        else:

            stub  = xpath.get('href')
            pdf   = f'https://link.springer.com/{stub}'
            self.pdf  = requests.get(pdf).content

            if epub:
                stub = epub.get('href')
                epub = f'https://link.springer.com/{stub}'
                self.epub = requests.get(epub).content


    def save(self):


        if self.pdf and not os.path.exists(self.path):
            with open(self.path, 'wb') as fhand:
                fhand.write(self.pdf)
            print(f'Saved: {self.path}')
        elif not self.pdf:
            print(f'Info: Springer does not furnish this as pdf.')
        else:
            print(f'Info: {self.path} already saved.')


        if self.epub and not os.path.exists(self.epat):
            with open(self.epat, 'wb') as fhand:
                fhand.write(self.epub)
            print(f'Saved: {self.epat}')
        elif not self.epub:
            print(f'Info: Springer does not furnish this as epub.')
        else:
            print(f'Info: {self.epat} already saved.')



for idx, row in df.iterrows():
    book = Book(idx, 
                df['Book Title'].iloc[idx], 
                df['Edition'].iloc[idx], 
                df['Subject Classification'].iloc[idx],
                df['OpenURL'].iloc[idx])
    print('\n', book)
    book.scrape()
    book.save()
    print('\n')
