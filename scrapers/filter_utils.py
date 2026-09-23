import re
from typing import List

# Words indicating true device accessories/parts that should be filtered out when hide_accessories is active
ACCESSORY_KEYWORDS = [
    "funda", "case", "carcasa", "cover", "protector", "estuche", "skin",
    "cargador", "charger", "cable", "adaptador", "adapter",
    "mica", "vidrio templado", "tempered glass", "lamina", "lámina", "hidrogel",
    "soporte para auto", "soporte", "holder", "tripode", "trípode",
    "bateria externa", "batería externa", "powerbank", "power bank",
    "repuesto", "pantalla de repuesto", "pantalla lcd", "display", "bateria para", "batería para",
    "tapa trasera", "flex", "conector", "correa para reloj", "lente de camara", "lente para cámara"
]

GENERIC_STOP_WORDS = {
    'de', 'el', 'la', 'con', 'para', 'en', 'los', 'las', 'un', 'una',
    'nuevo', 'original', 'producto', 'tienda'
}

FASHION_KEYWORDS = [
    "polo", "polos", "polera", "poleras", "camisa", "camisas", "camiseta", "camisetas",
    "pantalon", "pantalones", "pantalón", "jean", "jeans", "denim", "casaca", "casacas",
    "chompa", "chompas", "abrigo", "abrigos", "vestido", "vestidos", "falda", "faldas",
    "short", "shorts", "bermuda", "bermudas", "blusa", "blusas", "top", "tops",
    "legging", "leggings", "buzo", "buzos", "jogger", "joggers", "ropa", "moda",
    "calzado", "zapatilla", "zapatillas", "zapato", "zapatos", "sandalia", "sandalias",
    "calcetines", "medias", "boxer", "truza", "bikini", "hm", "h&m", "ralph lauren", "lauren",
    "topitop", "zara", "mango", "lacoste", "tommy", "hilfiger", "gucci", "calvin klein",
    "nike", "adidas", "puma", "reebok", "marathon", "quiksilver", "levis", "marquis",
    "index", "basement", "sybilla", "tex", "perfume", "fragancia", "colonia"
]

PHONE_KEYWORDS = [
    "celular", "celulares", "smartphone", "smartphones", "telefono", "telefonos",
    "iphone", "galaxy", "xiaomi", "redmi", "poco", "motorola", "moto", "oppo", "honor",
    "realme", "pixel"
]

def clean_text(text: str) -> str:
    """Normalize text by lowering, stripping accents and standardizing spacing."""
    text = text.lower()
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u', 'ñ': 'n'
    }
    for orig, rep in replacements.items():
        text = text.replace(orig, rep)
    
    # Normalize patterns like "h & m" or "h&m" to "hm" for consistent matching
    text = re.sub(r'\bh\s*&\s*m\b', 'hm', text)
    # Normalize patterns like "s 24" -> "s24" or "z flip" -> "zflip"
    text = re.sub(r'\b([a-z])\s+(\d+)\b', r'\1\2', text)
    return text

def is_phone_query(query: str) -> bool:
    norm = clean_text(query)
    if any(clean_text(pk) in norm for pk in PHONE_KEYWORDS):
        return True
    if re.search(r'\b[saz]\d{1,2}(?:fe|ultra|plus|\+)?\b', norm):
        return True
    if re.search(r'\b(?:pro\s*max|promax)\b', norm):
        return True
    return False

def is_fashion_query(query: str) -> bool:
    norm = clean_text(query)
    return any(clean_text(fk) in norm for fk in FASHION_KEYWORDS)

def is_phone_accessory(title: str, query: str) -> bool:
    """
    Returns True if the product is an accessory/case/cable/etc.,
    UNLESS the user specifically asked for that accessory in the query.
    """
    norm_title = clean_text(title)
    norm_query = clean_text(query)

    for word in ACCESSORY_KEYWORDS:
        clean_word = clean_text(word)
        if clean_word in norm_title:
            if clean_word in norm_query:
                continue
            return True
    return False

def matches_query_keywords(title: str, query: str, brand: str = "") -> bool:
    """
    Ensures that key terms from the query are present in the title or brand.
    Handles brand names, model numbers, and multi-word product names gracefully.
    """
    full_text = f"{title} {brand}".strip() if brand else title
    norm_title = clean_text(full_text)
    norm_query = clean_text(query)

    # Split into meaningful tokens excluding generic words
    raw_tokens = re.split(r'\s+', norm_query)
    tokens = [t for t in raw_tokens if len(t) >= 2 and t not in GENERIC_STOP_WORDS]
    if not tokens:
        tokens = [t for t in raw_tokens if len(t) >= 2]
    if not tokens:
        return True

    # 1. Model number checks (e.g. '13', 's24', 's24fe', '15')
    numeric_tokens = [t for t in tokens if re.search(r'\d', t)]
    for num_token in numeric_tokens:
        digit_only = re.sub(r'\D', '', num_token)
        if num_token not in norm_title and digit_only not in norm_title:
            return False

    # 2. Textual tokens check (e.g. 'samsung', 'galaxy', 'polo', 'ralph', 'lauren')
    text_tokens = [t for t in tokens if not re.search(r'^\d+$', t) and t not in numeric_tokens]
    if not text_tokens:
        return True

    # Check how many key text tokens appear in title or brand
    matched_count = sum(1 for t in text_tokens if t in norm_title)

    # Special qualifiers like 'fe', 'pro', 'ultra', 'plus', 'max', 'mini', 'lite'
    key_qualifiers = {'fe', 'pro', 'ultra', 'plus', 'max', 'mini', 'lite'}
    for qual in key_qualifiers:
        if qual in text_tokens and qual not in norm_title:
            return False

    # If 1 text token, it must match
    if len(text_tokens) == 1:
        return matched_count >= 1

    # If multiple text tokens, at least 50% must match (e.g. "polo ralph lauren" or "samsung galaxy s24")
    return (matched_count / len(text_tokens)) >= 0.50

def detect_condition(title: str) -> str:
    """Detects whether product is new, refurbished, or open box."""
    norm = clean_text(title)
    if any(k in norm for k in ["reacondicionado", "refurbished", "seminuevo", "semi-nuevo", "open box", "outlet"]):
        return "Reacondicionado"
    return "Nuevo"

def is_valid_phone_item(title: str, query: str, price: float, brand: str = "", hide_accessories: bool = True, min_price: float = 120.0) -> bool:
    """Validates if an item is a relevant result for phones, fashion, or general products."""
    if not title or price <= 0:
        return False

    phone_search = is_phone_query(query)
    fashion_search = is_fashion_query(query)

    # Phone accessories are only filtered out if this is actually a phone search
    if hide_accessories and phone_search and not fashion_search:
        if is_phone_accessory(title, query):
            return False
        norm_query = clean_text(query)
        is_accessory_query = any(clean_text(w) in norm_query for w in ACCESSORY_KEYWORDS)
        if not is_accessory_query and price < min_price:
            return False
    elif not phone_search or fashion_search:
        # For fashion and general products, valid items can be affordable (e.g. S/ 5 - 100)
        if price < 2.0:
            return False

    return matches_query_keywords(title, query, brand=brand)
