import requests
from bs4 import BeautifulSoup

URL = "https://race.netkeiba.com/?pid=schedule"
BASE_URL = "https://race.netkeiba.com"


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


if __name__ == "__main__":
    ans = race_urls(2018, "")
    print(ans)
