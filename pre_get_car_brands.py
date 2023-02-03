import time
from bs4 import BeautifulSoup
from selenium import webdriver
import json


def get_car_brands():
    url = 'https://k.autohome.com.cn/#pvareaid=3311255'
    brower = webdriver.Chrome()
    brower.get(url)
    brower.find_element_by_class_name('select-selected').click()

    time.sleep(1)

    page = brower.page_source
    soup = BeautifulSoup(page, 'html.parser')
    brower.quit()
    car_brands = {}
    car_list = soup.find('div', class_='selectpop-cont-main prov-width-01').find_all('a')
    for car in car_list:
        car_name = car.get_text()
        car_class = car.get('class')[1]  # 用class属性定位只能用单属性，即唯一性的属性
        car_brands[car_name] = car_class
    try:
        store = json.dumps(car_brands, ensure_ascii=False)
        f = open('car_brands.json', 'w', encoding='utf-8')
        f.write(store)
        f.close()
        print('Successfully!')
    except Exception as e:
        print('Something is wrong!\nThe error message: ' + e)


if __name__ == '__main__':
    get_car_brands()
