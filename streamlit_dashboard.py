
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 Customer360 Dashboard")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data/processed/customer360_segmented.csv")

df = load_data()

# Sidebar filter
cluster = st.sidebar.selectbox("Select Customer Segment", sorted(df['Cluster'].unique().tolist()) + ['All'])
if cluster != 'All':
    df = df[df['Cluster'] == cluster]

# KPI Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🧮 Total Customers", len(df))
with col2:
    st.metric("💰 Total Revenue", f"₹{df['TotalSpent'].sum():,.0f}")
with col3:
    st.metric("😊 Avg Satisfaction", round(df['AvgSatisfactionScore'].mean(), 2))

# Top Customers Table
st.subheader("🏆 Top 5 Customers by Spend")
st.dataframe(df.sort_values(by="TotalSpent", ascending=False)[["Name", "TotalSpent", "Location"]].head(5))

# Charts
st.subheader("📈 Distribution of Satisfaction Scores")
fig, ax = plt.subplots()
sns.boxplot(data=df, x="Cluster", y="AvgSatisfactionScore", palette="Set2", ax=ax)
st.pyplot(fig)

st.subheader("🧭 Resolution Time vs. Spend")
fig2, ax2 = plt.subplots()
sns.scatterplot(data=df, x="TotalSpent", y="AvgResolutionTime", hue="Cluster", palette="Set1", s=100, ax=ax2)
st.pyplot(fig2)
