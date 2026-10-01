import re
from typing import List, Optional

# Words indicating true device accessories/parts that should be filtered out when hide_accessories is active
ACCESSORY_KEYWORDS = [
    "funda", "fundas", "case", "cases", "carcasa", "carcasas", "cover", "protector", "protectores", "estuche", "skin",
    "cargador", "cargadores", "charger", "cable", "cables", "adaptador", "adapter", "dock",
    "mica", "micas", "vidrio templado", "tempered glass", "lamina", "lámina", "hidrogel",
    "soporte para auto", "soporte", "holder", "tripode", "trípode", "ring", "anillo",
    "bateria externa", "batería externa", "powerbank", "power bank",
    "repuesto", "pantalla de repuesto", "pantalla lcd", "display", "bateria para", "batería para",
    "tapa trasera", "flex", "conector", "correa para reloj", "correa", "lente de camara", "lente para cámara",
    "kit de video", "kit", "filtro nd", "filtro", "jaula", "rig", "parasol"
]

GENERIC_STOP_WORDS = {
    'de', 'el', 'la', 'con', 'para', 'en', 'los', 'las', 'un', 'una',
    'nuevo', 'original', 'producto', 'tienda', 'color'
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

KNOWN_BRANDS_AND_DEVICES = {
    "iphone": ["iphone", "apple"],
    "ipad": ["ipad", "apple"],
    "macbook": ["macbook", "apple"],
    "airpods": ["airpods", "apple"],
    "apple watch": ["apple watch", "watch", "apple"],
    "samsung": ["samsung", "galaxy"],
    "galaxy": ["samsung", "galaxy"],
    "xiaomi": ["xiaomi", "redmi", "poco"],
    "redmi": ["redmi", "xiaomi"],
    "poco": ["poco", "xiaomi"],
    "motorola": ["motorola", "moto"],
    "moto": ["motorola", "moto"],
    "oppo": ["oppo"],
    "honor": ["honor"],
    "pixel": ["pixel", "google"],
    "huawei": ["huawei"],
    "playstation": ["playstation", "ps5", "ps4"],
    "ps5": ["ps5", "playstation 5", "playstation"],
    "ps4": ["ps4", "playstation 4", "playstation"],
    "nintendo": ["nintendo", "switch"],
    "switch": ["nintendo", "switch"],
    "xbox": ["xbox"],
    "jbl": ["jbl"],
    "bose": ["bose"],
    "sony": ["sony"],
    "lenovo": ["lenovo"],
    "asus": ["asus"],
    "acer": ["acer"],
    "hp": ["hp"],
    "dell": ["dell"],
    "lg": ["lg"],
    "tcl": ["tcl"],
    "hisense": ["hisense"],
    "ralph lauren": ["ralph lauren", "lauren"],
    "polo ralph lauren": ["ralph lauren", "lauren"],
    "hm": ["hm", "h&m"],
    "h&m": ["hm", "h&m"],
    "topitop": ["topitop"],
    "zara": ["zara"],
    "mango": ["mango"],
    "nike": ["nike"],
    "adidas": ["adidas"],
    "puma": ["puma"],
    "reebok": ["reebok"],
    "marathon": ["marathon"]
}

KEY_QUALIFIERS = {'fe', 'pro', 'ultra', 'plus', 'max', 'mini', 'lite'}

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
        if re.search(r'\b' + re.escape(clean_word) + r'\b', norm_title):
            if not re.search(r'\b' + re.escape(clean_word) + r'\b', norm_query):
                return True
    return False

def matches_query_keywords(title: str, query: str, brand: str = "") -> bool:
    """
    Ensures that key terms from the query are present in the title or brand.
    Enforces brand identity, model numbers, and qualifiers using strict whole-word matching.
    """
    full_text = f"{title} {brand}".strip() if brand else title
    norm_title = clean_text(full_text)
    norm_query = clean_text(query)

    # 1. Enforce known brand / primary device constraint
    for key, synonyms in KNOWN_BRANDS_AND_DEVICES.items():
        if re.search(r'\b' + re.escape(key) + r'\b', norm_query):
            if not any(re.search(r'\b' + re.escape(syn) + r'\b', norm_title) for syn in synonyms):
                return False

    # 2. Number / model constraint (e.g. '15' in iPhone 15, '24' in S24, '5' in PS5)
    num_tokens = re.findall(r'\b\d+\b', norm_query)
    for n in num_tokens:
        if not re.search(r'\b' + n + r'\b', norm_title):
            return False
        # If all matches of this number in the title are followed by measurement units (kg, libras, horas, etc.), reject
        all_matches = list(re.finditer(r'\b' + n + r'\b', norm_title))
        unit_matches = list(re.finditer(r'\b' + n + r'\s*(?:kg|kilos?|libras?|lbs?|horas?|hrs?|g|mg|watts?|w|ml|oz|cm|mm|m)\b', norm_title))
        if len(all_matches) == len(unit_matches):
            return False

    # 3. Model qualifiers (fe, pro, ultra, plus, max, mini, lite) - MUST match as whole word
    for qual in KEY_QUALIFIERS:
        if re.search(r'\b' + qual + r'\b', norm_query):
            if not re.search(r'\b' + qual + r'\b', norm_title):
                return False

    # 4. Textual tokens check (excluding stopwords and numeric tokens)
    raw_tokens = re.split(r'\s+', norm_query)
    tokens = [t for t in raw_tokens if len(t) >= 2 and t not in GENERIC_STOP_WORDS and not re.search(r'^\d+$', t)]
    if not tokens:
        return True

    matched_count = 0
    for t in tokens:
        if re.search(r'\b' + re.escape(t) + r'\b', norm_title):
            matched_count += 1

    # Require high match percentage for non-stopwords
    return (matched_count / len(tokens)) >= 0.70

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

    # First verify keyword & brand & model relevance
    if not matches_query_keywords(title, query, brand=brand):
        return False

    # Phone accessories filtering
    if hide_accessories and phone_search and not fashion_search:
        if is_phone_accessory(title, query):
            return False
        norm_query = clean_text(query)
        is_accessory_query = any(clean_text(w) in norm_query for w in ACCESSORY_KEYWORDS)

        # Flagship phones have higher realistic price floors
        flagship_min = min_price
        if re.search(r'\biphone\s*(?:1[3-6]|x[sr]?)\b', norm_query):
            flagship_min = 600.0  # An iPhone 13-16 device is never < S/ 600 (accessories slip in otherwise)
        elif re.search(r'\bs2[3-5]\b', norm_query):
            flagship_min = 500.0

        if not is_accessory_query and price < flagship_min:
            return False
    elif not phone_search or fashion_search:
        # For fashion and general products, valid items can be affordable (e.g. S/ 5 - 100)
        if price < 2.0:
            return False

    return True
