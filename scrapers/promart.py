from .vtex_base import VTEXBaseScraper

class PromartScraper(VTEXBaseScraper):
    store_name = "Promart"
    store_id = "promart"
    store_color = "#f97316" # Orange
    base_url = "https://www.promart.pe"
