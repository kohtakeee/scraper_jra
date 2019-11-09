import requests
from bs4 import BeautifulSoup


def scraper_keiba_net(url):

    # このurlは2019/02/17(日)のフェブラリーステークス(G1)のレース結果です。
    res = requests.get(url)
    html_doc = res.content
    soup = BeautifulSoup(html_doc, 'html.parser')

    # webページの上段を獲得する
    div_house_detail = soup.find('dl', class_='racedata')

    # レース名を獲得する
    race_name = div_house_detail.find('h1')
    print("\n" + race_name.get_text().replace(u"\xa0", u""))

    # コースの距離と種類を獲得する
    race_detail = div_house_detail.find('p')
    print(race_detail.get_text().replace("\xa0", ""))

    # コースの状態と天気と時間
    race_detail = div_house_detail.find_all('p')

    for rd in race_detail:
        headers = []
        headers.append(rd.text)

    for header in headers:
        print(header.replace("\xa0", ""))

    # リストを使ってレース結果を保存する
    results = []

    res_tables = soup.find_all('table', class_='race_table_01')

    for table in res_tables:
        headers = []
        # rows = table.find_all('tr')
        # まず、フィールド名を決めるために、最初の行からヘッダーセルを獲得する
        for header in table.find('tr').find_all('th'):
            headers.append(header.text)

        # 一番最初の行に
        # results.append(headers)
       # つぎに、1行目以外の行を処理する

        for row in table.find_all('tr')[1:]:
            values = []
            for col in row.find_all(['th', 'td']):
                values.append(col.text)
            if values:
                result_dict = [values[i] for i in
                               range(len(values))]

                results.append(result_dict)

    return results
# 結果を表示
# for result in results:
#    print(result)
