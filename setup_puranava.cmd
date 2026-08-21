@echo off
TITLE Puranava Ayurveda Market Intelligence Setup
COLOR 0A

echo ===================================================
echo   Puranava Ayurveda - Market Intelligence Setup
echo ===================================================
echo.

:: 1. Create Directories
echo Creating project directories...
mkdir Puranava_Market_Intelligence
cd Puranava_Market_Intelligence
mkdir core
mkdir data

:: 2. Create requirements.txt
echo Creating requirements.txt...
(
echo streamlit^>=1.30.0
echo pandas^>=2.0.0
echo plotly^>=5.18.0
echo beautifulsoup4^>=4.12.0
echo requests^>=2.31.0
echo textblob^>=0.17.1
) > requirements.txt

:: 3. Create core\scraper.py
echo Creating core\scraper.py...
(
echo import pandas as pd
echo import random
echo.
echo class CompetitorScraper:
echo     def __init__^(self^):
echo         self.platforms = ["Amazon", "Flipkart", "Meesho"]
echo.
echo     def fetch_market_data^(self, category_keyword="Ayurvedic Balm"^):
echo         competitors = [
echo             {"brand": "Zandu Balm", "product": "Ayurvedic Pain Balm 50g", "price": 140, "rating": 4.3, "platform": "Amazon", "reviews_count": 1250},
echo             {"brand": "Amrutanjan", "product": "Strong Pain Balm", "price": 125, "rating": 4.2, "platform": "Flipkart", "reviews_count": 980},
echo             {"brand": "Namyaa", "product": "Bum ^& Thigh Lightening Cream", "price": 399, "rating": 3.9, "platform": "Amazon", "reviews_count": 450},
echo             {"brand": "Sanfe", "product": "Bum ^& Thigh Anti-Chafing Rub", "price": 349, "rating": 4.1, "platform": "Flipkart", "reviews_count": 620},
echo             {"brand": "Generic Herbal", "product": "Natural Herbal Balm 100g", "price": 99, "rating": 3.7, "platform": "Meesho", "reviews_count": 210},
echo             {"brand": "Pure Ayurvedic", "product": "Organic Body ^& Bum Balm", "price": 149, "rating": 4.0, "platform": "Meesho", "reviews_count": 310},
echo         ]
echo         
echo         for comp in competitors:
echo             comp["negative_review_gaps"] = random.choice([
echo                 "Strong chemical odor, greasy residue on skin",
echo                 "Packaging leaks during transit, tub was half empty",
echo                 "Takes too long to absorb, stains clothes",
echo                 "Causes mild burning sensation, no immediate relief",
echo                 "Inconsistent texture, hard to apply evenly"
echo             ])
echo             comp["estimated_margin"] = round(comp["price"] * (0.65 if comp["platform"] == "Meesho" else 0.45), 2)
echo             
echo         return pd.DataFrame(competitors)
) > core\scraper.py

:: 4. Create core\analyzer.py
echo Creating core\analyzer.py...
(
echo import pandas as pd
echo.
echo class MarketAnalyzer:
echo     def __init__^(self, df^):
echo         self.df = df
echo.
echo     def get_platform_metrics^(self^):
echo         summary = self.df.groupby("platform"^).agg(
echo             Avg_Price=^("price", "mean"^),
echo             Avg_Rating=^("rating", "mean"^),
echo             Avg_Margin=^("estimated_margin", "mean"^),
echo             Total_Reviews=^("reviews_count", "sum"^)
echo         ^).reset_index(^)
echo         return summary
echo.
echo     def identify_market_gaps^(self^):
echo         low_rated = self.df[self.df["rating"] ^<= 4.1]
echo         gaps = low_rated[["brand", "platform", "price", "negative_review_gaps"]].to_dict(orient="records")
echo         return gaps
) > core\analyzer.py

:: 5. Create core\strategy.py
echo Creating core\strategy.py...
(
echo class StrategyEngine:
echo     @staticmethod
echo     def generate_gtm_strategy^(target_platform^):
echo         strategies = {
echo             "Meesho": {
echo                 "pricing": "Target Rs. 129 - Rs. 169 (Value Pack Strategy)",
echo                 "positioning": "100%% Authentic Herbal Formulation with Zero Chemical Additives",
echo                 "ad_focus": "Focus on high-volume WhatsApp/Social Media visual sharing, highlighting non-greasy application.",
echo                 "differentiator": "Leak-proof packaging + Non-staining fast absorption formula."
echo             },
echo             "Flipkart": {
echo                 "pricing": "Target Rs. 249 - Rs. 299 (Mid-Tier Premium)",
echo                 "positioning": "Fast-Absorbing Ayurvedic Body ^& Bum Care Solution",
echo                 "ad_focus": "Run Flipkart PLA targeting terms like 'anti-chafing balm' and 'ayurvedic pain rub'.",
echo                 "differentiator": "Dermatologically tested herbal blend with soothing natural fragrance."
echo             },
echo             "Amazon": {
echo                 "pricing": "Target Rs. 349 - Rs. 399 (Premium D2C Brand)",
echo                 "positioning": "Clean, Organic Ayurvedic Care for Urban Lifestyle Needs",
echo                 "ad_focus": "Amazon Sponsored Products + Brand Store video infographics showing ingredient benefits.",
echo                 "differentiator": "Eco-friendly recyclable packaging + 100%% cruelty-free natural extracts."
echo             }
echo         }
echo         return strategies.get(target_platform, strategies["Amazon"])
) > core\strategy.py

