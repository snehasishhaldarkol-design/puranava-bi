class StrategyEngine:
    @staticmethod
    def generate_gtm_strategy(target_platform):
        strategies = {
            "Meesho": {
                "pricing": "Target Rs. 129 - Rs. 169 (Value Pack Strategy)",
                "positioning": "100% Authentic Herbal Formulation with Zero Chemical Additives",
                "ad_focus": "Focus on high-volume WhatsApp/Social Media visual sharing.",
                "differentiator": "Leak-proof packaging + Non-staining fast absorption formula."
            },
            "Flipkart": {
                "pricing": "Target Rs. 249 - Rs. 299 (Mid-Tier Premium)",
                "positioning": "Fast-Absorbing Ayurvedic Body Care Solution",
                "ad_focus": "Run Flipkart PLA targeting terms like anti-chafing balm.",
                "differentiator": "Dermatologically tested herbal blend with soothing natural fragrance."
            },
            "Amazon": {
                "pricing": "Target Rs. 349 - Rs. 399 (Premium D2C Brand)",
                "positioning": "Clean, Organic Ayurvedic Care for Urban Lifestyle Needs",
                "ad_focus": "Amazon Sponsored Products + Brand Store video infographics.",
                "differentiator": "Eco-friendly recyclable packaging + 100% cruelty-free extracts."
            }
        }
        return strategies.get(target_platform, strategies["Amazon"])
