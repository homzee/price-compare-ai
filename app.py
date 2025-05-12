import streamlit as st
from api_clients.amazon_scraper import search_amazon
from api_clients.rakuten_scraper import search_rakuten
from api_clients.yahoo_scraper import search_yahoo
import pandas as pd

st.set_page_config(page_title="🛍 AI 比价工具", layout="wide")
st.title("📦 多平台商品比价工具")
st.markdown("输入你想搜索的商品，我将为你抓取 Amazon、Rakuten 和 Yahoo! 的实时价格信息。")

keyword = st.text_input("🔍 请输入商品关键词：", value="iPhone 13")
search_btn = st.button("搜索")

if search_btn and keyword:
    with st.spinner("正在爬取价格数据，请稍候..."):
        amazon = search_amazon(keyword)
        rakuten = search_rakuten(keyword)
        yahoo = search_yahoo(keyword)
        all_results = amazon + rakuten + yahoo
        df = pd.DataFrame(all_results).sort_values("价格", key=lambda x: x.str.replace("¥", "").str.replace(",", "").astype(float))
        st.success(f"共获取 {len(df)} 条结果")
        st.dataframe(df, use_container_width=True)