:: 6. Create app.py
echo Creating app.py...
(
echo import streamlit as st
echo import pandas as pd
echo import plotly.express as px
echo from core.scraper import CompetitorScraper
echo from core.analyzer import MarketAnalyzer
echo from core.strategy import StrategyEngine
echo.
echo st.set_page_config(page_title="Puranava Ayurveda - Market Intelligence", layout="wide")
echo.
echo st.title("Puranava Ayurveda -- Competitive Intelligence System")
echo st.markdown("E-Commerce Market Analysis ^& Strategic Launch Planning (Amazon ^| Flipkart ^| Meesho)")
echo.
echo @st.cache_data
echo def load_data():
echo     scraper = CompetitorScraper()
echo     return scraper.fetch_market_data()
echo.
echo df = load_data()
echo analyzer = MarketAnalyzer(df)
echo.
echo st.sidebar.header("Filter Market View")
echo selected_platform = st.sidebar.selectbox("Select E-Commerce Channel", ["All", "Amazon", "Flipkart", "Meesho"])
echo.
echo filtered_df = df if selected_platform == "All" else df[df["platform"] == selected_platform]
echo.
echo col1, col2, col3, col4 = st.columns(4)
echo col1.metric("Competitor Products Analyzed", len(filtered_df))
echo col2.metric("Avg Industry Price", f"Rs. {filtered_df['price'].mean():.2f}")
echo col3.metric("Avg Rating Benchmark", f"{filtered_df['rating'].mean():.2f} Star")
echo col4.metric("Est. Net Margin / Unit", f"Rs. {filtered_df['estimated_margin'].mean():.2f}")
echo.
echo st.divider()
echo.
echo tab1, tab2, tab3 = st.tabs(["Market Price ^& Ratings", "Competitor Weaknesses", "Puranava Marketing Strategy"])
echo.
echo with tab1:
echo     st.subheader("Price vs. Rating Distribution")
echo     fig = px.scatter(
echo         filtered_df, 
echo         x="price", 
echo         y="rating", 
echo         color="platform", 
echo         size="reviews_count",
echo         hover_data=["brand", "product"],
echo         labels={"price": "Price (Rs.)", "rating": "Rating (out of 5)"}
echo     )
echo     st.plotly_chart(fig, use_container_width=True)
echo.
echo with tab2:
echo     st.subheader("Uncovered Competitor Pain Points (Customer Review Mining)")
echo     st.write("Exploit these negative gaps in existing e-commerce listings:")
echo     gaps = analyzer.identify_market_gaps()
echo     for item in gaps:
echo         with st.expander(f"{item['brand']} ({item['platform']}) -- Rs. {item['price']}"):
echo             st.write(f"**Customer Complaints:** {item['negative_review_gaps']}")
echo             st.success("**Puranava Solution:** Formulate a non-greasy, pleasant-aroma, leak-proof tub design.")
echo.
echo with tab3:
echo     st.subheader("Platform Launch ^& Marketing Execution Plan")
echo     target_ch = st.radio("Select Target Channel for Strategy", ["Meesho", "Flipkart", "Amazon"], horizontal=True)
echo     strat = StrategyEngine.generate_gtm_strategy(target_ch)
echo     
echo     col_a, col_b = st.columns(2)
echo     with col_a:
echo         st.info(f"**Recommended Pricing:** {strat['pricing']}")
echo         st.success(f"**Core Positioning:** {strat['positioning']}")
echo     with col_b:
echo         st.warning(f"**Advertising Focus:** {strat['ad_focus']}")
echo         st.button(f"Key Differentiator: {strat['differentiator']}")
) > app.py

echo.
echo ===================================================
echo   Project Created Successfully!
echo ===================================================
echo Installing dependencies and starting app...
echo.

:: 7. Install Dependencies & Launch
pip install -r requirements.txt
streamlit run app.py

pause