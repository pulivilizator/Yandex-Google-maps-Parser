import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import csv
import multiprocessing
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver as wb_proxy
from selenium import webdriver as wb_noproxy
from typing import NoReturn
import configparser
from options_yamaps import func_time, proxies, options, api_json

def pars(hrefs: list[str]) -> NoReturn:
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    a = int(multiprocessing.current_process().name.split('-')[1])
#
    cpu = multiprocessing.cpu_count()
    time.sleep(a * 2)

    if config.get('program', 'proxy') == 'on':
        proxy = proxies()
        with wb_proxy.Chrome(options=options(proxy=config.get('program', 'proxy'), headless=config.get('program', 'headless')),
                             service=ChromeService(ChromeDriverManager().install()), seleniumwire_options=proxy[a - 1]) as browser:
            for href in range(int(multiprocessing.current_process().name.split('-')[1]) - 1, len(hrefs), cpu):
                name, city, adress, ind, coord, site, number, vk, teleg, ok, wa, vb, yt, soc_contacts = '', '', '', '', '', '', '', '', '', '', '', '', '', ''
                browser.get(hrefs[href])
                #time.sleep(a / 4)
                print(browser.current_url)
                browser.implicitly_wait(5)
                if 'У вас старая версия браузера' in browser.page_source:
                    time.sleep(5)
                    browser.quit()
                    time.sleep(1)
                    browser = wb_proxy.Chrome(options=options(proxy=config.get('program', 'proxy'), headless=config.get('program', 'headless')),
                             service=ChromeService(ChromeDriverManager().install()), seleniumwire_options=proxy[a - 1])
                    continue
                try:
                    try:
                        element = WebDriverWait(browser, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'sidebar-container')))
                    except Exception as ex:
                        pass
                    name = [browser.find_element(By.CLASS_NAME, 'sidebar-container') \
                                .find_element(By.CLASS_NAME, 'orgpage-header-view__header').text]
                    try:
                        site = [browser.find_element(By.CLASS_NAME, 'sidebar-container') \
                                    .find_element(By.CLASS_NAME, 'business-urls-view__link').get_attribute('href')]
                    except Exception as ex:
                        site = ['']
                    try:
                        elem = browser.find_element(By.CLASS_NAME, 'sidebar-container').find_element(By.CLASS_NAME,
                                                                                                     'card-phones-view__more-wrapper')
                        ActionChains(browser).move_to_element(elem).perform()
                        elem.click()
                        elemm = browser.find_element(By.CLASS_NAME, 'sidebar-container') \
                            .find_element(By.CLASS_NAME, 'card-feature-view__additional') \
                            .find_element(By.CLASS_NAME, 'inline-image')
                        ActionChains(browser).move_to_element(elemm).perform()
                        elemm.click()
                        time.sleep(2)
                    except Exception as ex:
                        pass
                    try:
                        number = [i.text for i in browser.find_element(By.CLASS_NAME, 'sidebar-container') \
                            .find_elements(By.CLASS_NAME, 'card-phones-view__phone-number')]
                    except Exception as ex:
                        number = ['']
                    try:
                        soc_contacts = [i.find_element(By.TAG_NAME, 'a').get_attribute('href') \
                                        for i in browser.find_element(By.CLASS_NAME, 'sidebar-container') \
                                            .find_elements(By.CLASS_NAME, 'business-contacts-view__social-button')]
                        for seti in soc_contacts:
                            if 'vk.com' in seti:
                                vk = seti
                            elif 'ok.ru' in seti:
                                ok = seti
                            elif 't.me' in seti:
                                teleg = seti
                            elif 'youtube.com' in seti:
                                yt = seti
                            elif 'wa.me' in seti:
                                wa = seti
                            elif 'viber.click' in seti:
                                vb = seti

                    except Exception as ex:
                        soc_contacts = ['']
                    browser.get(browser.find_element(By.CLASS_NAME, 'sidebar-container') \
                                .find_element(By.CLASS_NAME, 'business-contacts-view__address-link').get_attribute(
                        'href'))
                    #time.sleep(1)
                    descr = browser.find_element(By.CLASS_NAME, 'sidebar-container') \
                        .find_element(By.CLASS_NAME, 'card-title-view__subtitle') \
                        .find_element(By.CLASS_NAME, 'toponym-card-title-view__description').text.split(',')
                    coord = browser.find_element(By.CLASS_NAME, 'sidebar-container') \
                        .find_element(By.CLASS_NAME, 'card-title-view__subtitle').find_element(By.CLASS_NAME,
                                                                                               'toponym-card-title-view__coords-badge').text
                    if descr[-1].strip().isdigit():
                        ind = descr[-1].strip()
                        city = descr[-2].strip()
                        adress = descr[:-2]
                    else:
                        ind = ''
                        city = descr[-1].strip()
                        adress = descr[:-1]

                    f = *name, city.strip(), ', '.join(adress).strip(), ind.strip(), coord.strip(), *site, '\n'.join(
                        number), \
                        vk.strip(), teleg.strip(), ok.strip(), wa.strip(), vb.strip(), yt.strip(), '\n'.join(
                        soc_contacts), browser.current_url
                    with open(f'{config.get("program", "path")}', 'a', encoding='utf-8-sig', newline='') as file:
                        writer = csv.writer(file, delimiter=';')
                        writer.writerow(f)
                except Exception as ex:
                    print(ex)
                    print('Произошла ошибка', browser.current_url)
                    continue
    elif config.get('program', 'proxy') == 'off':
        with wb_noproxy.Chrome(options=options(proxy=config.get('program', 'proxy'), headless=config.get('program', 'headless')),
                               service=ChromeService(ChromeDriverManager().install())) as browser:
            for href in range(int(multiprocessing.current_process().name.split('-')[1]) - 1, len(hrefs), cpu):
                name, city, adress, ind, coord, site, number, vk, teleg, ok, wa, vb, yt, soc_contacts = '', '', '', '', '', '', '', '', '', '', '', '', '', ''
                browser.get(hrefs[href])
                # time.sleep(a / 4)
                print(browser.current_url)
                browser.implicitly_wait(5)
                if 'У вас старая версия браузера' in browser.page_source:
                    time.sleep(5)
                    browser.quit()
                    time.sleep(1)
                    browser = wb_noproxy.Chrome(options=options(proxy=config.get('program', 'proxy'), headless=config.get('program', 'headless')),
                               service=ChromeService(ChromeDriverManager().install()))
                    continue
                try:
                    try:
                        element = WebDriverWait(browser, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'sidebar-container')))
                    except Exception as ex:
                        pass
                    name = [browser.find_element(By.CLASS_NAME, 'sidebar-container') \
                                .find_element(By.CLASS_NAME, 'orgpage-header-view__header').text]
                    try:
                        site = [browser.find_element(By.CLASS_NAME, 'sidebar-container') \
                                    .find_element(By.CLASS_NAME, 'business-urls-view__link').get_attribute('href')]
                    except Exception as ex:
                        site = ['']
                    try:
                        elem = browser.find_element(By.CLASS_NAME, 'sidebar-container').find_element(By.CLASS_NAME,
                                                                                                     'card-phones-view__more-wrapper')
                        ActionChains(browser).move_to_element(elem).perform()
                        elem.click()
                        elemm = browser.find_element(By.CLASS_NAME, 'sidebar-container') \
                            .find_element(By.CLASS_NAME, 'card-feature-view__additional') \
                            .find_element(By.CLASS_NAME, 'inline-image')
                        ActionChains(browser).move_to_element(elemm).perform()
                        elemm.click()
                        time.sleep(2)
                    except Exception as ex:
                        pass
                    try:
                        number = [i.text for i in browser.find_element(By.CLASS_NAME, 'sidebar-container') \
                            .find_elements(By.CLASS_NAME, 'card-phones-view__phone-number')]
                    except Exception as ex:
                        number = ['']
                    try:
                        soc_contacts = [i.find_element(By.TAG_NAME, 'a').get_attribute('href') \
                                        for i in browser.find_element(By.CLASS_NAME, 'sidebar-container') \
                                            .find_elements(By.CLASS_NAME, 'business-contacts-view__social-button')]
                        for seti in soc_contacts:
                            if 'vk.com' in seti:
                                vk = seti
                            elif 'ok.ru' in seti:
                                ok = seti
                            elif 't.me' in seti:
                                teleg = seti
                            elif 'youtube.com' in seti:
                                yt = seti
                            elif 'wa.me' in seti:
                                wa = seti
                            elif 'viber.click' in seti:
                                vb = seti

                    except Exception as ex:
                        soc_contacts = ['']
                    browser.get(browser.find_element(By.CLASS_NAME, 'sidebar-container') \
                                .find_element(By.CLASS_NAME, 'business-contacts-view__address-link').get_attribute(
                        'href'))
                    #time.sleep(1)
                    descr = browser.find_element(By.CLASS_NAME, 'sidebar-container') \
                        .find_element(By.CLASS_NAME, 'card-title-view__subtitle') \
                        .find_element(By.CLASS_NAME, 'toponym-card-title-view__description').text.split(',')
                    coord = browser.find_element(By.CLASS_NAME, 'sidebar-container') \
                        .find_element(By.CLASS_NAME, 'card-title-view__subtitle').find_element(By.CLASS_NAME,
                                                                                               'toponym-card-title-view__coords-badge').text
                    if descr[-1].strip().isdigit():
                        ind = descr[-1].strip()
                        city = descr[-2].strip()
                        adress = descr[:-2]
                    else:
                        ind = ''
                        city = descr[-1].strip()
                        adress = descr[:-1]

                    f = *name, city.strip(), ', '.join(adress).strip(), ind.strip(), coord.strip(), *site, '\n'.join(
                        number), \
                        vk.strip(), teleg.strip(), ok.strip(), wa.strip(), vb.strip(), yt.strip(), '\n'.join(
                        soc_contacts), browser.current_url
                    with open(f'{config.get("program", "path")}', 'a', encoding='utf-8-sig', newline='') as file:
                        writer = csv.writer(file, delimiter=';')
                        writer.writerow(f)
                except Exception as ex:
                    print(ex)
                    print('Произошла ошибка', browser.current_url)
                    continue
        browser.close()
        browser.quit()

