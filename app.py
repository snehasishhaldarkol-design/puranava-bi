import streamlit as st
import pandas as pd
import plotly.express as px
from serpapi import GoogleSearch

class NightwearMarketScraper:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_nightwear_data(self, query="Women Nighty"):
        params = {
            "engine": "google_shopping",
            "q": query,
            "location": "India",
            "hl": "en",
            "gl": "in",
            "api_key": self.api_key
        }
        
        products = []
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            shopping_results = results.get("shopping_results", [])
            
            for item in shopping_results[:20]:
                title = item.get("title", "Unknown Nightwear")
                price_str = item.get("price", "0")
                raw_price = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_str))) if price_str else 0.0
                rating = item.get("rating", 4.0)
                reviews = item.get("reviews", 30)
                merchant = item.get("source", "E-Commerce Store")
                
                # Identify platform classification
                platform = "Amazon" if "Amazon" in merchant else ("Flipkart" if "Flipkart" in merchant else ("Meesho" if "Meesho" in merchant else merchant))
                
                # Attribute parsing (Fabric & Combo Pack detection)
                title_lower = title.lower()
                fabric = "Cotton" if "cotton" in title_lower else ("Satin/Silk" if any(x in title_lower for x in ["satin", "silk"]) else "Hosiery/Rayon")
                is_combo = "Pack of" in title or "Combo" in title or "Set" in title
                
                if raw_price > 0:
                    products.append({
                        "product": title,
                        "brand": title.split()[0],
                        "seller": merchant,
                        "platform": platform,
                        "price": raw_price,
                        "fabric": fabric,
                        "type": "Combo / Pack" if is_combo else "Single Piece",
                        "rating": float(rating),
                        "reviews_count": int(reviews),
                        "est_margin": round(raw_price * (0.55 if platform == "Meesho" else 0.40), 2)
                    })
        except Exception as e:
            st.error(f"Data Fetching Error: {e}")
            
        return pd.DataFrame(products)

# UI Layout
st.set_page_config(page_title="Women's Nightwear BI Dashboard", layout="wide")
st.title("Women's Nightwear & Sleepwear -- Market Intelligence")
st.markdown("Live E-Commerce Analytics (Cotton Nighties | Satin Sets | Kaftans | Lounge Suits)")

SERPAPI_KEY = st.secrets.get("SERPAPI_KEY", "")

st.sidebar.header("Category Search")
search_term = st.sidebar.text_input("Enter Nightwear Sub-Category", "Cotton Nighty Combo")

if not SERPAPI_KEY:
    st.error("SERPAPI_KEY missing from Streamlit Secrets.")
else:
    @st.cache_data(ttl=3600)
    def load_data(keyword):
        scraper = NightwearMarketScraper(SERPAPI_KEY)
        return scraper.fetch_nightwear_data(keyword)

    with st.spinner(f"Scraping live marketplace listings for '{search_term}'..."):
        df = load_data(search_term)

    if not df.empty:
        # Sidebar Filters
        selected_platform = st.sidebar.selectbox("Filter Platform", ["All"] + list(df["platform"].unique()))
        selected_fabric = st.sidebar.selectbox("Filter Fabric", ["All"] + list(df["fabric"].unique()))
        
        filtered_df = df.copy()
        if selected_platform != "All":
            filtered_df = filtered_df[filtered_df["platform"] == selected_platform]
        if selected_fabric != "All":
            filtered_df = filtered_df[filtered_df["fabric"] == selected_fabric]

        # Top KPIs
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Listings Analyzed", len(filtered_df))
        col2.metric("Avg Retail Price", f"Rs. {filtered_df['price'].mean():.2f}")
        col3.metric("Avg Star Rating", f"{filtered_df['rating'].mean():.2f} Star")
        col4.metric("Est. Gross Margin / Unit", f"Rs. {filtered_df['est_margin'].mean():.2f}")

        st.divider()
        tab1, tab2 = st.tabs(["Fabric & Pricing Matrix", "Live Product Catalog"])

        with tab1:
            st.subheader("Price vs. Rating by Fabric & Platform")
            fig = px.scatter(
                filtered_df, 
                x="price", 
                y="rating", 
                color="fabric", 
                symbol="type",
                size="reviews_count", 
                hover_data=["product", "seller"],
                labels={"price": "Retail Price (INR)", "rating": "Rating"}
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.subheader("Extracted Listings")
            st.dataframe(filtered_df[["product", "seller", "platform", "fabric", "type", "price", "rating"]], use_container_width=True)
