from lib import scraper
import requests
from tqdm import tqdm
import time
from bs4 import BeautifulSoup
import pandas as pd


URL = "https://race.netkeiba.com/?pid=schedule"
BASE_URL = "https://race.netkeiba.com"

# main > div > div.schedule_select_cond > form > select:nth-child(3)


def Scraper(url):
    return url


def race_urls(year: int, month: int):
    # その年のレースの結果のページのurlを取得する。
    payload = {
        "pid": "schedule",
        "select": "schedule",
        "year": year,
        "month": month
    }
    resp = requests.post(URL, data=payload)

    bs = BeautifulSoup(resp.content, "lxml")
    tables = bs.find_all("table", class_="race_table_01")
    table = []
    if month:
        table = tables[1]
    else:
        table = tables[0]
    res = []
    objects = table.find_all("td", class_="txt_l")
    for obj in objects:
        try:
            url = obj.find("a").get("href")
            if url[0] == "/":
                res.append(BASE_URL + url)
            else:
                res.append(BASE_URL + "/" + url)
        except AttributeError:
            continue
    return res


def trans_result_page(mid_url):
    # 中間ページから結果のページのurlを取得る
    html = requests.get(mid_url)
    html_contents = html.content
    html_soup = BeautifulSoup(html_contents, "html.parser")
    try:
        url = html_soup.find_all(class_='racebtn')[1].find_all('li')[
            3].find('a').get("href")
        return BASE_URL + url
    except AttributeError:
        return "None"


def scraper_data(year: int):
    # year年の重賞レースの結果をスクレイピングして、三次元配列に保存する。
    urls = race_urls(year, "")  # その年の重賞レースの結果の中間URLnoリスト
    time.sleep(1)
    res = []
    for url in tqdm(urls):
        result_url = trans_result_page(url)  # レース結果のページのurlを取得
        time.sleep(1)
        if result_url == "None":
            res.append([])
        else:
            result = scraper.scraper_keiba_net(result_url)
            res.append(result)

    return res


if __name__ == "__main__":
    # res = scraper_data(2018)
    # df = pd.DataFrame(res)
    # df.to_csv("data.csv", encoding="utf_8")
    results = []
    for year in range(2009, 2018):
        print("scraping of", year)
        res = scraper_data(year)
        results.append(res)
    df = pd.DataFrame(results)
    df.to_csv("data.csv", encoding="utf_8")
