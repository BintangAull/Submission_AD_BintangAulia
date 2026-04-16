import streamlit as st
import pandas as pd

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

st.title("📊 E-Commerce Customer Dashboard")
st.write("Analisis RFM & Geospatial")

#load data
rfm = pd.read_csv('./data/rfm_data.csv')
city = pd.read_csv('./data/city_summary.csv')

col1, col2, col3 = st.columns(3)

col1.metric("Total Customer", rfm.shape[0])
col2.metric("Total Revenue", int(rfm['monetary'].sum()))
col3.metric("Avg Spending", int(rfm['monetary'].mean()))


segment_counts = rfm['segment'].value_counts()

st.subheader("📊 Customer Segment Distribution")

st.bar_chart(segment_counts)


st.subheader("🔥 Top VIP Customers")

vip = rfm[rfm['segment'] == '🔥 VIP Customer']
st.dataframe(vip.head(10))

st.subheader("🌍 Top Cities by Customers")

top_city = city.sort_values(by='total_customers', ascending=False).head(10)

st.dataframe(top_city)

st.subheader("🗺️ Customer Distribution Map")

city_map = city.rename(columns={'lng': 'lon'})

st.map(city_map[['lat', 'lon']].dropna())

segment_option = st.selectbox(
    "Pilih Segment",
    rfm['segment'].unique()
)

filtered = rfm[rfm['segment'] == segment_option]

st.dataframe(filtered.head(20))