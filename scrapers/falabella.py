import json
import re
from urllib.parse import quote
from typing import List
import httpx
import asyncio
from .base import BaseScraper, ProductItem
from .filter_utils import detect_condition

class FalabellaScraper(BaseScraper):
    store_name = "Falabella"
    store_id = "falabella"
    store_color = "#34d399"

    async def search(self, query: str, client: httpx.AsyncClient) -> List[ProductItem]:
        items: List[ProductItem] = []
        seen_ids = set()
        
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept-Language": "es-PE,es;q=0.9,en;q=0.8"
        }

        urls = [
            f"https://www.falabella.com.pe/falabella-pe/search?Ntt={quote(query)}",
            f"https://www.falabella.com.pe/falabella-pe/search?Ntt={quote(query)}&page=2"
        ]

        async def fetch_page(u):
            try:
                resp = await client.get(u, headers=headers, timeout=12.0)
                if resp.status_code != 200:
                    return []
                match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', resp.text)
                if not match:
                    return []
                data = json.loads(match.group(1))
                return data.get("props", {}).get("pageProps", {}).get("results", [])
            except Exception:
                return []

        pages_results = await asyncio.gather(*(fetch_page(u) for u in urls), return_exceptions=True)

        for raw_products in pages_results:
            if not isinstance(raw_products, list):
                continue

            for p in raw_products:
                prod_id = str(p.get("productId") or p.get("skuId") or "")
                if prod_id in seen_ids:
                    continue
                seen_ids.add(prod_id)

                title = p.get("displayName") or ""
                brand = p.get("brand") or ""
                prod_url = p.get("url") or ""
                if prod_url and not prod_url.startswith("http"):
                    prod_url = f"https://www.falabella.com.pe{prod_url}"

                media = p.get("mediaUrls") or []
                image_url = media[0] if media else ""

                # Extract prices
                price_list = p.get("prices") or []
                current_price = None
                original_price = None

                active_prices = []
                for pr in price_list:
                    raw_val = pr.get("price", ["0"])[0].replace(",", "").strip()
                    try:
                        val = float(raw_val)
                    except ValueError:
                        continue

                    is_crossed = pr.get("crossed", False)
                    if not is_crossed and val > 0:
                        active_prices.append(val)
                    elif is_crossed and val > 0:
                        original_price = val

                if active_prices:
                    current_price = min(active_prices)

                if not current_price or current_price <= 0:
                    continue

                discount_percent = None
                if original_price and original_price > current_price:
                    discount_percent = round((1 - (current_price / original_price)) * 100)
                else:
                    original_price = None

                cond = detect_condition(title)

                items.append(ProductItem(
                    id=f"fala-{prod_id or len(items)+1}",
                    title=title,
                    brand=brand,
                    price=current_price,
                    original_price=original_price,
                    discount_percent=discount_percent,
                    currency="PEN",
                    store=self.store_name,
                    store_id=self.store_id,
                    store_color=self.store_color,
                    url=prod_url,
                    image_url=image_url,
                    in_stock=True,
                    condition=cond
                ))

        return items
