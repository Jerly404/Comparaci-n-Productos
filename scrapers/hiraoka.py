import re
from urllib.parse import quote
from typing import List
import httpx
from bs4 import BeautifulSoup
from .base import BaseScraper, ProductItem
from .filter_utils import detect_condition

class HiraokaScraper(BaseScraper):
    store_name = "Hiraoka"
    store_id = "hiraoka"
    store_color = "#dc2626" # Brand Red

    async def search(self, query: str, client: httpx.AsyncClient) -> List[ProductItem]:
        items: List[ProductItem] = []
        try:
            url = f"https://hiraoka.com.pe/catalogsearch/result/?q={quote(query)}"
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Accept-Language": "es-PE,es;q=0.9,en;q=0.8"
            }
            resp = await client.get(url, headers=headers, timeout=12.0)
            if resp.status_code != 200:
                return items

            soup = BeautifulSoup(resp.text, "html.parser")
            cards = soup.select(".product-item")

            for card in cards:
                a_elem = card.select_one(".product-item-name a") or card.select_one(".product-item-link")
                if not a_elem:
                    continue

                title = a_elem.get("title") or a_elem.get_text(strip=True)
                prod_url = a_elem.get("href", "")

                # Image
                img_elem = card.select_one(".product-image-photo")
                image_url = img_elem.get("src", "") if img_elem else ""

                # Final Price
                final_elem = card.select_one('[data-price-type="finalPrice"] .price') or card.select_one(".special-price .price") or card.select_one(".price")
                if not final_elem:
                    continue

                raw_final = re.sub(r"[^\d.]", "", final_elem.get_text().replace(",", "").strip())
                try:
                    price = float(raw_final)
                except ValueError:
                    continue

                if price <= 0:
                    continue

                # Old Price
                original_price = None
                old_elem = card.select_one('[data-price-type="oldPrice"] .price') or card.select_one(".old-price .price")
                if old_elem:
                    raw_old = re.sub(r"[^\d.]", "", old_elem.get_text().replace(",", "").strip())
                    try:
                        parsed_old = float(raw_old)
                        if parsed_old > price:
                            original_price = parsed_old
                    except ValueError:
                        pass

                discount_percent = None
                if original_price and original_price > price:
                    discount_percent = round((1 - (price / original_price)) * 100)

                # Brand
                brand = ""
                brand_elem = card.select_one(".product-item-brand")
                if brand_elem:
                    brand = brand_elem.get_text(strip=True)

                cond = detect_condition(title)
                prod_id = card.get("data-product-id") or f"hiraoka-{len(items)+1}"

                items.append(ProductItem(
                    id=f"hiraoka-{prod_id}",
                    title=title,
                    brand=brand,
                    price=price,
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
            print(f"[HiraokaScraper Error]: {e}")

        return items
