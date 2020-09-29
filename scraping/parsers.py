from bs4 import BeautifulSoup
from random import randint
import requests
import codecs


__all__ = ('work_ua', 'rabota_ua', 'dou_ua', 'djinni_co')

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:48.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/46.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/43.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:51.0) Gecko/20100101 Firefox/45.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9*/*;q=0.8'},
]


def work_ua(url, location=None, specialty=None):
    response = requests.get(url, headers=headers[randint(0, 4)])
    domain = 'https://www.work.ua'
    jobs, errors = [], []
    if url:
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            main_div = soup.find('div', id='pjax-job-list')

            if main_div:
                list_div = main_div.find_all('div', attrs={'class': 'job-link'})
                for div in list_div:
                    title = div.find('h2')
                    link = title.a['href']
                    description = div.p.text
                    company = 'No name'
                    company_name = div.find('img')
                    if company_name:
                        company = company_name['alt']
                    jobs.append({'url': domain+link,
                                 'title': title.text,
                                 'company': company,
                                 'description': description,
                                 'location_id': location,
                                 'specialty_id': specialty})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})
    else:
        errors.append({'url': url, 'title': 'URL do not response'})
    return jobs, errors


def rabota_ua(url, location=None, specialty=None):
    response = requests.get(url, headers=headers[randint(0, 4)])
    domain = 'https://rabota.ua'
    jobs, errors = [], []

    if url:
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', id='ctl00_content_vacancyList_gridList')

            if table:
                list_tr = table.find_all('tr', attrs={'id': True})
                for tr in list_tr:
                    div = tr.find('div', attrs={'class': 'card-body'})
                    if div:
                        title = div.find('p', attrs={'class': 'card-title'})
                        link = title.a['href']
                        description = div.p.text
                        company = 'No name'
                        company_name = div.find('p', attrs={'class':
                                                            'company-name'})
                        if company_name:
                            company = company_name.a.text
                        jobs.append({'url': domain+link,
                                     'title': title.text,
                                     'company': company,
                                     'description': description,
                                     'location_id': location,
                                     'specialty_id': specialty})
            else:
                errors.append({'url': url, 'title': 'Table does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})
    else:
        errors.append({'url': url, 'title': 'URL do not response'})
    return jobs, errors


def dou_ua(url, location=None, specialty=None):
    response = requests.get(url, headers=headers[randint(0, 4)])
    jobs, errors = [], []

    if url:
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            main_div = soup.find('div', id='vacancyListId')

            if main_div:
                list_li = main_div.find_all('li', attrs={'class': 'l-vacancy'})
                for li in list_li:
                    if '__hot' not in li['class']:
                        title = li.find('div', attrs={'class': 'title'})
                        link = title.a['href']
                        company_description = li.find('div', attrs={'class':
                                                                    'sh-info'})
                        description = company_description.text
                        company = 'No name'
                        company_name = title.find('a', attrs={'class':
                                                              'company'})
                        if company_name:
                            company = company_name.text
                        jobs.append({'url': link,
                                     'title': title.text,
                                     'company': company,
                                     'description': description,
                                     'location_id': location,
                                     'specialty_id': specialty})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})
    else:
        errors.append({'url': url, 'title': 'URL do not response'})
    return jobs, errors


def djinni_co(url, location=None, specialty=None):
    response = requests.get(url, headers=headers[randint(0, 4)])
    domain = 'https://djinni.co'
    jobs, errors = [], []

    if url:
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            main_ul = soup.find('ul', attrs={'class': 'list-jobs'})

            if main_ul:
                list_li = main_ul.find_all('li', attrs={'class':
                                                        'list-jobs__item'})
                for li in list_li:
                    title = li.find('div', attrs={'class': 'list-jobs__title'})
                    link = title.a['href']
                    company_description = li.find(
                        'div', attrs={'class': 'list-jobs__description'})
                    description = company_description.text
                    company_name = li.find(
                        'div', attrs={'class': 'list-jobs__details__info'})
                    company = 'No name'
                    if company_name:
                        company = company_name.text
                    jobs.append({'url': domain+link,
                                 'title': title.text,
                                 'company': company,
                                 'description': description,
                                 'location_id': location,
                                 'specialty_id': specialty})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})
    else:
        errors.append({'url': url, 'title': 'URL do not response'})
    return jobs, errors
