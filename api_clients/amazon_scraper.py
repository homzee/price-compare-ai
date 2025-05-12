from bs4 import BeautifulSoup
import requests

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def search_amazon(keyword):
    url = f"https://www.amazon.co.jp/s?k={requests.utils.quote(keyword)}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    results = []

    for item in soup.select('.s-result-item'):
        name_tag = item.select_one('h2 a span')
        price_tag = item.select_one('.a-price-whole')
        link_tag = item.select_one('h2 a')
        if name_tag and price_tag and link_tag:
            results.append({
                "平台": "Amazon",
                "商品名": name_tag.text.strip(),
                "价格": f"¥{price_tag.text.strip()}",
                "链接": f"https://www.amazon.co.jp{link_tag['href']}"
            })
        if len(results) >= 5:
            break
    return results
