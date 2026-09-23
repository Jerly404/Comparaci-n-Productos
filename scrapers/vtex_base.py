from urllib.parse import quote
from typing import List
import httpx
from .base import BaseScraper, ProductItem
from .filter_utils import detect_condition

class VTEXBaseScraper(BaseScraper):
    base_url: str = ""
    max_items: int = 25

    async def search(self, query: str, client: httpx.AsyncClient) -> List[ProductItem]:
        items: List[ProductItem] = []
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "es-PE,es;q=0.9,en;q=0.8"
            }
            # VTEX search works best with hyphenated or encoded query
            formatted_query = query.strip().replace(" ", "-")
            url = f"{self.base_url}/api/catalog_system/pub/products/search/{quote(formatted_query)}?_from=0&_to={self.max_items-1}&O=OrderByPriceASC"
            
            resp = await client.get(url, headers=headers, timeout=12.0)
            if resp.status_code not in [200, 206]:
                # Retry with regular space encoding if hyphenated gave nothing
                url = f"{self.base_url}/api/catalog_system/pub/products/search/{quote(query)}?_from=0&_to={self.max_items-1}&O=OrderByPriceASC"
                resp = await client.get(url, headers=headers, timeout=12.0)
                if resp.status_code not in [200, 206]:
                    return items

            data = resp.json()
            if not isinstance(data, list):
                return items

            for p in data:
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

                # Images
                images = first_sub.get("images") or []
                image_url = images[0].get("imageUrl", "") if images else ""

                cond = detect_condition(title)
                prod_id = p.get("productId") or first_sub.get("itemId") or f"{self.store_id}-{len(items)+1}"

                items.append(ProductItem(
                    id=f"{self.store_id}-{prod_id}",
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
        except Exception as e:
            print(f"[{self.store_name}Scraper Error]: {e}")

        return items
