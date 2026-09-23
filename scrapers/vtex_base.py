import asyncio
from urllib.parse import quote
from typing import List
import httpx
from .base import BaseScraper, ProductItem
from .filter_utils import detect_condition

class VTEXBaseScraper(BaseScraper):
    base_url: str = ""

    async def search(self, query: str, client: httpx.AsyncClient) -> List[ProductItem]:
        items: List[ProductItem] = []
        seen_ids = set()
        
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "es-PE,es;q=0.9,en;q=0.8"
        }

        # Query page 1 (0-49) and page 2 (50-99) via Full-Text search concurrently
        encoded_query = quote(query)
        urls = [
            f"{self.base_url}/api/catalog_system/pub/products/search?ft={encoded_query}&_from=0&_to=49",
            f"{self.base_url}/api/catalog_system/pub/products/search?ft={encoded_query}&_from=50&_to=99"
        ]

        async def fetch_vtex_page(u: str):
            try:
                resp = await client.get(u, headers=headers, timeout=12.0)
                if resp.status_code in [200, 206] and resp.text.strip().startswith("["):
                    data = resp.json()
                    return data if isinstance(data, list) else []
            except Exception:
                pass
            return []

        pages = await asyncio.gather(*(fetch_vtex_page(u) for u in urls), return_exceptions=True)

        for page_data in pages:
            if not isinstance(page_data, list):
                continue

            for p in page_data:
                prod_id = str(p.get("productId") or "")
                if prod_id in seen_ids:
                    continue
                seen_ids.add(prod_id)

                title = p.get("productName") or p.get("productTitle") or ""
                brand = p.get("brand") or ""
                prod_url = p.get("link") or ""

                items_sub = p.get("items") or []
                if not items_sub:
                    continue

                first_sub = items_sub[0]
                sellers = first_sub.get("sellers") or []
                if not sellers:
                    continue

                comm_offer = sellers[0].get("commertialOffer") or {}
                price = comm_offer.get("Price", 0.0)
                list_price = comm_offer.get("ListPrice", 0.0)
                available_qty = comm_offer.get("AvailableQuantity", 0)

                if price <= 0:
                    continue

                original_price = None
                discount_percent = None
                if list_price and list_price > price:
                    original_price = float(list_price)
                    discount_percent = round((1 - (price / original_price)) * 100)

                images = first_sub.get("images") or []
                image_url = images[0].get("imageUrl", "") if images else ""

                cond = detect_condition(title)
                item_id = prod_id or first_sub.get("itemId") or f"{self.store_id}-{len(items)+1}"

                items.append(ProductItem(
                    id=f"{self.store_id}-{item_id}",
                    title=title,
                    brand=brand,
                    price=float(price),
                    original_price=original_price,
                    discount_percent=discount_percent if discount_percent and discount_percent > 0 else None,
                    currency="PEN",
                    store=self.store_name,
                    store_id=self.store_id,
                    store_color=self.store_color,
                    url=prod_url,
                    image_url=image_url,
                    in_stock=(available_qty > 0),
                    condition=cond
                ))

        return items
