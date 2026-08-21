import pandas as pd
import random

class CompetitorScraper:
    def fetch_market_data(self):
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
