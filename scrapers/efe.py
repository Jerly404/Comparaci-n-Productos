from .magento_base import MagentoBaseScraper

class TiendasEfeScraper(MagentoBaseScraper):
    store_name = "Tiendas EFE"
    store_id = "efe"
    store_color = "#f59e0b" # Amber / Gold
    base_url = "https://www.efe.com.pe"
