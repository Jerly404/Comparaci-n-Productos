from .vtex_base import VTEXBaseScraper

class ClaroScraper(VTEXBaseScraper):
    store_name = "Claro"
    store_id = "claro"
    store_color = "#e11d48" # Claro Crimson Red
    base_url = "https://tiendaclaro.pe"
