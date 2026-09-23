from dataclasses import dataclass
from typing import Optional, List
from abc import ABC, abstractmethod
import httpx

@dataclass
class ProductItem:
    id: str
    title: str
    brand: str
    price: float
    original_price: Optional[float]
    discount_percent: Optional[int]
    currency: str
    store: str
    store_id: str
    store_color: str
    url: str
    image_url: str
    in_stock: bool = True
    condition: str = "Nuevo"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "brand": self.brand,
            "price": self.price,
            "original_price": self.original_price,
            "discount_percent": self.discount_percent,
            "currency": self.currency,
            "store": self.store,
            "store_id": self.store_id,
            "store_color": self.store_color,
            "url": self.url,
            "image_url": self.image_url,
            "in_stock": self.in_stock,
            "condition": self.condition
        }

class BaseScraper(ABC):
    store_name: str
    store_id: str
    store_color: str

    @abstractmethod
    async def search(self, query: str, client: httpx.AsyncClient) -> List[ProductItem]:
        """Search products for a query asynchronously."""
        pass
