import streamlit as st
import pandas as pd
import plotly.express as px
from serpapi import GoogleSearch

# Authentic E-Commerce Scraper via SerpApi
class AuthenticMarketScraper:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_authentic_data(self, query="Ayurvedic Pain Balm"):
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
            
            for item in shopping_results[:15]:
                title = item.get("title", "Unknown Product")
                price_str = item.get("price", "0")
                raw_price = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_str))) if price_str else 0.0
                rating = item.get("rating", 4.0)
                reviews = item.get("reviews", 50)
                merchant = item.get("source", "E-Commerce Vendor")
                
                platform = "Amazon" if "Amazon" in merchant else ("Flipkart" if "Flipkart" in merchant else ("Meesho" if "Meesho" in merchant else merchant))
                
                if raw_price > 0:
                    products.append({
                        "brand": title.split()[0],
                        "product": title,
                        "price": raw_price,
                        "rating": float(rating),
                        "platform": platform,
                        "reviews_count": int(reviews),
                        "seller": merchant,
                        "estimated_margin": round(raw_price * (0.60 if platform == "Meesho" else 0.45), 2)
                    })
        except Exception as e:
            st.error(f"API Data Retrieval Error: {e}")
            
        return pd.DataFrame(products)

st.set_page_config(page_title="Puranava Ayurveda - Authentic BI", layout="wide")
st.title("Puranava Ayurveda -- Authentic E-Commerce Market Intelligence")
st.markdown("Live Data Stream via SerpApi (Amazon | Flipkart | Meesho | D2C Merchants)")

SERPAPI_KEY = st.secrets.get("SERPAPI_KEY", "")

st.sidebar.header("Search & Filters")
search_term = st.sidebar.text_input("Enter Product Category", "Ayurvedic Pain Balm")

if not SERPAPI_KEY:
    st.warning("Please configure your SERPAPI_KEY inside Streamlit Cloud Settings > Secrets to unlock live API streaming.")
else:
    @st.cache_data(ttl=3600)
    def load_data(keyword):
        scraper = AuthenticMarketScraper(SERPAPI_KEY)
        return scraper.fetch_authentic_data(keyword)

    with st.spinner(f"Extracting live market listings for '{search_term}'..."):
        df = load_data(search_term)

    if not df.empty:
        selected_platform = st.sidebar.selectbox("Filter Platform", ["All"] + list(df["platform"].unique()))
        filtered_df = df if selected_platform == "All" else df[df["platform"] == selected_platform]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Authentic Products Scraped", len(filtered_df))
        col2.metric("Avg Market Price", f"Rs. {filtered_df['price'].mean():.2f}")
        col3.metric("Avg Rating Benchmark", f"{filtered_df['rating'].mean():.2f} Star")
        col4.metric("Est. Unit Margin", f"Rs. {filtered_df['estimated_margin'].mean():.2f}")

        st.divider()
        tab1, tab2 = st.tabs(["Price vs. Rating Distribution", "Live E-Commerce Catalog"])

        with tab1:
            st.subheader("Authentic Price Points & Ratings")
            fig = px.scatter(
                filtered_df, 
                x="price", 
                y="rating", 
                color="platform", 
                size="reviews_count", 
                hover_data=["product", "seller"],
                labels={"price": "Live Price (INR)", "rating": "Authentic Star Rating"}
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.subheader("Scraped Marketplace Products")
            st.dataframe(filtered_df[["product", "seller", "platform", "price", "rating", "reviews_count"]], use_container_width=True)
    else:
        st.info("No matching live listings returned. Try adjusting your search query.")
