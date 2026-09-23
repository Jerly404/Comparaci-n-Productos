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

import re

CAJAMARCA_EL_QUINDE_STORES = {"falabella", "ripley", "claro", "entel", "metro"}
CAJAMARCA_REAL_PLAZA_STORES = {"plazavea", "promart", "oechsle"}
LIMA_STORE_PRESENCE = {"falabella", "ripley", "plazavea", "oechsle", "promart", "metro", "hiraoka", "coolbox", "claro", "entel", "lacuracao", "efe"}
AREQUIPA_STORE_PRESENCE = {"falabella", "ripley", "plazavea", "oechsle", "promart", "metro", "claro", "entel", "lacuracao", "efe"}
TRUJILLO_STORE_PRESENCE = {"falabella", "ripley", "plazavea", "promart", "metro", "claro", "entel", "oechsle", "lacuracao", "efe"}
CHICLAYO_PIURA_STORE_PRESENCE = {"falabella", "ripley", "plazavea", "promart", "metro", "claro", "entel", "oechsle", "lacuracao", "efe"}
CUSCO_STORE_PRESENCE = {"falabella", "promart", "plazavea", "claro", "entel", "lacuracao", "efe"}

STORE_EXCLUSIVE_CARDS = {
    "falabella": "CMR Falabella",
    "ripley": "Tarjeta Ripley",
    "plazavea": "Tarjeta Oh!",
    "oechsle": "Tarjeta Oh!",
    "promart": "Tarjeta Oh!"
}

def extract_inferred_specs(title: str, condition: str) -> dict:
    specs = {}
    title_upper = title.upper()

    # Storage
    storage_match = re.search(r'\b(64|128|256|512)\s*GB\b|\b(1|2)\s*TB\b', title_upper)
    if storage_match:
        specs["Almacenamiento"] = storage_match.group(0).replace(" ", "")
    
    # RAM
    ram_match = re.search(r'\b(4|6|8|12|16|24|32|64)\s*GB(?:\s*RAM)?\b', title_upper)
    if ram_match and (not storage_match or ram_match.group(0) != storage_match.group(0)):
        specs["Memoria RAM"] = ram_match.group(0).replace(" ", "")

    # Display / Screen size
    screen_match = re.search(r'(\d{1,2}(?:\.\d{1,2})?)\s*(?:["\']|PULGADAS|PULG)', title_upper)
    if screen_match:
        specs["Pantalla"] = f"{screen_match.group(1)}\""

    # Warranty
    if condition == "Reacondicionado":
        specs["Garantía"] = "6 Meses (Garantía Tienda / Grado A)"
    else:
        specs["Garantía"] = "12 Meses (Garantía Oficial Perú)"

    specs["Estado"] = condition
    return specs

