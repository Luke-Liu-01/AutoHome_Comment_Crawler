import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import random
import pre_get_car_brands
import pre_get_target_url


def get_data(series, url, car, brower):
    # 如果已经存在了此车系数据，就不用重新获取了
    if os.path.exists('data/{}/{}.txt'.format(car, series)):
        return
    fl = open('data/{}/{}.txt'.format(car, series), 'a+', encoding='utf-8')
    # 这个死循环是当汽车之家辨别出我是爬虫的时候，自动进行等待时间重新获取
    while True:
        brower.get(url)
        time.sleep(3)
        try:
            brower.find_element_by_class_name('first-close').click()  # 关掉“发表质量评价”
        except Exception as e:
            pass
        page = brower.page_source
        bs = BeautifulSoup(page, 'html.parser')
        try:
            categories = bs.find('div', class_='cont-first').find_all('a')
            break
        except Exception as e:
            time.sleep(90)
    for i in range(3, len(categories)):
        url = 'https://k.autohome.com.cn{}'.format(categories[i].get('href'))
        category = categories[i].get_text().strip()  # 口碑类别
        brower.get(url)
        sed1 = random.randint(2, 5)
        time.sleep(sed1)
        page = brower.page_source
        bs = BeautifulSoup(page, 'html.parser')
        try:
            tags = bs.find('div', class_='revision-suspend').find_all('a')
            tags.pop(0)  # 剔除 “全部”
            for i in range(len(tags)):
                url = 'https://k.autohome.com.cn{}'.format(tags[i].get('href'))
                tag = tags[i].get_text().split('(')[0]  # 标签
                evaluate = 1 if 'dust' not in tags[i].get('class') else -1  # 正面: 1  负面: -1
                brower.get(url)
                sed2 = random.randint(2, 5)
                time.sleep(sed2)
                while True:
                    page = brower.page_source
                    bs = BeautifulSoup(page, 'html.parser')
                    mouthcons = bs.find_all('div', class_='mouthcon')

                    for mouthcon in mouthcons:
                        textcon = mouthcon.find('div', class_='text-con')
                        [s.extract() for s in textcon("div")]
                        text = textcon.get_text().strip()
                        str_list = [series, category, tag, str(evaluate), text]
                        strs = ";".join(str_list)
                        fl.write(strs + '\n')
                        print('车系：' + series + '；类别：' + category + '；标签：' + tag + '；正负面评估：' + str(evaluate) + '；内容：' + text)
                    next_page = bs.find_all('a', class_='page-disabled page-item-next')
                    if len(next_page) == 0:
                        try:
                            ck = brower.find_element_by_class_name('page-item-next')
                            ck.click()
                            time.sleep(1)
                        except BaseException:
                            break
                    else:
                        break
        except Exception as e:  # 没有标签的情况
            while True:
                page = brower.page_source
                bs = BeautifulSoup(page, 'html.parser')
                mouthcons = bs.find_all('div', class_='mouthcon')
                for mouthcon in mouthcons:
                    textcon = mouthcon.find('div', class_='text-con')
                    [s.extract() for s in textcon("div")]
                    [s.extract() for s in textcon("script")]
                    text = textcon.get_text().strip()
                    str_list = [series, category, "", str(0), text]  # 没有标签的情况，正负面未知，设为0
                    strs = ";".join(str_list)
                    fl.write(strs + '\n')
                    print('车系：' + series + '；类别：' + category + '；标签：' + '' + '；正负面评估：' + str(0) + '；内容：' + text)
                next_page = bs.find_all('a', class_='page-disabled page-item-next')
                if len(next_page) == 0:
                    try:
                        ck = brower.find_element_by_class_name('page-item-next')
                        ck.click()
                        time.sleep(1)
                    except BaseException:
                        break
                else:
                    break
    fl.close()


def pre_doing_something():
    """
    预处理操作：必须保证生成car_brands.json和all_series.json文件。
    优化思想：要想将运行时的时间尽量缩短，一种策略就是预处理的数据更加完善，增加这两个文件的目的就在于此。
    比如如果要是想要获取宝马的车系评论，没必要在运行的时候去获取哪些车系，可以将其存在all_series.json中，
    因为这部分数据其实是有限的，这样就减少了一次打开浏览器的操作。
    """
    if not os.path.exists('car_brands.json'):
        pre_get_car_brands.get_car_brands()
        time.sleep(2)
    if not os.path.exists('all_series.json'):
        pre_get_target_url.get_target_url()
        time.sleep(2)
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists('data/xlsx'):
        os.makedirs('data/xlsx')


if __name__ == "__main__":
    pre_doing_something()
    car_brands = ['奔驰']
    f = open('all_series.json', 'r', encoding='utf-8')
    car_series = json.load(f)
    f.close()
    brower = webdriver.Chrome()
    for car in car_brands:
        cur = car_series[car]
        if not os.path.exists('data/' + car):
            os.makedirs('data/' + car)
        for series, url in cur.items():
            get_data(series, url, car, brower)
    brower.quit()
