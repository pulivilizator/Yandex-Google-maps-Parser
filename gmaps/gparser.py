import re
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
from selenium.webdriver.common.action_chains import ScrollOrigin
from bs4 import BeautifulSoup
from options_gmap import options

def get_hrefs() -> list:
	data = []
	hrefs = []
	url = 'https://www.google.ru/maps/'
	with wb_noproxy.Chrome(options=options()) as browser:
		browser.get(url)
		time.sleep(3)
		try:
			browser.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button/span').click()
			time.sleep(5)
		except:
			pass
		browser.find_element(By.ID, 'searchboxinput').send_keys(input('Введите запрос'))
		browser.find_element(By.ID, 'searchbox-searchbutton').click()
		time.sleep(5)
		while True:
			for i in browser.find_element(By.CLASS_NAME, 'm6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd').find_elements(By.CLASS_NAME, 'Nv2PK'):
				if i not in data:
					data.append(i)
			elem = browser.find_element(By.CLASS_NAME, 'm6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd')

			element = ScrollOrigin(origin=elem, x_offset=0, y_offset=0)
			ActionChains(browser).move_to_element(elem).scroll_from_origin(scroll_origin=element, delta_x=0,
																		   delta_y=800).perform()
			print(len(data))
			if 'Больше результатов нет.' in browser.page_source:
				ActionChains(browser).move_to_element(elem).scroll_from_origin(scroll_origin=element, delta_x=0,
																			   delta_y=500).perform()
				for i in browser.find_element(By.CLASS_NAME, 'm6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd').find_elements(By.CLASS_NAME, 'Nv2PK.tH5CWc.THOPZb'):
					if i not in data:
						data.append(i)
				ActionChains(browser).move_to_element(elem).scroll_from_origin(scroll_origin=element, delta_x=0,
																			   delta_y=500).perform()
				for i in browser.find_element(By.CLASS_NAME, 'm6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd').find_elements(
						By.CLASS_NAME, 'Nv2PK.tH5CWc.THOPZb'):
					if i not in data:
						data.append(i)
				break
		for i in data:
			hrefs.append(i.find_element(By.TAG_NAME, 'a').get_attribute('href'))
		print(len(hrefs))
		return hrefs

def parser(hrefs):
	with wb_noproxy.Chrome(options=options()) as browser:
		for i in hrefs:
			adress, site, mobile, code = '', '', '', ''
			browser.get(i)
			time.sleep(3)
			data = browser.find_element(By.ID, 'QA0Szd').find_elements(By.CLASS_NAME, 'RcCsl.fVHpi.w4vB1d.NOE9ve.M0S7ae.AG25L')
			for k in data:
				try:
					aria = k.find_element(By.TAG_NAME, 'button').get_attribute('aria-label')

					if 'Адрес' in aria:
						adress = aria.split(':')[1].strip()
						print(adress, 'adress')
					if 'Телефон' in aria:
						mobile = aria.split(':')[1].strip()
						print(mobile, 'mobile')

					if 'Код Plus Code' in aria:
						code = aria.split(':')[1].strip()
						print(code, 'code')
				except Exception as ex:
					try:
						if 'Сайт' in k.find_element(By.TAG_NAME, 'a').get_attribute('aria-label'):
							site = k.find_element(By.TAG_NAME, 'a').get_attribute('href')
							print(site, 'site')
					except Exception as ex:
						print(ex, 'AAAAAAAAAAAAAAAA')
					continue
			with open('data.csv', 'a', encoding='utf-8-sig', newline='') as file:
				wrt = csv.writer(file, delimiter=';')
				f = adress, site, mobile, code, i
				wrt.writerow(f)


if __name__ == '__main__':
	with open('data.csv', 'w', encoding='utf-8-sig', newline='') as file:
		wrt = csv.writer(file, delimiter=';')
		wrt.writerow(['Адрес', 'Сайт', 'Телефон', 'Код Plus Code', 'Страница на Google Maps'])
	parser(get_hrefs())