def enrich_product_item(item: ProductItem, avg_price: float = 0.0, location: str = "todas"):
    # 1. Store payment method
    if item.store_id in STORE_EXCLUSIVE_CARDS:
        item.payment_method = STORE_EXCLUSIVE_CARDS[item.store_id]
        item.card_name = STORE_EXCLUSIVE_CARDS[item.store_id]
    else:
        item.payment_method = "Cualquier Tarjeta / Yape / Efectivo"
        item.card_name = None

    # 2. Regional pickup & logistics
    loc = (location or "todas").strip().lower()
    if loc == "cajamarca":
        if item.store_id in CAJAMARCA_EL_QUINDE_STORES:
            item.pickup_cajamarca = True
            item.pickup_available = True
            item.pickup_location = "El Quinde Cajamarca (Retiro Gratis)"
        elif item.store_id in CAJAMARCA_REAL_PLAZA_STORES:
            item.pickup_cajamarca = True
            item.pickup_available = True
            item.pickup_location = "Real Plaza Cajamarca (Retiro Gratis)"
        else:
            item.pickup_cajamarca = False
            item.pickup_available = False
            item.pickup_location = "Envío courier a Cajamarca (S/ 15 - 25)"
    elif loc in ("lima", "miraflores", "surco", "lima_centro", "lima_norte", "lima_sur", "lima_este", "callao"):
        item.pickup_cajamarca = False
        item.pickup_available = True
        item.pickup_location = "Retiro Gratis en Tienda (Lima Metropolitana)"
    elif loc == "arequipa":
        item.pickup_cajamarca = False
        if item.store_id in AREQUIPA_STORE_PRESENCE:
            item.pickup_available = True
            item.pickup_location = "Mall Aventura / Real Plaza Arequipa (Retiro Gratis)"
        else:
            item.pickup_available = False
            item.pickup_location = "Envío courier a Arequipa (S/ 15 - 20)"
    elif loc == "trujillo":
        item.pickup_cajamarca = False
        if item.store_id in TRUJILLO_STORE_PRESENCE:
            item.pickup_available = True
            item.pickup_location = "Mallplaza / Real Plaza Trujillo (Retiro Gratis)"
        else:
            item.pickup_available = False
            item.pickup_location = "Envío courier a Trujillo (S/ 15 - 20)"
    elif loc == "chiclayo_piura":
        item.pickup_cajamarca = False
        if item.store_id in CHICLAYO_PIURA_STORE_PRESENCE:
            item.pickup_available = True
            item.pickup_location = "Mall Aventura / Real Plaza (Retiro Gratis)"
        else:
            item.pickup_available = False
            item.pickup_location = "Envío courier a Piura/Chiclayo (S/ 15 - 22)"
    elif loc == "cusco":
        item.pickup_cajamarca = False
        if item.store_id in CUSCO_STORE_PRESENCE:
            item.pickup_available = True
            item.pickup_location = "Real Plaza Cusco (Retiro Gratis)"
        else:
            item.pickup_available = False
            item.pickup_location = "Envío courier a Cusco / Huancayo (S/ 18 - 25)"
    else: # "todas"
        item.pickup_cajamarca = item.store_id in (CAJAMARCA_EL_QUINDE_STORES | CAJAMARCA_REAL_PLAZA_STORES)
        item.pickup_available = True
        item.pickup_location = "Retiro en tienda o envío a todo el Perú"

    # 3. Installments
    item.installments_12x = round(item.price / 12, 2)
    item.installments_info = f"12 cuotas de S/ {item.installments_12x:,.2f} sin int. (BCP, BBVA, Interbank)"

    # 4. Inferred specs for side-by-side comparison
    item.specs = extract_inferred_specs(item.title, item.condition)

    # 5. Deal verdict (Semáforo de Oferta)
    discount = item.discount_percent or 0
    if discount >= 25 or (avg_price > 0 and item.price <= 0.82 * avg_price):
        item.deal_verdict = "Mínimo Histórico"
    elif discount >= 10 or (avg_price > 0 and item.price <= 0.93 * avg_price):
        item.deal_verdict = "Buen Precio"
    else:
        item.deal_verdict = "Precio Normal"

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
        sort_by: str = "asc", # 'asc' (menor a mayor), 'desc' (mayor a menor), 'discount'
        payment_filter: Optional[str] = None, # 'all', 'any_card', 'store_cards'
        pickup_cajamarca_only: bool = False,
        pickup_only: bool = False,
        deal_verdict_filter: Optional[str] = None, # 'all', 'minimo', 'buen_precio'
        location: str = "todas",
        only_discounts: bool = False
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

        # Baseline filter
        valid_items: List[ProductItem] = []
        for item in all_items:
            # Check refurbished
            if not include_refurbished and item.condition == "Reacondicionado":
                continue

            # Check min/max price
            if min_price is not None and item.price < min_price:
                continue
            if max_price is not None and item.price > max_price:
                continue

            # Validate phone / general product & filter accessories
            if not is_valid_phone_item(item.title, query, item.price, hide_accessories=hide_accessories):
                continue

            valid_items.append(item)

        # Preliminary average calculation for deal verdict
        preliminary_prices = [x.price for x in valid_items]
        avg_price = (sum(preliminary_prices) / len(preliminary_prices)) if preliminary_prices else 0.0

        # Enrich all valid items with regional pickup and specs
        for item in valid_items:
            enrich_product_item(item, avg_price=avg_price, location=location)

        # Apply secondary filters (discounts, payment method, regional pickup, deal verdict)
        filtered_items: List[ProductItem] = []
        for item in valid_items:
            # Discount only filter
            if only_discounts:
                has_discount = ((item.discount_percent or 0) > 0) or (item.original_price is not None and item.original_price > item.price)
                if not has_discount:
                    continue

            # Payment method filter
            if payment_filter == "any_card":
                if item.card_name is not None:
                    continue
            elif payment_filter == "store_cards":
                if item.card_name is None:
                    continue

            # Regional store pickup filter
            if pickup_only and not item.pickup_available:
                continue

            # Cajamarca pickup only filter (backwards compatibility)
            if pickup_cajamarca_only and not item.pickup_cajamarca:
                continue

            # Deal verdict filter
            if deal_verdict_filter == "minimo":
                if item.deal_verdict != "Mínimo Histórico":
                    continue
            elif deal_verdict_filter == "buen_precio":
                if item.deal_verdict not in ("Mínimo Histórico", "Buen Precio"):
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
            "location": location,
            "only_discounts": only_discounts,
            "stats": stats,
            "stores": store_stats,
            "results": [item.to_dict() for item in filtered_items]
        }
