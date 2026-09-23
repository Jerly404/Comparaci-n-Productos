from .vtex_base import VTEXBaseScraper

class ShopstarScraper(VTEXBaseScraper):
    store_name = "Shopstar"
    store_id = "shopstar"
    store_color = "#6366f1" # Indigo
    base_url = "https://www.shopstar.pe"
