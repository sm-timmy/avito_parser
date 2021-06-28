import os, traceback, sys
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pandas
from pandas import ExcelWriter
import openpyxl
import time
import psycopg2
from sqlalchemy import create_engine
import datetime




def fullparse(search_, min_price_, max_price_, pagecount_):
        try:
                search = str(search_)
                min_price=str(min_price_)
                max_price=str(max_price_)
                pagecount=str(pagecount_)
                print("Parser started!\n")
                print("search "+ search)
                print("min_price "+ min_price)
                print("max_price "+ max_price)
                print("pagecount "+ pagecount)
                today=datetime.date.today()
                today=str(today)
                url = 'https://www.avito.ru'

                headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
                }

                today=str(today + "_" + search)
                print(today)
                resp = requests.get(url, headers=headers, params={'bt': 1, 'pmax': max_price, 'pmin': min_price, 'q': search, 's': '2', 'view': 'gallery'})
                print('Ссылка со всеми параметрами:\n', resp.url)
                print(resp.status_code)
                soup = BeautifulSoup(resp.text, 'lxml')

                h12 = soup.h1.get_text()

                try:
                    str1 = soup.find('span', {'data-marker': 'pagination-button/next'}).previous_element
                except:
                    str1 = 1

                #print(f'Категория: {h12}\nКоличество страниц: {str1}')

                pagination = int(pagecount_)


                data = []
                my_city = resp.url.replace('https://www.avito.ru/', '').split('?')[0]
                print('Мой город:', my_city)

                for page in range(1, pagination + 1):
                    response = requests.get(url, headers=headers, params={'bt': 1, 'p': page, 'pmax': max_price, 'pmin': min_price, 'q': search, 's': '2', 'view': 'gallery'})
                    soup = BeautifulSoup(response.text, 'lxml')
                    blocks = soup.find_all('div', class_='iva-item-root-G3n7v')
                    
                    for block in blocks:
                
                        if my_city == block.find('a', class_='link-link-39EVK').get('href').split('/')[1]:
                            data.append({
                                "title": block.find('h3', class_='title-root-395AQ').get_text(strip=True),
                                'price': block.find('span', class_='price-text-1HrJ_').get_text(strip=True).replace('₽', '').replace(' ', ''),
                                'city': block.find('a', class_='link-link-39EVK').get('href').split('/')[1],
                                'district': block.find('div', class_='geo-root-1pUZ8').get_text(strip=True),
                                'link': url + block.find('a', class_='link-link-39EVK').get('href'),
                                'time' : block.find('div', class_='date-text-2jSvU').get_text(strip=True),
                            })
                    time.sleep(1)
                    #print(f'Парсинг страницы {page} из {pagination}')

                #print(f'Количество собранных позиций по городу "{my_city}": {len(data)}')



                dataframe = pandas.DataFrame(data)
                newdataframe = dataframe.rename(columns={
                    'title': 'Наименование', 'price': 'Цена, ₽',
                    'link': 'Ссылка', 'city': 'Город', 'district': 'Район', 'time': 'Время'
                })


                engine = create_engine('postgresql://postgres:password@localhost:5432/parseravito')
                newdataframe.to_sql(today, index=False, con=engine)
                return resp.url
                
        except:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

def getpages(search_, min_price_, max_price_):
        try:
                search = str(search_)
                min_price=str(min_price_)
                max_price=str(max_price_)
                print("Parser started!\n")
                print("search "+ search)
                print("min_price "+ min_price)
                print("max_price "+ max_price)
                #print("pagecount "+ pagecount)
                today=datetime.date.today()
                today=str(today)
                url = 'https://www.avito.ru'

                headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
                }

                today=str(today + "_" + search)
                print(today)
                resp = requests.get(url, headers=headers, params={'bt': 1, 'pmax': max_price, 'pmin': min_price, 'q': search, 's': '2', 'view': 'gallery'})
                print('Ссылка со всеми параметрами:\n', resp.url)
                print(resp.status_code)
                soup = BeautifulSoup(resp.text, 'lxml')

                h12 = soup.h1.get_text()

                try:
                    str1 = soup.find('span', {'data-marker': 'pagination-button/next'}).previous_element
                    print("1pages\n" + str1)
                    return str1
                except:
                    str1 = 1

                #print(f'Категория: {h12}\nКоличество страниц: {str1}')
                
                pagecount =1
                pagination = int(pagecount)


                data = []
                my_city = resp.url.replace('https://www.avito.ru/', '').split('?')[0]
                print('Мой город:', my_city)

                for page in range(1, pagination + 1):
                    response = requests.get(url, headers=headers, params={'bt': 1, 'p': page, 'pmax': max_price, 'pmin': min_price, 'q': search, 's': '2', 'view': 'gallery'})
                    soup = BeautifulSoup(response.text, 'lxml')
                    blocks = soup.find_all('div', class_='iva-item-root-G3n7v')
                    
                    for block in blocks:
                
                        if my_city == block.find('a', class_='link-link-39EVK').get('href').split('/')[1]:
                            data.append({
                                "title": block.find('h3', class_='title-root-395AQ').get_text(strip=True),
                                'price': block.find('span', class_='price-text-1HrJ_').get_text(strip=True).replace('₽', '').replace(' ', ''),
                                'city': block.find('a', class_='link-link-39EVK').get('href').split('/')[1],
                                'district': block.find('div', class_='geo-root-1pUZ8').get_text(strip=True),
                                'link': url + block.find('a', class_='link-link-39EVK').get('href'),
                                'time' : block.find('div', class_='date-text-2jSvU').get_text(strip=True),
                            })
                    time.sleep(1)
                    #print(f'Парсинг страницы {page} из {pagination}')

                #print(f'Количество собранных позиций по городу "{my_city}": {len(data)}')



                dataframe = pandas.DataFrame(data)
                newdataframe = dataframe.rename(columns={
                    'title': 'Наименование', 'price': 'Цена, ₽',
                    'link': 'Ссылка', 'city': 'Город', 'district': 'Район', 'time': 'Время'
                })


                engine = create_engine('postgresql://postgres:password@localhost:5432/parseravito')
                newdataframe.to_sql(today, index=False, con=engine)
                
                
        except:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)



                    

                    