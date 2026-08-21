import streamlit as st
import pandas as pd
import plotly.express as px
from core.scraper import CompetitorScraper
from core.analyzer import MarketAnalyzer
from core.strategy import StrategyEngine

st.set_page_config(page_title="Puranava Ayurveda - Market Intelligence", layout="wide")
st.title("Puranava Ayurveda -- Competitive Intelligence System")
st.markdown("E-Commerce Market Analysis & Strategic Launch Planning (Amazon | Flipkart | Meesho)")

@st.cache_data
def load_data():
    scraper = CompetitorScraper()
    return scraper.fetch_market_data()

df = load_data()
analyzer = MarketAnalyzer(df)

st.sidebar.header("Filter Market View")
selected_platform = st.sidebar.selectbox("Select E-Commerce Channel", ["All", "Amazon", "Flipkart", "Meesho"])
filtered_df = df if selected_platform == "All" else df[df["platform"] == selected_platform]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Competitor Products Analyzed", len(filtered_df))
col2.metric("Avg Industry Price", f"Rs. {filtered_df['price'].mean():.2f}")
col3.metric("Avg Rating Benchmark", f"{filtered_df['rating'].mean():.2f} Star")
col4.metric("Est. Net Margin / Unit", f"Rs. {filtered_df['estimated_margin'].mean():.2f}")

st.divider()
tab1, tab2, tab3 = st.tabs(["Market Price & Ratings", "Competitor Weaknesses", "Puranava Marketing Strategy"])

with tab1:
    st.subheader("Price vs. Rating Distribution")
    fig = px.scatter(filtered_df, x="price", y="rating", color="platform", size="reviews_count", hover_data=["brand", "product"])
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Uncovered Competitor Pain Points (Customer Review Mining)")
    gaps = analyzer.identify_market_gaps()
    for item in gaps:
        with st.expander(f"{item['brand']} ({item['platform']}) -- Rs. {item['price']}"):
            st.write(f"**Customer Complaints:** {item['negative_review_gaps']}")
            st.success("**Puranava Solution:** Formulate a non-greasy, pleasant-aroma, leak-proof tub design.")

with tab3:
    st.subheader("Platform Launch & Marketing Execution Plan")
    target_ch = st.radio("Select Target Channel for Strategy", ["Meesho", "Flipkart", "Amazon"], horizontal=True)
    strat = StrategyEngine.generate_gtm_strategy(target_ch)
    col_a, col_b = st.columns(2)
    with col_a:
        st.info(f"**Recommended Pricing:** {strat['pricing']}")
        st.success(f"**Core Positioning:** {strat['positioning']}")
    with col_b:
        st.warning(f"**Advertising Focus:** {strat['ad_focus']}")
        st.button(f"Key Differentiator: {strat['differentiator']}")
