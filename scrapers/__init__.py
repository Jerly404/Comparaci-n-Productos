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
from .filter_utils import is_valid_phone_item, is_phone_accessory, matches_query_keywords

__all__ = [
    "ProductItem",
    "BaseScraper",
    "FalabellaScraper",
    "RipleyScraper",
    "PlazaVeaScraper",
    "CoolboxScraper",
    "OechsleScraper",
    "PromartScraper",
    "HiraokaScraper",
    "ClaroScraper",
    "EntelScraper",
    "LaCuracaoScraper",
    "TiendasEfeScraper",
    "ShopstarScraper",
    "is_valid_phone_item",
    "is_phone_accessory",
    "matches_query_keywords"
]
