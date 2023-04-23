import time
from selenium import webdriver as wb_noproxy
from random import choice
from seleniumwire import webdriver as wb_proxy
import json
import functools
import configparser
import requests
def func_time(func):
    @functools.wraps(func)
    def timer(*args, **kwargs):
        start = time.perf_counter()
        data = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'Время выполнения {func.__name__}: {round(end - start, 4)} сек')
        return data
    return timer
def proxies():
    with open('proxies.json', 'r', encoding='utf-8') as f:
        text = json.load(f)
    return text
def options(proxy: str, headless: str):
    if proxy.lower() == 'on':
        opt = wb_proxy.ChromeOptions()
        opt.add_argument('--start-maximized')
        with open('user_agent.txt', 'r', encoding='utf-8') as file:
            agents = [i.strip() for i in file.readlines()]
            user_agent = choice(agents)
            opt.add_argument(f'user-agent={user_agent}')
            file.close()
        if headless == 'on':
            opt.add_argument('--headless')
        opt.add_experimental_option("excludeSwitches", ["enable-logging"])
        return opt
    elif proxy.lower() == 'off':
        opt = wb_noproxy.ChromeOptions()
        opt.add_argument('--start-maximized')
        with open('user_agent.txt', 'r', encoding='utf-8') as file:
            agents = [i.strip() for i in file.readlines()]
            user_agent = choice(agents)
            opt.add_argument(f'user-agent={user_agent}')
            file.close()
        if headless == 'on':
            opt.add_argument('--headless')
        opt.add_experimental_option("excludeSwitches", ["enable-logging"])
        return opt

def api_json() -> list[str]:
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    api_key = config.get('program', 'api_key')
    search = input('Введите запрос для поиска организаций: ')
    print()
    print('Начат сбор ссылок\n')
    url = f'https://search-maps.yandex.ru/v1/?text={search}&type=biz&lang=ru_RU&results=2000&apikey={api_key}'

    resp = requests.get(url=url)
    resp = resp.json()
    data = (i['properties']['CompanyMetaData']['id'] for i in resp['features'])
    c = len([i['properties']['CompanyMetaData']['id'] for i in resp['features']])
    print(f'Найдено {c} ссылок.\n')
    return data