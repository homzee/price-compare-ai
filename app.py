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
        df = pd.DataFrame(all_results)

        if "价格" in df.columns and not df.empty:
            try:
                df["价格_数值"] = df["价格"].str.replace("¥", "").str.replace(",", "").astype(float)
                df = df.sort_values("价格_数值")
                st.success(f"共获取 {len(df)} 条结果（已按价格升序排列）")
                st.dataframe(df.drop(columns="价格_数值"), use_container_width=True)
            except Exception as e:
                st.warning(f"⚠️ 排序时发生错误：{e}")
                st.dataframe(df, use_container_width=True)
        else:
            st.warning("❗未能抓取包含价格的数据，请检查关键词或平台状态。")