if __name__ == '__main__':
    multiprocessing.freeze_support()

    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')

    cpu = multiprocessing.cpu_count()

    s = time.monotonic()

    with open(f'{config.get("program", "path")}', 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Регион', 'Адрес', 'Индекс', 'Координаты',
                         'Сайт', 'Номера', 'VK', 'TG', 'OK', 'WhatsApp', 'Viber', 'YouTube', 'Все социальные сети', 'Ссылка на Яндекс картах',
                         ])
        file.close()
    print(f'Создан файл по пути: {config.get("program", "path")}\nНе открывайте его до окончания работы программы\n')

    data = api_json()
    hrefs = list(map(lambda x: f'https://yandex.ru/maps/org/oldskul_pab/{x}', data))
    hrefs = [hrefs] * cpu
    print(hrefs)
    print('Начинаю сбор данных, ожидайте.\nВсе ссылки будут выводиться на экран, чтобы было видно, что работа идёт.\n')
    try:
        with multiprocessing.Pool(processes=cpu) as p:
            p.map(func=pars, iterable=(hrefs))
            p.close()
            p.join()
    except Exception as ex:
        pass
    e = time.monotonic()
    print('Работа завершена.\n')
    print(f'Время выполнения программы: {round(e - s, 4)}')
    time.sleep(99999)