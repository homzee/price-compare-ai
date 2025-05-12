from bs4 import BeautifulSoup
import requests

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def search_rakuten(keyword):
    url = f"https://search.rakuten.co.jp/search/mall/{requests.utils.quote(keyword)}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    results = []

    for item in soup.select('.searchresultitem'):
        name_tag = item.select_one('.title')
        price_tag = item.select_one('.important')
        link_tag = item.select_one('a')
        if name_tag and price_tag and link_tag:
            results.append({
                "平台": "Rakuten",
                "商品名": name_tag.text.strip(),
                "价格": price_tag.text.strip(),
                "链接": link_tag['href']
            })
        if len(results) >= 5:
            break
    return results
