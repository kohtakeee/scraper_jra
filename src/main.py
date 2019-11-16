# %%
from lib.scraper import scraper_keiba_net
import requests
from tqdm import tqdm
import time
from bs4 import BeautifulSoup
import pandas as pd
import sys
from typing import List

URL = "https://race.netkeiba.com/?pid=schedule"
BASE_URL = "https://race.netkeiba.com"


class Scraper:
    def __init__(self):
        self.data = []

    def get_data(self):
        """dataを取得するメソッド."""
        return self.data

    def save_data(self, file_name: str):
        """指定されたファイル名でdataを保存するメソッド."""
        df = pd.DataFrame(self.data)
        df.to_csv(file_name + ".csv", encoding="utf_8")

    def scraping_2014(self):
        """"２０１４年のレース結果をスクレイピングするメソッド."""
        target_2014 = [
            [[1, 8], [2, 6]],  # 札幌競馬場のレースの情報　[[第何回, 何日]]
            [[1, 6], [2, 6]],  # 函館競馬場のレースの情報　[[第何回, 何日]]
            [[1, 6], [2, 8], [3, 6], [4, 4]],  # 福岡競馬場のレースの情報[　[[第何回, 何日]]
            [[1, 8], [2, 12], [3, 8]],  # 新潟競馬場のレースの情報　[[第何回, 何日]]
            [[1, 8], [2, 12], [3, 8], [4, 9], [5, 9]],  # 東京競馬場のレースの情報　[[第何回, 何日]]
            [[1, 9], [2, 8], [3, 8], [4, 8]],  # 中山競馬場のレースの情報　[[第何回, 何日]]
            [[1, 4], [2, 6], [3, 8], [4, 6]],  # 中京競馬場のレースの情報　[[第何回, 何日]]
            [[1, 9], [2, 8], [3, 12], [4, 9], [5, 9]],  # 京都競馬場のレースの情報　[[第何回, 何日]]
            [[1, 8], [2, 8], [3, 8], [4, 8], [5, 8]],  # 阪神競馬場のレースの情報　[[第何回, 何日]]
            [[1, 8], [2, 12]]  # 小倉競馬場のレースの情報　[[第何回, 何日]]
        ]

        self.scraping(target_2014, 2014)

    def scraping_2011(self):
        """"２０１１年のレース結果をスクレイピングするメソッド."""
        target_2011 = [
            [[1, 8], [2, 8]],  # 札幌競馬場のレースの情報　[[第何回, 何日]]
            [[1, 8], [2, 8]],  # 函館競馬場のレースの情報　[[第何回, 何日]]
            [],  # 福島競馬場のレースの情報[　[[第何回, 何日]]

            # 新潟競馬場のレースの情報　[[第何回, 何日]]
            [[1, 10], [2, 6], [3, 8], [4, 8], [5, 12]],
            [[1, 8], [2, 8], [3, 8], [4, 9], [5, 8]],  # 東京競馬場のレースの情報　[[第何回, 何日]]
            [[1, 8], [2, 4], [3, 8], [4, 8], [5, 8]],  # 中山競馬場のレースの情報　[[第何回, 何日]]
            [],  # 中京競馬場のレースの情報　[[第何回, 何日]]
            [[1, 8], [2, 8], [3, 12], [4, 8], [5, 8],
                [6, 8]],  # 京都競馬場のレースの情報　[[第何回, 何日]]
            [[1, 8], [2, 8], [3, 4], [4, 4], [5, 8],
                [6, 8]],  # 阪神競馬場のレースの情報　[[第何回, 何日]]
            # 小倉競馬場のレースの情報　[[第何回, 何日]]
            [[1, 8], [2, 12], [3, 2], [4, 12], [5, 10]]
        ]
        self.scraping(target_2011, 2011)

    def scraping(self, target: List[List[int]], year: int):
        """特定の年のレース結果をスクレイピングするメソッド."""
        # 10個のの開催場所
        for i, days in tqdm(enumerate(target)):
            spot = i + 1
            self.spot_scraping(year, spot, days)

    def spot_scraping(self, year: int, spot: int, days: List[List[int]]):
        """spot: 競馬場, 第何回とレース何日めのペアの配列を受け取る."""
        for pair in tqdm(days):
            assert len(pair) == 2, "length of pair is not 2."
            siries = pair[0]
            races = pair[1]
            self.race_scraping(year, spot, siries, races)

    def race_scraping(self, year: int, spot: int, siries: int, races: int):
        """spot: 競馬場, siries: 第何回、race:何日目、 レーススクレイピングする."""
        for race in tqdm(range(races)):
            url = BASE_URL + "/?pid=race&id=c" + \
                str(year) + str(spot).zfill(2) + \
                str(siries).zfill(2) + str(race+1).zfill(2) + "11&mode=result"
            print(url + "\n")
            if siries == 1 and spot == 9 and race + 1 == 6:
                continue
            else:
                time.sleep(1)
                res = scraper_keiba_net(url)
                time.sleep(1)
                self.data.append(res)


if __name__ == "__main__":

    year = sys.argv[1]
    scp = Scraper()
    if year == "2014":
        scp.scraping_2014()
    elif year == "2011":
        scp.scraping_2011()

    scp.save_data("sample_" + year)

# %%
