# -*- coding: utf-8 -*-
import json
# ここからスクレイピング必要分
from bs4 import BeautifulSoup
import urllib.request
import re
# ここからseleniumでブラウザ操作必要分
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep   # 新しくインポート
import datetime

# ここからflaskの必要分
import os
from flask import Flask

# ここからflaskでcorsの設定 ajaxを使う時のクロスドメイン制約用
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return """
    使い方 : /api/<記事リストのURL> /n
    <記事リストのURL>には　"entrylist?url="　以降を入力する
    """


@app.route('/api/<list_url>')  # list_urlは記事一ページのURL
def slide(list_url):
    # list_urlにはXXXで渡されるため、元のURLに戻す
    string_1 = re.compile("XXX")
    string_2 = re.compile("X$")
    url = string_1.sub("%3A%2F%2F", list_url)
    url = string_2.sub("%2F", url)
    URL = "http://b.hatena.ne.jp/entrylist?url=" + str(url)
    print(URL)

    html = urllib.request.urlopen(URL).read()
    data_list = []  # 全ページのデータを集める配列

    soup = BeautifulSoup(html, "html.parser")
    articles = soup.select("div.entrylist-contents-main")

    for article in articles:
        article_in = {}
        title = article.a.get("title")
        article_URL = article.a.get("href")
        bookmark_num = article.find("a", class_="js-keyboard-entry-page-openable").span.string
        bookmark_URL = "http://b.hatena.ne.jp" + article.find("a", class_="js-keyboard-entry-page-openable").get("href")
        contents_date = article.find("li", class_="entrylist-contents-date").string

        article_in["title"] = title
        article_in["article_URL"] = article_URL
        article_in["bookmark_num"] = bookmark_num
        article_in["bookmark_URL"] = bookmark_URL
        article_in["contents_date"] = contents_date

        data_list.append(article_in)

    jsonstring = json.dumps(data_list, ensure_ascii=False,
                            indent=2)  # 作った配列をjson形式にして出力する
    return jsonstring


@app.route('/api/test/<url>')  # list_urlは記事一ページのURL
def test(url):
    string_3 = re.compile("Z")
    string_4 = re.compile("XXX")
    string_5 = re.compile("YYY")
    URL = string_3.sub("%", url)
    URL = string_4.sub("://", URL)
    URL = string_5.sub("/", URL)
    print("ちゃんと動く")
    return URL


@app.route('/api/bookmark/<bookmark_url>')  # list_urlは記事一ページのURL
def bookmark(bookmark_url):
    string_3 = re.compile("Z")
    string_4 = re.compile("XXX")
    string_5 = re.compile("YYY")
    url = string_3.sub("%", bookmark_url)
    url = string_4.sub("://", url)
    URL = string_5.sub("/", url)

    # ブラウザのオプションを格納する変数をもらってきます。
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path="/Users/shingo/webdriver/chromedriver", chrome_options=options)

    print("ここまで")

    # URLを開いてから3秒待機
    driver.get(URL)
    sleep(3)

    next = driver.find_element_by_class_name("entry-bookmarkUsers-readMore-btn")  # ブクマリストを開くボタンを取得
    button_actions = ActionChains(driver)
    button_actions.move_to_element(next)
    button_actions.perform()
    sleep(2)
    next.click()  # ボタンをクリック
    sleep(1)

    # １８番目のブクマがあるかの判定
    target = driver.find_elements_by_xpath(
        "//*[@id='container']/div/div[2]/div[2]/section[2]/div[2]/div/div/div[1]/div[18]")
    if len(target) > 0:
        actions = ActionChains(driver)
        actions.move_to_element(target[0])
        actions.perform()
        sleep(2)

    # ブックマークしているユーザーをとる
    data = driver.page_source.encode('utf-8')  # ページ内の情報をutf-8で用意する
    soup = BeautifulSoup(data, "html.parser")
    bookmark_users = []

    users = soup.find_all("span", class_="entry-comment-username")
    for user in users:
        bookmark_user_in = {}
        name = user.a.string
        user_url = "http://b.hatena.ne.jp" + user.a.get("href")

        bookmark_user_in["name"] = name
        bookmark_user_in["user_url"] = user_url
        bookmark_users.append(bookmark_user_in)

    driver.close()
    driver.quit()

    jsonstring = json.dumps(bookmark_users, ensure_ascii=False,
                            indent=2)  # 作った配列をjson形式にして出力する
    return jsonstring



# bashで叩いたかimportで入れたかを判定する
if __name__ == '__main__':
    app.run()
