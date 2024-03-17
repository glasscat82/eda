""" eda.yandex.ru """
import sys, time, json
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from help import *
from art import tprint


def get_pagen(browser, *args):
    time.sleep(0.5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)

    return True

def get_selenium_driver():
    """ start selenium driver """
    service = Service(executable_path='/usr/local/bin/geckodriver')
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--incognito")
    options.headless = True    
    driver = webdriver.Chrome(options=options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol
        '''
    })

    driver.maximize_window()
    return driver

def get_html(driver, url, pg = None):
    """_"""
    driver.get(url)
    time.sleep(0.5)
    html = False

    try:
        ''' Этот код будет ждать 10 секунд до того, как отдаст исключение TimeoutException или если найдет элемент за эти 10 секунд, то вернет его. 
        WebDriverWait по умолчанию вызывает ExpectedCondition каждые 500 миллисекунд до тех пор, пока не получит успешный return. 
        Успешный return для ExpectedCondition имеет тип Boolean и возвращает значение true, либо возвращает not null для всех других ExpectedCondition типов. '''
        element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.TAG_NAME, "footer"))
        )

        last_height = driver.execute_script("return document.body.scrollHeight") 
        while True: 
            # прокрутка вниз 
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
            # пауза, пока загрузится страница. 
            time.sleep(1)
            # вычисляем новую высоту прокрутки и сравниваем с последней высотой прокрутки. 
            new_height = driver.execute_script("return document.body.scrollHeight") 
            if new_height == last_height:
                # сохраняем и завершаем
                html = driver.page_source
                wtf(html, pg = f'_{pg}')
                pcolor("[+] прокрутка завершена")
                break
            
            last_height = new_height
            pcolor("[*] появился новый контент, прокручиваем дальше", 3)

    except Exception as e:
        pcolor(f'[-] errorf: {sys.exc_info()[1]}', color_num=1)
    
    return html

def get_links(html):
    ''' '''
    soup = BeautifulSoup(html, 'lxml')
    result_body = soup.find('body', {})

    r = []
    for h2 in result_body.find_all('h2', {"class":"PlaceList_title"}):
        """ list restaurant only """
        n0 = h2.text.strip()

        if n0 == 'Все рестораны':
            hp = h2.parent.parent
            ul = hp.find('ul')
            for item in ul.find_all('div', {'class':'PlaceListBduItem_placesListItem'}):
                i_name = item.find('h3', {'class':'NewPlaceItem_title'})
                i_url = item.find('a')
                i_img = item.find('img',{'class':'NewPlaceItem_image'})
                i_rating = item.find('div',{'class':'NewPlaceItem_metaWrapper'})

                row = {}
                row['name'] = i_name.text.strip()
                row['title'] = i_name.get('title')
                row['url'] = i_url.get('href')
                row['img'] = i_img.get('src')
                row['rating'] = i_rating.get('aria-label').strip()
                r.append(row)

            break

    return r

if __name__ == "__main__":
    """_@_@_"""    
    city = ['spb', 'moscow', 'Chita', 'novosibirsk', 'kaliningrad']
    code_region = city[1]
    url = f'https://eda.yandex.ru/{code_region}?shippingType=delivery'

    tprint(f'eda - {code_region}', font='cybermedium', sep='\n')

    # ------------------------
    driver = get_selenium_driver()
    html = get_html(driver, url, code_region)

    # html = lf(f'./html/html_{code_region}.txt')
    eda_data = get_links(html)
    write_json(eda_data, f'./json/{code_region}.json')

    # -------------------------
    pcolor(f'[+] всего загруженно: {len(eda_data)}')

