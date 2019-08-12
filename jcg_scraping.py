# -*- coding: utf-8 -*-
import os.path
import time
import re
import copy
import threading
import setting
from scrapy.http import HtmlResponse
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


def init():
    #Selenium初期化
    options = ChromeOptions()
    options.add_argument('--headless')
    return Chrome(options=options)

def close(driver):
    #Selenium終了
    driver.quit()

def move_page(driver,url):
    #指定されたURLまでWebページを移動する
    driver.get(url)
    time.sleep(3)

def jcg_entry_page_get(driver):
    #jcgのエントリーページ取得
    number_of_participants = driver.find_elements_by_class_name('ng-binding')[0].text
    now_participant_number = driver.find_elements_by_class_name('sort-id')[-1].text
    while number_of_participants != now_participant_number:
        now_participant_number = driver.find_elements_by_class_name('sort-id')[-1].text
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

def jcg_class_urls_parser(driver):
    #パーサーでクラスURLを抽出
    soup = BeautifulSoup(driver.page_source, "html5lib")
    class_img = soup.select("div.jcgcore_content td.decks img")
    class_urls = []
    for img in class_img:
        class_urls.append(img["src"])
    return class_urls

def jcg_class_counter(class_urls):
    #クラスのURLからそれぞれのクラスの出場数を抽出
    class_dict = {
                    "1":["エルフ",0],
                    "2":["ロイヤル",0],
                    "3":["ウィッチ",0],
                    "4":["ドラゴン",0],
                    "5":["ネクロマンサー",0],
                    "6":["ヴァンパイア",0],
                    "7":["ビショップ",0],
                    "8":["ネメシス",0]
                }
    for decks in class_urls:
        num = re.sub("\\D", "", decks)
        class_dict[num][1] += 1
    return class_dict

def get_deck_dictionary(driver):
    #デッキ内容を辞書で抽出
    deck_dict = {}
    soup = BeautifulSoup(driver.page_source, "html5lib")
    classes = soup.select("div.el-card-list-info")
    for data in classes:
        name = data.select("span.el-card-list-info-name-text")[0].text
        count = re.sub("\\D", "",data.select("span.el-card-list-info-count")[0].text)
        deck_dict[name] = count
    return deck_dict

def dictionary_marge(card_dictionary,deck_dictionary):
    #deck_dictionaryをcard_dictionaryに統合する
    for k,v in deck_dictionary.items():
        if k in card_dictionary:
            card_dictionary[k] += int(v)
        else:
            card_dictionary[k] = int(v)

def get_card_dictionary(driver,class_urls):
    #card_dictionaryを取得する
    card_dictionary = {}
    class_img = driver.find_elements_by_css_selector("div.jcgcore_content td.decks img")
    for i,img in enumerate(class_img):
        print(f"\r{i}ページ目",end="")
        img.click()
        driver.switch_to.window(driver.window_handles[1])
        deck_dictionary = get_deck_dictionary(driver)
        dictionary_marge(card_dictionary,deck_dictionary)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    print("")
    return card_dictionary

def print_class_dictionary(class_dictionary):
    #class_dictionaryのコンソールへの出力
    print("参加クラス数")
    for k,v in class_dictionary.items():
        print(v[0],":",v[1])

def print_card_dictionary(card_dictionary):
    #card_dictionaryのコンソールへの出力
    print("カード種類数")
    for k,v in card_dictionary.items():
        print(k,":",v)

def print_card_csv(card_dictionary,class_dictionary):
    #csvにスクレイピングした情報を出力する
    path = setting.CARD_DATA_OUTPUT_FILE_NAME
    with open(path, mode='w',encoding='utf-8') as f:
        for k,v in card_dictionary.items():
            f.write(f"{k},{v}\n")

    path = setting.CLASS_DATA_OUTPUT_FILE_NAME
    with open(path, mode='w',encoding='utf-8') as f:
        for k,v in class_dictionary.items():
            f.write(f"{v[0]},{v[1]}\n")


