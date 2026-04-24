import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")
st.title("📊 E-Commerce Customer Dashboard")


# ─── CACHING DATA ──────────────────────────────────────────────
# @st.cache_data mencegah CSV dibaca ulang setiap rerun
@st.cache_data
def load_data():
    rfm = pd.read_csv('./data/rfm_data.csv')
    city = pd.read_csv('./data/city_summary.csv')
    product = pd.read_csv('./data/product_analysis.csv', index_col=0)
    revenue_yearly = pd.read_csv('./data/revenue_yearly.csv')
    satisfaction = pd.read_csv('./data/customer_satisfaction.csv')

    # Preprocess sekali saja di sini
    satisfaction['order_purchase_timestamp'] = pd.to_datetime(
        satisfaction['order_purchase_timestamp']
    )
    satisfaction['year'] = satisfaction['order_purchase_timestamp'].dt.year

    return rfm, city, product, revenue_yearly, satisfaction


rfm, city, product, revenue_yearly, satisfaction = load_data()

# ─── SECTION 1: PRODUCT PERFORMANCE ───────────────────────────
st.header("📦 Product Performance Analysis")
st.write("Distribusi Revenue, Contribution, dan Growth Kategori Produk")

st.subheader("🔎 Filter Data")

year_option = st.selectbox("Pilih Tahun", options=['All', 2016, 2017, 2018])
growth_option = st.multiselect(
    "Pilih Growth Category",
    options=product['growth_category'].unique(),
    default=product['growth_category'].unique()
)

# Filter revenue berdasarkan tahun
if year_option == 'All':
    filtered_revenue = revenue_yearly.groupby(
        'product_category_name_english'
    )['price'].sum()
else:
    filtered_revenue = revenue_yearly[
        revenue_yearly['year'] == year_option
        ].groupby('product_category_name_english')['price'].sum()

filtered_df = product.copy()
filtered_df['revenue'] = filtered_revenue
filtered_df = filtered_df.fillna(0)
filtered_df = filtered_df[filtered_df['growth_category'].isin(growth_option)]

# Top 10 Revenue
st.subheader("💰 Top 10 Product Categories by Revenue")
top10 = filtered_df.sort_values('revenue', ascending=False).head(10)
st.bar_chart(top10['revenue'])

# Growth Distribution
st.subheader("📊 Growth Distribution")
st.bar_chart(filtered_df['growth_category'].value_counts())

# Scatter Plot — data produk biasanya kecil, aman
st.subheader("📍 Contribution vs Growth Mapping")
chart = alt.Chart(filtered_df.reset_index()).mark_circle(size=80).encode(
    x='contribution_%',
    y='growth_%',
    color='growth_category',
    tooltip=['product_category_name_english', 'revenue']
).interactive()
st.altair_chart(chart, use_container_width=True)

# ─── SECTION 2: CUSTOMER SATISFACTION ─────────────────────────
st.header("😊 Customer Satisfaction Analysis")
st.write("Hubungan antara Harga, Waktu Pengiriman, dan Kepuasan Pelanggan")

st.subheader("🔎 Filter Data (Satisfaction)")
year_option_2 = st.selectbox(
    "Pilih Tahun (Satisfaction)", options=['All', 2016, 2017, 2018]
)

if year_option_2 == 'All':
    filtered_sat = satisfaction.copy()
else:
    filtered_sat = satisfaction[satisfaction['year'] == year_option_2]

# ── FIX UTAMA: Sampling untuk scatter plot besar ──────────────
# Scatter plot dengan >10k titik bikin browser lag & WebSocket putus
# Sample 2000 baris sudah cukup untuk melihat pola korelasi
MAX_SCATTER_POINTS = 2000


@st.cache_data
def sample_for_scatter(df, year, n=MAX_SCATTER_POINTS):
    """Cache hasil sampling agar tidak diulang setiap rerun."""
    if len(df) > n:
        return df.sample(n=n, random_state=42)
    return df


sat_sample = sample_for_scatter(filtered_sat, year_option_2)

# Price vs Review
st.subheader("💰 Price vs Customer Satisfaction")
chart_price = alt.Chart(sat_sample).mark_circle(size=40, opacity=0.4).encode(
    x=alt.X('price', title='Price'),
    y=alt.Y('review_score', title='Review Score'),
    tooltip=['price', 'review_score']
).properties(height=300).interactive()
st.altair_chart(chart_price, use_container_width=True)

# Delivery Time vs Review
st.subheader("🚚 Delivery Time vs Customer Satisfaction")
chart_delivery = alt.Chart(sat_sample).mark_circle(size=40, opacity=0.4).encode(
    x=alt.X('delivery_time', title='Delivery Time (days)'),
    y=alt.Y('review_score', title='Review Score'),
    tooltip=['delivery_time', 'review_score']
).properties(height=300).interactive()
st.altair_chart(chart_delivery, use_container_width=True)

# Delay vs Review + Trend Line — FIX: pisahkan nama variabel
st.subheader("⏱️ Delivery Delay vs Customer Satisfaction")

base_delay = alt.Chart(sat_sample).mark_circle(size=40, opacity=0.4).encode(
    x=alt.X('delay', title='Delay (days)'),
    y=alt.Y('review_score', title='Review Score'),
    tooltip=['delay', 'review_score']
).properties(height=300)

trend_line = base_delay.transform_regression(
    'delay', 'review_score'
).mark_line(color='red', strokeWidth=2)

# Render sekali dengan trend, bukan dua kali terpisah
st.altair_chart((base_delay + trend_line).interactive(), use_container_width=True)

# Correlation Summary — gunakan filtered_sat (data penuh) untuk akurasi
st.subheader("📈 Correlation Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Price vs Review",
            round(filtered_sat[['price', 'review_score']].corr().iloc[0, 1], 3))
col2.metric("Delivery Time vs Review",
            round(filtered_sat[['delivery_time', 'review_score']].corr().iloc[0, 1], 3))
col3.metric("Delay vs Review",
            round(filtered_sat[['delay', 'review_score']].corr().iloc[0, 1], 3))

# Strategic Categories
st.subheader("🚀 Strategic Categories")
strategic = product[
    (product['contribution_%'] > product['contribution_%'].mean()) &
    (product['growth_%'] > 50)
    ]
st.dataframe(strategic)

# ─── SECTION 3: RFM & GEOSPATIAL ──────────────────────────────
st.header("📊 Analisis RFM & Geospatial")

col1, col2, col3 = st.columns(3)
col1.metric("Total Customer", rfm.shape[0])
col2.metric("Total Revenue", int(rfm['monetary'].sum()))
col3.metric("Avg Spending", int(rfm['monetary'].mean()))

st.subheader("📊 Customer Segment Distribution")
st.bar_chart(rfm['segment'].value_counts())

st.subheader("🔥 Top VIP Customers")
vip = rfm[rfm['segment'] == '🔥 VIP Customer']
st.dataframe(vip.head(10))

st.subheader("🌍 Top Cities by Customers")
top_city = city.sort_values(by='total_customers', ascending=False).head(10)
st.dataframe(top_city)

st.subheader("🗺️ Customer Distribution Map")
city_map = city.rename(columns={'lng': 'lon'})
st.map(city_map[['lat', 'lon']].dropna())

st.subheader("🔍 Filter by Segment")
segment_option = st.selectbox("Pilih Segment", rfm['segment'].unique())
filtered = rfm[rfm['segment'] == segment_option]
st.dataframe(filtered.head(20))