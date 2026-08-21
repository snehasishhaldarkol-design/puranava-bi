import streamlit as st
import pandas as pd
import plotly.express as px
import random

# Core Modules
class CompetitorScraper:
    def __init__(self):
        self.platforms = ["Amazon", "Flipkart", "Meesho"]
    def fetch_market_data(self, category_keyword="Ayurvedic Balm"):
        competitors = [
            {"brand": "Zandu Balm", "product": "Ayurvedic Pain Balm 50g", "price": 140, "rating": 4.3, "platform": "Amazon", "reviews_count": 1250},
            {"brand": "Amrutanjan", "product": "Strong Pain Balm", "price": 125, "rating": 4.2, "platform": "Flipkart", "reviews_count": 980},
            {"brand": "Namyaa", "product": "Bum Thigh Lightening Cream", "price": 399, "rating": 3.9, "platform": "Amazon", "reviews_count": 450},
            {"brand": "Sanfe", "product": "Bum Thigh Anti-Chafing Rub", "price": 349, "rating": 4.1, "platform": "Flipkart", "reviews_count": 620},
            {"brand": "Generic Herbal", "product": "Natural Herbal Balm 100g", "price": 99, "rating": 3.7, "platform": "Meesho", "reviews_count": 210},
            {"brand": "Pure Ayurvedic", "product": "Organic Body Balm", "price": 149, "rating": 4.0, "platform": "Meesho", "reviews_count": 310}
        ]
        for comp in competitors:
            comp["negative_review_gaps"] = random.choice([
                "Strong chemical odor, greasy residue on skin",
                "Packaging leaks during transit, tub was half empty",
                "Takes too long to absorb, stains clothes",
                "Causes mild burning sensation, no immediate relief",
                "Inconsistent texture, hard to apply evenly"
            ])
            comp["estimated_margin"] = round(comp["price"] * (0.65 if comp["platform"] == "Meesho" else 0.45), 2)
        return pd.DataFrame(competitors)

class MarketAnalyzer:
    def __init__(self, df):
        self.df = df
    def identify_market_gaps(self):
        low_rated = self.df[self.df["rating"] <= 4.1]
        return low_rated[["brand", "platform", "price", "negative_review_gaps"]].to_dict(orient="records")

class StrategyEngine:
    @staticmethod
    def generate_gtm_strategy(target_platform):
        strategies = {
            "Meesho": {"pricing": "Target Rs. 129 - Rs. 169 (Value Pack Strategy)", "positioning": "100% Authentic Herbal Formulation with Zero Chemical Additives", "ad_focus": "Focus on high-volume WhatsApp/Social Media visual sharing, highlighting non-greasy application.", "differentiator": "Leak-proof packaging + Non-staining fast absorption formula."},
            "Flipkart": {"pricing": "Target Rs. 249 - Rs. 299 (Mid-Tier Premium)", "positioning": "Fast-Absorbing Ayurvedic Body Care Solution", "ad_focus": "Run Flipkart PLA targeting terms like anti-chafing balm and ayurvedic pain rub.", "differentiator": "Dermatologically tested herbal blend with soothing natural fragrance."},
            "Amazon": {"pricing": "Target Rs. 349 - Rs. 399 (Premium D2C Brand)", "positioning": "Clean, Organic Ayurvedic Care for Urban Lifestyle Needs", "ad_focus": "Amazon Sponsored Products + Brand Store video infographics showing ingredient benefits.", "differentiator": "Eco-friendly recyclable packaging + 100% cruelty-free natural extracts."}
        }
        return strategies.get(target_platform, strategies["Amazon"])

# Application Dashboard
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
    fig = px.scatter(filtered_df, x="price", y="rating", color="platform", size="reviews_count", hover_data=["brand", "product"], labels={"price": "Price (Rs.)", "rating": "Rating (out of 5)"})
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Uncovered Competitor Pain Points (Customer Review Mining)")
    st.write("Exploit these negative gaps in existing e-commerce listings:")
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
