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
        self.title   = self.fix(title)
        self.edition = edition
        self.name    = f'{self.title}, {self.edition}'
        self.subject = self.process(subject)
        self.url     = url
        self.pdf     = None
        self.epub    = None


    def __repr__(self):
        return f'{self.idx}: {self.title}, {self.edition} [{self.subject}]'


    def fix(self, title):
        return title.replace('/', '_')


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


    def check(self):

        if os.path.exists(self.path):
            print(f'Info: {self.path} already saved.')
            self.save_pdf = None

        if os.path.exists(self.epat):
            print(f'Info: {self.epat} already saved.')
            self.save_epub = None

        if os.path.exists(self.path) and os.path.exists(self.epat):
            self.scrape = lambda: 0
            self.save = lambda: 0


    def scrape(self):

        response = requests.get(self.url)
        html  = lxml.html.fromstring(response.content)
        pdf   = None
        epub  = None
        try:
            xpath = html.xpath(
                '//*[@id="main-content"]/article[1]/div/div/div[2]/div/div/a'
                )
            if not bool(xpath):
                pdf = html.xpath(
                    '//*[@id="main-content"]/article[1]/div/div/div[2]/div[1]/a'
                    )
                pdf = pdf[0]
                epub  = html.xpath(
                    '//*[@id="main-content"]/article[1]/div/div/div[2]/div[2]/a'
                    )
                epub = epub[0]
            else:
                xpath = xpath[0]
                if 'pdf' in xpath.get('href'):
                    pdf = xpath
                else:
                    epub = xpath

        except IndexError:
            print(
                f'Error: {self.idx} {self.name} server access point missing'
                 )
            self.save = lambda: 0
            return False

        else:
            if self.save_pdf and pdf:
                stub  = pdf.get('href')
                pdf   = f'https://link.springer.com/{stub}'
                self.pdf  = requests.get(pdf).content

            if self.save_epub and epub:
                stub = epub.get('href')
                epub = f'https://link.springer.com/{stub}'
                self.epub = requests.get(epub).content


    def save(self):

        if self.save_pdf:
            self.save_pdf()
        if self.save_epub:
            self.save_epub()


    def save_pdf(self):

        if not self.pdf:
            print(f'Info: Springer does not furnish this as pdf.')
        elif not os.path.exists(self.path):
            with open(self.path, 'wb') as fhand:
                fhand.write(self.pdf)
            print(f'Saved: {self.path}')


    def save_epub(self):

        if not self.epub:
            print(f'Info: Springer does not furnish this as epub.')
        elif self.epub and not os.path.exists(self.epat):
            with open(self.epat, 'wb') as fhand:
                fhand.write(self.epub)
            print(f'Saved: {self.epat}')



for idx, row in df.iterrows():
    book = Book(idx, 
                df['Book Title'].iloc[idx], 
                df['Edition'].iloc[idx], 
                df['Subject Classification'].iloc[idx],
                df['OpenURL'].iloc[idx])
    print('\n', book)
    book.check()
    book.scrape()
    book.save()
    print('\n')
