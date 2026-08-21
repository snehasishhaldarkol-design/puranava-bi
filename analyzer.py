import pandas as pd

class MarketAnalyzer:
    def __init__(self, df):
        self.df = df
    def identify_market_gaps(self):
        low_rated = self.df[self.df["rating"] <= 4.1]
        return low_rated[["brand", "platform", "price", "negative_review_gaps"]].to_dict(orient="records")
