from typing import List
import httpx
from .vtex_base import VTEXBaseScraper
from .base import ProductItem
from .filter_utils import clean_text

class HMScraper(VTEXBaseScraper):
    store_name = "H&M"
    store_id = "hm"
    store_color = "#e11d48"  # H&M Red
    base_url = "https://pe.hm.com"

    async def search(self, query: str, client: httpx.AsyncClient) -> List[ProductItem]:
        q_norm = clean_text(query).strip()
        # If the user is searching for H&M brand itself, use general fashion query
        if q_norm in ("hm", "h&m", "tienda hm", "h y m", "hm peru", "h&m peru", "ropa hm", "ropa h&m"):
            actual_query = "ropa"
        else:
            actual_query = query
        return await super().search(actual_query, client)
