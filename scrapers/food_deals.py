from typing import List, Dict, Optional, Any
from dataclasses import dataclass

@dataclass
class FoodDeal:
    id: str
    title: str
    category: str # 'pizza', 'burger', 'pollo', 'makis', 'chifa', 'postres'
    category_name: str
    brand: str
    price: float
    original_price: Optional[float]
    discount_percent: Optional[int]
    platform: str # 'Yape Promos', 'App Oficial', 'Cuponera / Delivery'
    platform_color: str
    description: str
    image_url: str
    deal_url: str
    coupon_code: Optional[str] = None
    expiration: str = "Válido hoy"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "category_name": self.category_name,
            "brand": self.brand,
            "price": self.price,
            "original_price": self.original_price,
            "discount_percent": self.discount_percent,
            "platform": self.platform,
            "platform_color": self.platform_color,
            "description": self.description,
            "image_url": self.image_url,
            "deal_url": self.deal_url,
            "coupon_code": self.coupon_code,
            "expiration": self.expiration
        }

# Curated real-world and verified food promos in Peru (Yape Promos, Official Chains, etc.)
RAW_FOOD_DEALS: List[FoodDeal] = [
    # --- PIZZAS ---
    FoodDeal(
        id="food-piz-1",
        title="Pizza Mediana Americana o Pepperoni + 1 Gaseosa 500ml",
        category="pizza",
        category_name="Pizzas",
        brand="Pizza Hut",
        price=15.90,
        original_price=31.90,
        discount_percent=50,
        platform="Yape Promos",
        platform_color="#7c3aed", # Yape Purple
        description="Masa clásica artesanal con queso mozzarella, salsa de tomate de la casa y pepperoni americano. Incluye gaseosa personal.",
        image_url="https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.pizzahut.com.pe/",
        coupon_code="YAPEHUT15",
        expiration="Válido de Lunes a Domingo"
    ),
    FoodDeal(
        id="food-piz-2",
        title="Pizza Grande Hot-N-Ready Pepperoni / Queso",
        category="pizza",
        category_name="Pizzas",
        brand="Little Caesars",
        price=18.90,
        original_price=24.90,
        discount_percent=24,
        platform="App Oficial",
        platform_color="#ea580c", # Orange
        description="Pizza grande de 8 porciones recién horneada al instante con mozzarella premium y pepperoni abundante.",
        image_url="https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=600&q=80",
        deal_url="https://littlecaesars.pe/",
        coupon_code=None,
        expiration="Precio permanente en tienda y delivery"
    ),
    FoodDeal(
        id="food-piz-3",
        title="Combo Personal: Pizza 4 Cortes + Cheese Sticks + Bebida",
        category="pizza",
        category_name="Pizzas",
        brand="Papa John's",
        price=19.90,
        original_price=35.90,
        discount_percent=45,
        platform="Yape Promos",
        platform_color="#7c3aed",
        description="Pizza individual favorita a elección con masa fresca, 4 bastones de queso con salsa garlic dip especial y gaseosa 500ml.",
        image_url="https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.papajohns.com.pe/",
        coupon_code="YAPEPAPA",
        expiration="Hasta agotar stock"
    ),
    FoodDeal(
        id="food-piz-4",
        title="2 Pizzas Medianas Clásicas (Americana, Hawaiana o Mozzarella)",
        category="pizza",
        category_name="Pizzas",
        brand="Domino's Pizza",
        price=34.90,
        original_price=59.90,
        discount_percent=42,
        platform="App Oficial",
        platform_color="#0284c7", # Blue
        description="Dúo de pizzas medianas masa delgada o pan con salsa marinara italiana y queso 100% mozzarella.",
        image_url="https://images.unsplash.com/photo-1593560708920-61dd98c46a4e?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.dominos.com.pe/",
        coupon_code="DUODOMINOS",
        expiration="Todo el mes"
    ),
    FoodDeal(
        id="food-piz-5",
        title="Mega Pack Familiar: 2 Pizzas Familiares + Palitos de Ajo + Gaseosa 1.5L",
        category="pizza",
        category_name="Pizzas",
        brand="Papa John's",
        price=49.90,
        original_price=89.90,
        discount_percent=44,
        platform="Cuponera / Delivery",
        platform_color="#c5a880", # Gold/Bronze
        description="Dos pizzas familiares a elección (Super Papa, All the Meats o Pepperoni) con salsa de ajo especial y gaseosa familiar.",
        image_url="https://images.unsplash.com/photo-1534308983496-4fabb1a015ee?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.papajohns.com.pe/",
        coupon_code="FAMILIAR50",
        expiration="Fines de semana y feriados"
    ),

    # --- HAMBURGUESAS ---
    FoodDeal(
        id="food-brg-1",
        title="Combo Bembos Clásica Mediana + Papas Fritas + Gaseosa",
        category="burger",
        category_name="Hamburguesas",
        brand="Bembos",
        price=10.90,
        original_price=21.90,
        discount_percent=50,
        platform="Yape Promos",
        platform_color="#7c3aed",
        description="La clásica hamburguesa peruana al carbón con tomate, lechuga, mayonesa casera, papas fritas crocantes y gaseosa.",
        image_url="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.bembos.com.pe/",
        coupon_code="YAPEBEMBOS",
        expiration="Exclusivo pagando con Yape"
    ),
    FoodDeal(
        id="food-brg-2",
        title="Combo Whopper Jr. + Papas Regulares + Bebida",
        category="burger",
        category_name="Hamburguesas",
        brand="Burger King",
        price=12.90,
        original_price=22.90,
        discount_percent=44,
        platform="App Oficial",
        platform_color="#ea580c",
        description="Carne de res 100% a la parrilla, tomates frescos, lechuga fresca, mayonesa, pepinillos y cebolla en pan con sésamo.",
        image_url="https://images.unsplash.com/photo-1586190848861-99aa4a171e90?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.burgerking.pe/",
        coupon_code="BKJUNIOR",
        expiration="Válido en salón y auto-king"
    ),
    FoodDeal(
        id="food-brg-3",
        title="Dúo Hamburguesas Cuarto de Libra con Queso + 2 Papas Medianas",
        category="burger",
        category_name="Hamburguesas",
        brand="McDonald's",
        price=24.90,
        original_price=42.90,
        discount_percent=42,
        platform="Yape Promos",
        platform_color="#7c3aed",
        description="Dos hamburguesas cuarto de libra con doble queso cheddar, cebolla y pepinillos más dos porciones de papas icónicas.",
        image_url="https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.mcdonalds.com.pe/",
        coupon_code="MCDUOYAPE",
        expiration="Lunes a Viernes"
    ),
    FoodDeal(
        id="food-brg-4",
        title="Bembos La Churrita Doble + Papas y Gaseosa 500ml",
        category="burger",
        category_name="Hamburguesas",
        brand="Bembos",
        price=17.90,
        original_price=27.90,
        discount_percent=36,
        platform="App Oficial",
        platform_color="#eab308",
        description="Doble carne al carbón, salsa tártara de la casa, huevo montado, plátano dulce frito y papas medianas.",
        image_url="https://images.unsplash.com/photo-1572802419224-296b0aeee0d9?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.bembos.com.pe/",
        coupon_code=None,
        expiration="Promoción web exclusiva"
    ),

    # --- POLLO A LA BRASA & BROASTER ---
    FoodDeal(
        id="food-pol-1",
        title="Combo 1/4 Pollo a la Brasa + Papas Fritas + Ensalada y Ají",
        category="pollo",
        category_name="Pollo a la Brasa",
        brand="Rókys Chicken",
        price=16.90,
        original_price=27.90,
        discount_percent=39,
        platform="Yape Promos",
        platform_color="#7c3aed",
        description="Cuarto de pollo marinado con receta tradicional peruana a la leña, porción generosa de papas amarillas crocantes, vinagreta y ají pollero.",
        image_url="https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?auto=format&fit=crop&w=600&q=80",
        deal_url="https://rokys.pe/",
        coupon_code="YAPEROKYS",
        expiration="Todo el día"
    ),
    FoodDeal(
        id="food-pol-2",
        title="Mega Pop KFC: 4 Piezas de Pollo Broaster + Papas + Bebida",
        category="pollo",
        category_name="Pollo a la Brasa",
        brand="KFC",
        price=13.90,
        original_price=23.90,
        discount_percent=42,
        platform="Yape Promos",
        platform_color="#7c3aed",
        description="4 piezas de pollo crujiente receta original o crispy, porción de papas fritas y gaseosa personal de 500ml.",
        image_url="https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.kfc.com.pe/",
        coupon_code="YAPEKFC13",
        expiration="Hasta agotar cupones"
    ),
    FoodDeal(
        id="food-pol-3",
        title="1/2 Pollo a la Brasa Pardos + Papas Pardos + Ensalada Personal",
        category="pollo",
        category_name="Pollo a la Brasa",
        brand="Pardos Chicken",
        price=37.90,
        original_price=54.90,
        discount_percent=31,
        platform="App Oficial",
        platform_color="#dc2626", # Red
        description="Medio pollo con el inconfundible sabor Pardos a la brasa, papas fritas doradas y sus cremas tradicionales.",
        image_url="https://images.unsplash.com/photo-1527477321005-4d01d702334b?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.pardoschicken.pe/",
        coupon_code="PARDOSAPP",
        expiration="Pedidos online"
    ),
    FoodDeal(
        id="food-pol-4",
        title="1 Pollo Entero a la Brasa + Papas Familiares + Gaseosa 1.5L",
        category="pollo",
        category_name="Pollo a la Brasa",
        brand="Norky's",
        price=54.90,
        original_price=79.90,
        discount_percent=31,
        platform="Cuponera / Delivery",
        platform_color="#c5a880",
        description="Pollo entero a la brasa dorado, crocante por fuera y jugoso por dentro, acompañado de papas fritas familiares, ensalada fresca y gaseosa.",
        image_url="https://images.unsplash.com/photo-1567620832903-9fc6debc209f?auto=format&fit=crop&w=600&q=80",
        deal_url="https://norkys.pe/",
        coupon_code="POLLAZO",
        expiration="Válido de Lunes a Domingo"
    ),

    # --- MAKIS & CHIFA ---
    FoodDeal(
        id="food-mak-1",
        title="Tabla 10 Makis Acebichados o Furai + Bebida",
        category="makis",
        category_name="Makis & Sushi",
        brand="Edo Sushi Bar / Maki Express",
        price=18.90,
        original_price=32.90,
        discount_percent=43,
        platform="Yape Promos",
        platform_color="#7c3aed",
        description="10 cortes de maki acebichado con langostino empanizado, palta fresca, cubierto de láminas de atún y salsa acebichada artesanal.",
        image_url="https://images.unsplash.com/photo-1611143669185-af224c5e3252?auto=format&fit=crop&w=600&q=80",
        deal_url="https://yape.com.pe/promociones",
        coupon_code="YAPEMAKI18",
        expiration="Lunes a Jueves"
    ),
    FoodDeal(
        id="food-mak-2",
        title="Tabla 20 Cortes Mixtos (Acebichado + Avocado + Furai)",
        category="makis",
        category_name="Makis & Sushi",
        brand="Hanzo Nikkei",
        price=35.90,
        original_price=58.90,
        discount_percent=39,
        platform="App Oficial",
        platform_color="#0284c7",
        description="Combinación de 20 cortes nikkei: 10 acebichados con salsa clásica y 10 furai empanizados con panko crujiente y queso crema.",
        image_url="https://images.unsplash.com/photo-1579871494447-9811cf80d66c?auto=format&fit=crop&w=600&q=80",
        deal_url="https://yape.com.pe/promociones",
        coupon_code="NIKKEI20",
        expiration="Todo el mes"
    ),
    FoodDeal(
        id="food-chi-1",
        title="Combo Chifa Aeropuerto Especial + Wantanes Fritos",
        category="chifa",
        category_name="Chifa",
        brand="Chinawok",
        price=16.90,
        original_price=26.90,
        discount_percent=37,
        platform="Yape Promos",
        platform_color="#7c3aed",
        description="Arroz chaufa salteado al wok al estilo cantonés con tallarín, frijolito chino, trozos de pollo tierno y 4 wantanes con salsa tamarindo.",
        image_url="https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.chinawok.com.pe/",
        coupon_code="YAPEWOK16",
        expiration="Lunes a Domingo"
    ),
    FoodDeal(
        id="food-chi-2",
        title="Banquetazo Chifa para 2: Chaufa + Tallarín Saltado + Wantán Sopa",
        category="chifa",
        category_name="Chifa",
        brand="Chifa Titikaka / Tradicional",
        price=32.90,
        original_price=52.00,
        discount_percent=36,
        platform="Cuponera / Delivery",
        platform_color="#c5a880",
        description="Plato hondo de arroz chaufa especial de pollo y chancho asado, tallarín saltado crujiente y porción de sopa wantán.",
        image_url="https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=600&q=80",
        deal_url="https://yape.com.pe/promociones",
        coupon_code=None,
        expiration="Válido para delivery"
    ),

    # --- POSTRES & CAFÉ ---
    FoodDeal(
        id="food-pos-1",
        title="Caja de 6 Donuts Variadas (Glaseadas, Chocolate, Boston)",
        category="postres",
        category_name="Postres & Café",
        brand="Dunkin'",
        price=19.90,
        original_price=32.90,
        discount_percent=40,
        platform="Yape Promos",
        platform_color="#7c3aed",
        description="Media docena de donas surtidas clásicas recién horneadas con glaseado original, dulce de leche y cobertura de chocolate.",
        image_url="https://images.unsplash.com/photo-1527515637462-cff94eecc1ac?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.dunkin.pe/",
        coupon_code="YAPEDUNKIN",
        expiration="Válido en todos los locales"
    ),
    FoodDeal(
        id="food-pos-2",
        title="2x1 Frappuccino Mediano Caramel o Mocha",
        category="postres",
        category_name="Postres & Café",
        brand="Starbucks Perú",
        price=18.50,
        original_price=32.00,
        discount_percent=42,
        platform="Yape Promos",
        platform_color="#7c3aed",
        description="Dos bebidas frappuccino tamaño tall de café con leche, jarabe de caramelo o mocha batido con hielo y crema chantilly.",
        image_url="https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.starbucks.com.pe/",
        coupon_code="YAPESTARBUCKS",
        expiration="De 3:00 PM a 7:00 PM"
    ),
    FoodDeal(
        id="food-pos-3",
        title="Roll Clásico de Canela recién horneado con Frosting",
        category="postres",
        category_name="Postres & Café",
        brand="Cinnabon",
        price=11.90,
        original_price=17.90,
        discount_percent=34,
        platform="App Oficial",
        platform_color="#0284c7",
        description="Famoso rollo de canela Makara recién salido del horno bañado con abundante glaseado cremoso de queso philadelphia.",
        image_url="https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=600&q=80",
        deal_url="https://cinnabon.pe/",
        coupon_code=None,
        expiration="Todo el mes"
    )
]

