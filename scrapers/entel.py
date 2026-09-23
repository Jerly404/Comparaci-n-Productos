import asyncio
import urllib.request
import ssl
import json
import re
import time
from typing import List, Tuple, Optional
import httpx
from .base import BaseScraper, ProductItem
from .filter_utils import matches_query_keywords, detect_condition

class EntelScraper(BaseScraper):
    store_name = "Entel"
    store_id = "entel"
    store_color = "#0284c7" # Sky / Entel Blue

    def __init__(self):
        self._catalog_cache: List[Tuple[str, str]] = [] # (title, url)
        self._last_catalog_fetch: float = 0
        self._ssl_ctx = ssl.create_default_context()
        self._ssl_ctx.check_hostname = False
        self._ssl_ctx.verify_mode = ssl.CERT_NONE
        self._headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept-Language": "es-PE,es;q=0.9,en;q=0.8"
        }

    def _get_catalog_sync(self) -> List[Tuple[str, str]]:
        # Refresh cache every hour
        now = time.time()
        if self._catalog_cache and (now - self._last_catalog_fetch < 3600):
            return self._catalog_cache

        try:
            cat_url = "https://miportal.entel.pe/personas/catalogo/postpago/portabilidad"
            req = urllib.request.Request(cat_url, headers=self._headers)
            with urllib.request.urlopen(req, timeout=10, context=self._ssl_ctx) as resp:
                content = resp.read().decode("utf-8", errors="ignore")

            links = re.findall(
                r'<a class="footer__links semantic-link"\s+href="([^"]+)"\s+title="([^"]+)">',
                content
            )
            if links:
                # Store (title, url)
                self._catalog_cache = [(t.strip(), l.strip()) for l, t in links if "producto/equipos" in l]
                self._last_catalog_fetch = now
        except Exception as e:
            print(f"[EntelScraper Catalog Error]: {e}")

        return self._catalog_cache

    def _fetch_product_details_sync(self, title: str, link: str) -> Optional[ProductItem]:
        try:
            req = urllib.request.Request(link, headers=self._headers)
            with urllib.request.urlopen(req, timeout=8, context=self._ssl_ctx) as resp:
                html = resp.read().decode("utf-8", errors="ignore")

            scripts = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.DOTALL)
            for s in scripts:
                if '"@type":"Product"' in s or '"@type": "Product"' in s:
                    data = json.loads(s)
                    offers = data.get("offers", {})
                    raw_price = offers.get("price")
                    if not raw_price:
                        continue

                    try:
                        price = float(str(raw_price).replace(",", "").strip())
                    except ValueError:
                        continue

                    if price <= 0:
                        continue

                    name = data.get("name") or title
                    brand = data.get("brand", "")
                    if isinstance(brand, dict):
                        brand = brand.get("name", "")

                    image_url = data.get("image", "")
                    cond = detect_condition(name)
                    prod_id = data.get("sku") or re.search(r'prod\d+', link).group(0) if re.search(r'prod\d+', link) else f"entel-{len(link)}"

                    return ProductItem(
                        id=f"entel-{prod_id}",
                        title=name,
                        brand=brand,
                        price=price,
                        original_price=None,
                        discount_percent=None,
                        currency="PEN",
                        store=self.store_name,
                        store_id=self.store_id,
                        store_color=self.store_color,
                        url=link,
                        image_url=image_url,
                        in_stock=True,
                        condition=cond
                    )
        except Exception as e:
            print(f"[EntelScraper Product Error {link}]: {e}")

        return None

    async def search(self, query: str, client: httpx.AsyncClient) -> List[ProductItem]:
        items: List[ProductItem] = []
        try:
            # 1. Get or update catalog links
            catalog = await asyncio.to_thread(self._get_catalog_sync)
            if not catalog:
                return items

            # 2. Filter matching phone models in catalog
            matching_links = [
                (title, url) for title, url in catalog
                if matches_query_keywords(title, query)
            ][:25]

            if not matching_links:
                return items

            # 3. Fetch product details concurrently
            tasks = [asyncio.to_thread(self._fetch_product_details_sync, title, url) for title, url in matching_links]
            fetched = await asyncio.gather(*tasks, return_exceptions=True)

            for prod in fetched:
                if isinstance(prod, ProductItem) and prod is not None:
                    items.append(prod)

        except Exception as e:
            print(f"[EntelScraper Error]: {e}")

        return items
