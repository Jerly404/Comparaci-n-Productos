import asyncio
from typing import List, Dict, Optional, Any
import httpx
from .base import ProductItem, BaseScraper
from .falabella import FalabellaScraper
from .ripley import RipleyScraper
from .plazavea import PlazaVeaScraper
from .coolbox import CoolboxScraper
from .oechsle import OechsleScraper
from .promart import PromartScraper
from .hiraoka import HiraokaScraper
from .claro import ClaroScraper
from .entel import EntelScraper
from .lacuracao import LaCuracaoScraper
from .efe import TiendasEfeScraper
from .shopstar import ShopstarScraper
from .filter_utils import is_valid_phone_item

ALL_SCRAPERS: Dict[str, BaseScraper] = {
    "falabella": FalabellaScraper(),
    "ripley": RipleyScraper(),
    "plazavea": PlazaVeaScraper(),
    "coolbox": CoolboxScraper(),
    "oechsle": OechsleScraper(),
    "promart": PromartScraper(),
    "hiraoka": HiraokaScraper(),
    "claro": ClaroScraper(),
    "entel": EntelScraper(),
    "lacuracao": LaCuracaoScraper(),
    "efe": TiendasEfeScraper(),
    "shopstar": ShopstarScraper()
}

class SearchManager:
    def __init__(self):
        self.scrapers = ALL_SCRAPERS

    def get_supported_stores(self) -> List[Dict[str, str]]:
        return [
            {
                "id": s_id,
                "name": scraper.store_name,
                "color": scraper.store_color
            }
            for s_id, scraper in self.scrapers.items()
        ]

    async def search_store(self, scraper: BaseScraper, query: str, client: httpx.AsyncClient) -> List[ProductItem]:
        try:
            return await scraper.search(query, client)
        except Exception as e:
            print(f"[Error in {scraper.store_name}]: {e}")
            return []

    async def search_all(
        self,
        query: str,
        stores: Optional[List[str]] = None,
        hide_accessories: bool = True,
        include_refurbished: bool = True,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        sort_by: str = "asc" # 'asc' (menor a mayor), 'desc' (mayor a menor), 'discount'
    ) -> Dict[str, Any]:
        active_scrapers = []
        if stores:
            for s_id in stores:
                if s_id in self.scrapers:
                    active_scrapers.append(self.scrapers[s_id])
        if not active_scrapers:
            active_scrapers = list(self.scrapers.values())

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept-Language": "es-PE,es;q=0.9,en;q=0.8"
        }

        async with httpx.AsyncClient(headers=headers, timeout=14.0, follow_redirects=True) as client:
            tasks = [self.search_store(scraper, query, client) for scraper in active_scrapers]
            results_nested = await asyncio.gather(*tasks, return_exceptions=True)

        all_items: List[ProductItem] = []
        for r in results_nested:
            if isinstance(r, list):
                all_items.extend(r)

        # Apply filtering
        filtered_items: List[ProductItem] = []
        for item in all_items:
            # Check refurbished
            if not include_refurbished and item.condition == "Reacondicionado":
                continue

            # Check min/max price
            if min_price is not None and item.price < min_price:
                continue
            if max_price is not None and item.price > max_price:
                continue

            # Validate phone / remove accessories
            if not is_valid_phone_item(item.title, query, item.price, hide_accessories=hide_accessories):
                continue

            filtered_items.append(item)

        # Sort items: default is ASCENDING (menor precio a mayor precio)
        if sort_by == "desc":
            filtered_items.sort(key=lambda x: x.price, reverse=True)
        elif sort_by == "discount":
            filtered_items.sort(key=lambda x: (x.discount_percent or 0), reverse=True)
        else: # 'asc' - menor a mayor
            filtered_items.sort(key=lambda x: x.price)

        # Compute summary analytics
        prices = [x.price for x in filtered_items]
        stats = {
            "total_results": len(filtered_items),
            "lowest_price": min(prices) if prices else 0.0,
            "highest_price": max(prices) if prices else 0.0,
            "average_price": round(sum(prices) / len(prices), 2) if prices else 0.0,
            "cheapest_item": filtered_items[0].to_dict() if filtered_items else None
        }

        # Store breakdown
        store_stats = {}
        for s in active_scrapers:
            s_items = [x for x in filtered_items if x.store_id == s.store_id]
            s_prices = [x.price for x in s_items]
            store_stats[s.store_id] = {
                "name": s.store_name,
                "color": s.store_color,
                "count": len(s_items),
                "lowest_price": min(s_prices) if s_prices else None
            }

        return {
            "query": query,
            "sort_by": sort_by,
            "stats": stats,
            "stores": store_stats,
            "results": [item.to_dict() for item in filtered_items]
        }