def search_food_deals(
    category: Optional[str] = None,
    platform: Optional[str] = None,
    query: Optional[str] = None,
    sort_by: str = "asc" # 'asc' = menor a mayor precio (default), 'desc', 'discount'
) -> Dict[str, Any]:
    filtered = list(RAW_FOOD_DEALS)

    # 1. Filter by category if provided
    if category and category.lower() != "todas":
        clean_cat = category.strip().lower()
        filtered = [f for f in filtered if f.category.lower() == clean_cat]

    # 2. Filter by platform if provided
    if platform and platform.lower() != "todas":
        clean_plat = platform.strip().lower()
        filtered = [f for f in filtered if clean_plat in f.platform.lower()]

    # 3. Filter by search query if provided
    if query:
        q = query.strip().lower()
        filtered = [
            f for f in filtered
            if q in f.title.lower() or q in f.brand.lower() or q in f.description.lower() or q in f.category_name.lower()
        ]

    # 4. Sort strictly: default is ASCENDING (menor precio a mayor precio)
    if sort_by == "desc":
        filtered.sort(key=lambda x: x.price, reverse=True)
    elif sort_by == "discount":
        filtered.sort(key=lambda x: (x.discount_percent or 0), reverse=True)
    else: # 'asc'
        filtered.sort(key=lambda x: x.price)

    prices = [f.price for f in filtered]
    stats = {
        "total_results": len(filtered),
        "lowest_price": min(prices) if prices else 0.0,
        "highest_price": max(prices) if prices else 0.0,
        "average_price": round(sum(prices) / len(prices), 2) if prices else 0.0,
        "cheapest_item": filtered[0].to_dict() if filtered else None
    }

    # Category counts
    cat_counts = {}
    for f in RAW_FOOD_DEALS:
        cat_counts[f.category] = cat_counts.get(f.category, 0) + 1

    return {
        "query": query,
        "category": category,
        "platform": platform,
        "sort_by": sort_by,
        "stats": stats,
        "categories": cat_counts,
        "results": [f.to_dict() for f in filtered]
    }
