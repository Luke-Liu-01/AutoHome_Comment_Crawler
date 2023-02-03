import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
import json


def get_target_url():
    # 读取各品牌对应的标签
    if os.path.exists('car_brands.json') is False:
        print('Please run pre_get_car_brands.py first')
        return
    if os.path.exists('all_series.json') is False:
        all_series = {}
    else:
        a = open('all_series.json', 'r', encoding='utf-8')
        all_series = json.load(a)
        a.close()
    f = open('car_brands.json', 'r', encoding='utf-8')
    car_brands = json.load(f)
    f.close()
    url = 'https://k.autohome.com.cn/#pvareaid=3311255'
    brower = webdriver.Chrome()
    time.sleep(3)
    brower.get(url)
    brower.find_element_by_class_name('select-selected').click()
    time.sleep(2)
    for key in car_brands:
        if key in all_series.keys() and all_series[key]:
            continue
        brower.find_element_by_class_name(car_brands[key]).click()
        time.sleep(1)

        page = brower.page_source
        soup = BeautifulSoup(page, 'html.parser')
        series_list = soup.find('div', class_='selectpop-box-prov').find_next_sibling().find_all('a')
        cur_car_series = {}
        for series in series_list:
            series_name = series.get_text()
            series_href = 'https://k.autohome.com.cn{}'.format(series.get('href'))
            cur_car_series[series_name] = series_href
        print(cur_car_series)
        all_series[key] = cur_car_series
    brower.quit()
    try:
        store = json.dumps(all_series, ensure_ascii=False)
        f = open('all_series.json', 'w', encoding='utf-8')
        f.write(store)
        f.close()
        print('Successfully!')
    except Exception as e:
        print('Something is wrong!\nThe error message: ' + e)


if __name__ == '__main__':
    get_target_url()
