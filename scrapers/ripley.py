import json
import re
from urllib.parse import quote
from typing import List
import httpx
from .base import BaseScraper, ProductItem
from .filter_utils import detect_condition

class RipleyScraper(BaseScraper):
    store_name = "Ripley"
    store_id = "ripley"
    store_color = "#8b5cf6" # Violet/Purple

    async def search(self, query: str, client: httpx.AsyncClient) -> List[ProductItem]:
        items: List[ProductItem] = []
        try:
            url = f"https://simple.ripley.com.pe/search/{quote(query)}"
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Accept-Language": "es-PE,es;q=0.9,en;q=0.8"
            }
            resp = await client.get(url, headers=headers, timeout=12.0)
            if resp.status_code != 200:
                return items

            match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', resp.text)
            if not match:
                return items

            data = json.loads(match.group(1))
            page_props = data.get("props", {}).get("pageProps", {})
            raw_products = (
                page_props.get("findabilityProps", {}).get("data", {}).get("products") or
                page_props.get("products") or []
            )

            for p in raw_products:
                name = p.get("name") or ""
                brand = p.get("brand") or ""
                
                # Price extraction
                price = p.get("priceNumber") or p.get("masterPriceNumber")
                if not price:
                    raw_price = str(p.get("price", "0")).replace("S/", "").replace(",", "").strip()
                    try:
                        price = float(raw_price)
                    except ValueError:
                        price = 0.0

                if price <= 0:
                    continue

                # Old price extraction
                original_price = None
                old_raw = str(p.get("oldPrice", "")).replace("S/", "").replace(",", "").strip()
                if old_raw:
                    try:
                        parsed_old = float(old_raw)
                        if parsed_old > price:
                            original_price = parsed_old
                    except ValueError:
                        pass

                discount_percent = p.get("discount")
                if not discount_percent and original_price and original_price > price:
                    discount_percent = round((1 - (price / original_price)) * 100)

                # Images
                images = p.get("images") or []
                image_url = images[0] if images else p.get("primaryImage", "")

                # URL
                part_no = p.get("parentProductID") or p.get("sku") or ""
                slug = re.sub(r'[^a-zA-Z0-9]+', '-', name.lower()).strip('-')
                prod_url = f"https://simple.ripley.com.pe/{slug}-{part_no}" if part_no else f"https://simple.ripley.com.pe/search/{quote(query)}"

                cond = detect_condition(name)
                prod_id = part_no or p.get("code") or f"ripley-{len(items)+1}"

                items.append(ProductItem(
                    id=f"ripley-{prod_id}",
                    title=name,
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
                    in_stock=p.get("inStock", True),
                    condition=cond
                ))
        except Exception as e:
            print(f"[RipleyScraper Error]: {e}")

        return items
