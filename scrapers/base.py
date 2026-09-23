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
    deal_verdict: str = "Precio Normal" # "Mínimo Histórico", "Buen Precio", "Precio Normal"
    payment_method: str = "Cualquier Tarjeta / Yape" # "Cualquier Tarjeta / Yape", "Tarjeta CMR", "Tarjeta Ripley", "Tarjeta Oh!"
    card_name: Optional[str] = None
    pickup_cajamarca: bool = False
    pickup_location: str = "Envío a Domicilio" # "El Quinde Cajamarca", "Real Plaza Cajamarca", "Envío courier a Cajamarca"
    installments_12x: Optional[float] = None
    installments_info: Optional[str] = None
    specs: Optional[dict] = None

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
            "condition": self.condition,
            "deal_verdict": self.deal_verdict,
            "payment_method": self.payment_method,
            "card_name": self.card_name,
            "pickup_cajamarca": self.pickup_cajamarca,
            "pickup_location": self.pickup_location,
            "installments_12x": self.installments_12x,
            "installments_info": self.installments_info,
            "specs": self.specs or {}
        }

class BaseScraper(ABC):
    store_name: str
    store_id: str
    store_color: str

    @abstractmethod
    async def search(self, query: str, client: httpx.AsyncClient) -> List[ProductItem]:
        """Search products for a query asynchronously."""
        pass
