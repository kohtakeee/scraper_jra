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


# その年のレース一覧を取得する
def race_urls(year: int, month: int):
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
    for url in map(lambda x: x.a.get("href"), table.find_all("td", class_="txt_l")):
        if url[0] == "/":
            res.append(BASE_URL + url)
        else:
            res.append(BASE_URL + "/" + url)

    return res

# 中間ページから結果のページのurlを取得る


def trans_result_page(mid_url):
    html = requests.get(mid_url)
    html_contents = html.content
    html_soup = BeautifulSoup(html_contents, "html.parser")
    url = html_soup.find_all(class_='racebtn')[1].find_all('li')[
        3].find('a').get('href')
    return BASE_URL + url


if __name__ == "__main__":
    urls = race_urls(2018, "")
    # for url in urls:
    # print(url)

    url_target = "https://race.netkeiba.com/?pid=special&id=0124"
    url = trans_result_page(url_target)
    print(url)
# #main > div.GradeRace_Area > div > div.RaceNavi_Box.fc > div.Right_Box > div > ul:nth-child(2) > li:nth-child(4) > a
