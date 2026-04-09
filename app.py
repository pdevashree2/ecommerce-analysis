import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('🛒 E-Commerce Sales Dashboard')
st.write('Analysis of 100K+ Brazilian E-Commerce Orders')

# Load data
orders = pd.read_csv(r'C:\Users\pdeva\ecommerce\data\olist_orders_dataset.csv')
customers = pd.read_csv(r'C:\Users\pdeva\ecommerce\data\olist_customers_dataset.csv')
payments = pd.read_csv(r'C:\Users\pdeva\ecommerce\data\olist_order_payments_dataset.csv')
order_items = pd.read_csv(r'C:\Users\pdeva\ecommerce\data\olist_order_items_dataset.csv')

# Clean
orders_clean = orders[orders['order_status'] == 'delivered']
orders_clean = orders_clean.dropna(subset=['order_delivered_customer_date'])

# Merge
df = orders_clean.merge(customers, on='customer_id')
df = df.merge(payments, on='order_id')
df = df.merge(order_items, on='order_id')

# Monthly Revenue
st.subheader('📈 Monthly Revenue')
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
df['month_year'] = df['order_purchase_timestamp'].dt.to_period('M')
monthly_revenue = df.groupby('month_year')['payment_value'].sum().reset_index()
monthly_revenue.columns = ['month', 'revenue']
fig, ax = plt.subplots(figsize=(12,4))
ax.plot(monthly_revenue['month'].astype(str), monthly_revenue['revenue'], marker='o', color='steelblue')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# Top Cities
st.subheader('🏙️ Top 10 Cities by Orders')
top_cities = df.groupby('customer_city')['order_id'].count().reset_index()
top_cities.columns = ['city', 'orders']
top_cities = top_cities.sort_values('orders', ascending=False).head(10)
fig2, ax2 = plt.subplots(figsize=(10,4))
ax2.barh(top_cities['city'], top_cities['orders'], color='steelblue')
ax2.invert_yaxis()
plt.tight_layout()
st.pyplot(fig2)

# Payment Types
st.subheader('💳 Payment Method Breakdown')
payment_types = df.groupby('payment_type')['order_id'].count().reset_index()
payment_types.columns = ['payment_type', 'count']
fig3, ax3 = plt.subplots(figsize=(6,4))
ax3.pie(payment_types['count'], labels=payment_types['payment_type'], autopct='%1.1f%%')
plt.tight_layout()
st.pyplot(fig3)

# Key Metrics
st.subheader('📊 Key Metrics')
col1, col2, col3 = st.columns(3)
col1.metric('Total Orders', f"{len(orders_clean):,}")
col2.metric('Total Revenue', f"R$ {df['payment_value'].sum():,.0f}")
col3.metric('Avg Order Value', f"R$ {df['payment_value'].mean():,.0f}")