import re
from typing import List

# Words indicating true device accessories/parts that should be filtered out when hide_accessories is active
ACCESSORY_KEYWORDS = [
    "funda", "case", "carcasa", "cover", "protector", "estuche", "skin",
    "cargador", "charger", "cable", "adaptador", "adapter", "dock",
    "mica", "vidrio templado", "tempered glass", "lamina", "lámina", "hidrogel",
    "soporte", "holder", "tripode", "trípode", "anillo",
    "bateria externa", "batería externa", "powerbank", "power bank",
    "repuesto", "pantalla de repuesto", "pantalla lcd", "display", "bateria para", "batería para",
    "tapa trasera", "flex", "conector", "correa para reloj", "lente de camara", "lente para cámara",
    "mochila", "backpack", "maletin", "maletín", "bolso para", "funda para"
]

GENERIC_STOP_WORDS = {
    'de', 'el', 'la', 'con', 'para', 'en', 'los', 'las', 'un', 'una',
    'nuevo', 'original', 'producto', 'tienda'
}

def clean_text(text: str) -> str:
    """Normalize text by lowering, stripping accents and standardizing spacing."""
    text = text.lower()
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u', 'ñ': 'n'
    }
    for orig, rep in replacements.items():
        text = text.replace(orig, rep)
    
    # Normalize patterns like "s 24" -> "s24" or "z flip" -> "zflip"
    text = re.sub(r'\b([a-z])\s+(\d+)\b', r'\1\2', text)
    return text

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

def matches_query_keywords(title: str, query: str) -> bool:
    """
    Ensures that key terms from the query are present in the title.
    Handles brand names, model numbers, and multi-word product names gracefully.
    """
    norm_title = clean_text(title)
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
        # Check if num_token or just the digit part is present in title
        digit_only = re.sub(r'\D', '', num_token)
        if num_token not in norm_title and digit_only not in norm_title:
            return False

    # 2. Textual tokens check (e.g. 'samsung', 'galaxy', 'ultra', 'fe', 'pro')
    text_tokens = [t for t in tokens if not re.search(r'^\d+$', t) and t not in numeric_tokens]
    if not text_tokens:
        return True

    # Check how many key text tokens appear in title
    matched_count = sum(1 for t in text_tokens if t in norm_title)

    # Special qualifiers like 'fe', 'pro', 'ultra', 'plus', 'max', 'mini', 'lite'
    key_qualifiers = {'fe', 'pro', 'ultra', 'plus', 'max', 'mini', 'lite'}
    for qual in key_qualifiers:
        if qual in text_tokens and qual not in norm_title:
            return False

    # If 1 text token, it must match
    if len(text_tokens) == 1:
        return matched_count >= 1

    # If multiple text tokens, at least 50% must match (e.g. "samsung galaxy s24" only needs "samsung" or "galaxy" + "s24")
    return (matched_count / len(text_tokens)) >= 0.50

def detect_condition(title: str) -> str:
    """Detects whether product is new, refurbished, or open box."""
    norm = clean_text(title)
    if any(k in norm for k in ["reacondicionado", "refurbished", "seminuevo", "semi-nuevo", "open box", "outlet"]):
        return "Reacondicionado"
    return "Nuevo"

def is_valid_phone_item(title: str, query: str, price: float, hide_accessories: bool = True, min_price: float = 120.0) -> bool:
    """Validates if an item is a relevant phone result."""
    if not title or price <= 0:
        return False

    if hide_accessories:
        if is_phone_accessory(title, query):
            return False
        norm_query = clean_text(query)
        is_accessory_query = any(clean_text(w) in norm_query for w in ACCESSORY_KEYWORDS)
        if not is_accessory_query and price < min_price:
            return False

    return matches_query_keywords(title, query)
