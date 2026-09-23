import json
import re
from urllib.parse import quote
from typing import List
import httpx
from .base import BaseScraper, ProductItem
from .filter_utils import detect_condition

class FalabellaScraper(BaseScraper):
    store_name = "Falabella"
    store_id = "falabella"
    store_color = "#34d399" # Emerald/Green

    async def search(self, query: str, client: httpx.AsyncClient) -> List[ProductItem]:
        items: List[ProductItem] = []
        try:
            url = f"https://www.falabella.com.pe/falabella-pe/search?Ntt={quote(query)}"
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
            raw_products = data.get("props", {}).get("pageProps", {}).get("results", [])

            for p in raw_products:
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

                # Find uncrossed prices (offer/event/cmr/internet) and crossed (normal)
                active_prices = []
                for pr in price_list:
                    raw_val = pr.get("price", ["0"])[0].replace(",", "").strip()
                    try:
                        val = float(raw_val)
                    except ValueError:
                        continue

                    is_crossed = pr.get("crossed", False)
                    ptype = pr.get("type", "")

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
                prod_id = p.get("productId") or p.get("skuId") or f"falabella-{len(items)+1}"

                items.append(ProductItem(
                    id=f"fala-{prod_id}",
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
        except Exception as e:
            print(f"[FalabellaScraper Error]: {e}")

        return items
