from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
import copy

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
    platform: str # 'Yape Promos', 'Rappi', 'PedidosYa', 'App Oficial', 'Cuponera / Delivery'
    platform_color: str
    description: str
    image_url: str
    deal_url: str
    coupon_code: Optional[str] = None
    expiration: str = "Válido hoy"
    location: str = "Nacional (Lima y Provincias)"
    districts: List[str] = field(default_factory=list) # e.g. ["cajamarca", "miraflores", "arequipa"]
    is_promo: bool = True # True = oferta/descuento especial, False = carta regular/combo estándar
    delivery_time: str = "25-45 min"

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
            "expiration": self.expiration,
            "location": self.location,
            "districts": self.districts,
            "is_promo": self.is_promo,
            "delivery_time": self.delivery_time
        }

# Standard national district coverage for major restaurant chains present across Peru
ALL_PERU_DISTRICTS = [
    "cajamarca", "miraflores", "surco", "lima_centro", "lima_norte",
    "lima_sur", "lima_este", "callao", "arequipa", "trujillo",
    "chiclayo_piura", "cusco"
]

LIMA_ONLY_DISTRICTS = [
    "miraflores", "surco", "lima_centro", "lima_norte", "lima_sur", "lima_este", "callao"
]

LIMA_PREMIUM_DISTRICTS = [
    "miraflores", "surco", "lima_centro", "lima_sur"
]

CAJAMARCA_ONLY_DISTRICTS = [
    "cajamarca"
]

PROVINCE_MAJOR_DISTRICTS = [
    "cajamarca", "arequipa", "trujillo", "chiclayo_piura", "cusco"
]

# Comprehensive Catalog: Full Carta Menu & Active Verified Promotions
RAW_FOOD_DEALS: List[FoodDeal] = [
    # =========================================================================
    # --- 1. PIZZAS (CARTA COMPLETA + OFERTAS YAPE / RAPPI / APPS) ---
    # =========================================================================
    FoodDeal(
        id="piz-reg-1",
        title="Pizza Personal Americana (4 Cortes)",
        category="pizza",
        category_name="Pizzas",
        brand="Little Caesars",
        price=11.90,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#ea580c",
        description="Pizza personal individual horneada al momento con masa crujiente, salsa de tomate italiana y queso 100% mozzarella.",
        image_url="https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=600&q=80",
        deal_url="https://littlecaesars.pe/menu/",
        expiration="Carta habitual diaria",
        location="Cobertura Nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=False,
        delivery_time="20-30 min"
    ),
    FoodDeal(
        id="piz-reg-2",
        title="Palitroques con Salsa Bolognesa o Queso Parmesano",
        category="pizza",
        category_name="Pizzas",
        brand="Pizza Hut",
        price=12.90,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#dc2626",
        description="Porción de palitroques horneados dorados cubiertos con hierbas aromáticas y servidos con abundante salsa bolognesa.",
        image_url="https://images.unsplash.com/photo-1541745537411-b8046dc6d66c?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.pizzahut.com.pe/entradas",
        expiration="Carta permanente",
        location="Cajamarca, Lima y Provincias",
        districts=ALL_PERU_DISTRICTS,
        is_promo=False,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="piz-promo-1",
        title="Pizza Mediana Americana o Pepperoni + Gaseosa 500ml",
        category="pizza",
        category_name="Pizzas",
        brand="Pizza Hut",
        price=15.90,
        original_price=31.90,
        discount_percent=50,
        platform="Yape Promos",
        platform_color="#7c3aed",
        description="Masa clásica artesanal con abundante queso mozzarella, salsa italiana y pepperoni americano o jamón. Incluye gaseosa 500ml.",
        image_url="https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.pizzahut.com.pe/promociones",
        coupon_code="YAPEHUT15",
        expiration="Exclusivo pagando con Yape",
        location="El Quinde Cajamarca y a nivel nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=True,
        delivery_time="30-40 min"
    ),
    FoodDeal(
        id="piz-promo-2",
        title="Pizza Mediana Pepperoni Clásica + Garlic Sauce",
        category="pizza",
        category_name="Pizzas",
        brand="Papa John's / Rappi",
        price=17.90,
        original_price=34.90,
        discount_percent=49,
        platform="Rappi",
        platform_color="#ff441f",
        description="Pizza mediana recién salida del horno con masa fresca, pepperoni de primera calidad, queso mozzarella y su cremosa salsa de ajo.",
        image_url="https://images.unsplash.com/photo-1534308983496-4fabb1a015ee?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.rappi.com.pe/restaurantes/search?query=papa+johns+pepperoni",
        coupon_code="RAPPIPAPA",
        expiration="Lunes a Domingo en Rappi",
        location="Cajamarca, Lima, Arequipa, Trujillo",
        districts=ALL_PERU_DISTRICTS,
        is_promo=True,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="piz-reg-3",
        title="Pizza Grande Hot-N-Ready Pepperoni",
        category="pizza",
        category_name="Pizzas",
        brand="Little Caesars",
        price=18.90,
        original_price=24.90,
        discount_percent=24,
        platform="App Oficial",
        platform_color="#ea580c",
        description="Pizza grande familiar de 8 porciones recién salida del horno sin espera. Cubierta de mozzarella y pepperoni crujiente.",
        image_url="https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=600&q=80",
        deal_url="https://littlecaesars.pe/menu/",
        coupon_code=None,
        expiration="Precio permanente en tienda y delivery",
        location="Nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=True,
        delivery_time="20-30 min"
    ),
    FoodDeal(
        id="piz-promo-3",
        title="Combo Personal: Pizza 4 Cortes + Cheese Sticks + Bebida",
        category="pizza",
        category_name="Pizzas",
        brand="Papa John's",
        price=19.90,
        original_price=35.90,
        discount_percent=45,
        platform="Yape Promos",
        platform_color="#7c3aed",
        description="Pizza personal a elección con 4 bastones crocantes de queso mozzarella, salsa especial garlic dip y gaseosa helada.",
        image_url="https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.papajohns.com.pe/combos",
        coupon_code="YAPEPAPA",
        expiration="Hasta agotar cupones",
        location="Nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=True,
        delivery_time="30-40 min"
    ),
    FoodDeal(
        id="piz-reg-4",
        title="Pizza Familiar Hawaiana Jamón Glaseado & Piña",
        category="pizza",
        category_name="Pizzas",
        brand="Pizza Hut",
        price=32.90,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#dc2626",
        description="Pizza grande familiar con doble jamón glaseado seleccionado, trozos dulces de piña fresca y abundante queso mozzarella fundido.",
        image_url="https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.pizzahut.com.pe/pizzas",
        expiration="Carta habitual",
        location="El Quinde Cajamarca y sedes a nivel nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=False,
        delivery_time="30-40 min"
    ),
    FoodDeal(
        id="piz-promo-4",
        title="2 Pizzas Medianas Clásicas (Americana, Hawaiana o Mozzarella)",
        category="pizza",
        category_name="Pizzas",
        brand="Domino's Pizza",
        price=34.90,
        original_price=59.90,
        discount_percent=42,
        platform="App Oficial",
        platform_color="#0284c7",
        description="Dúo de pizzas medianas masa artesanal delgada o pan con salsa marinara italiana y queso 100% mozzarella de vaca.",
        image_url="https://images.unsplash.com/photo-1593560708920-61dd98c46a4e?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.dominos.com.pe/promociones",
        coupon_code="DUODOMINOS",
        expiration="Todo el mes",
        location="Cobertura Nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=True,
        delivery_time="30-40 min"
    ),
    FoodDeal(
        id="piz-reg-5",
        title="Pizza Familiar Especial The Works (Todas las Carnes & Vegetales)",
        category="pizza",
        category_name="Pizzas",
        brand="Papa John's",
        price=44.90,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#0284c7",
        description="Pepperoni, salchicha italiana, jamón canadiense, champiñones frescos, cebolla, pimientos verdes y aceitunas negras con queso mozzarella.",
        image_url="https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.papajohns.com.pe/pizzas",
        expiration="Carta permanente",
        location="Nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=False,
        delivery_time="30-45 min"
    ),
    FoodDeal(
        id="piz-promo-5",
        title="Mega Pack Familiar: 2 Pizzas Familiares + Palitos de Ajo + Gaseosa 1.5L",
        category="pizza",
        category_name="Pizzas",
        brand="Papa John's",
        price=49.90,
        original_price=89.90,
        discount_percent=44,
        platform="Cuponera / Delivery",
        platform_color="#c5a880",
        description="Dos pizzas familiares a elección (Super Papa, All The Meats o Pepperoni) con salsa garlic dip especial y gaseosa familiar de 1.5L.",
        image_url="https://images.unsplash.com/photo-1534308983496-4fabb1a015ee?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.papajohns.com.pe/promociones",
        coupon_code="FAMILIAR50",
        expiration="Fines de semana y feriados",
        location="Nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=True,
        delivery_time="35-45 min"
    ),

    # =========================================================================
    # --- 2. HAMBURGUESAS (CARTA COMPLETA + OFERTAS) ---
    # =========================================================================
    FoodDeal(
        id="brg-reg-1",
        title="Porción de Papas Fritas Amarillas Medianas Crocantes",
        category="burger",
        category_name="Hamburguesas",
        brand="Bembos",
        price=6.90,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#0284c7",
        description="Papas amarillas peruanas seleccionadas, fritas al punto exacto con crema tártara casera y mayonesa.",
        image_url="https://images.unsplash.com/photo-1576107232684-1279f3908594?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.bembos.com.pe/complementos",
        expiration="Carta permanente",
        location="Real Plaza Cajamarca y nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=False,
        delivery_time="20-30 min"
    ),
    FoodDeal(
        id="brg-reg-2",
        title="Hamburguesa Simple Clásica al Carbón",
        category="burger",
        category_name="Hamburguesas",
        brand="Bembos",
        price=8.90,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#0284c7",
        description="Carne 100% de res a la parrilla de carbón tradicional, lechuga fresca, rodajas de tomate y mayonesa Bembos.",
        image_url="https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.bembos.com.pe/hamburguesas",
        expiration="Carta permanente",
        location="Real Plaza Cajamarca y nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=False,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="brg-promo-1",
        title="Combo Bembos Clásica Mediana + Papas Fritas + Gaseosa",
        category="burger",
        category_name="Hamburguesas",
        brand="Bembos",
        price=10.90,
        original_price=21.90,
        discount_percent=50,
        platform="Yape Promos",
        platform_color="#7c3aed",
        description="La clásica hamburguesa peruana a la parrilla de carbón, servida con papas amarillas fritas y vaso de gaseosa helada.",
        image_url="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.bembos.com.pe/promociones",
        coupon_code="YAPEBEMBOS",
        expiration="Válido con Yape en tienda y delivery",
        location="Real Plaza Cajamarca y a nivel nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=True,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="brg-reg-3",
        title="Hamburguesa con Queso Cheddar Derretido & Pepinillos",
        category="burger",
        category_name="Hamburguesas",
        brand="McDonald's",
        price=9.90,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#0284c7",
        description="Carne de res sazonada, queso cheddar fundido, pepinillos crujientes, mostaza y ketchup en pan suave de ajonjolí.",
        image_url="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.mcdonalds.com.pe/menu/hamburguesas",
        expiration="Carta habitual",
        location="Lima, Arequipa, Trujillo, Chiclayo",
        districts=["miraflores", "surco", "lima_centro", "lima_norte", "lima_sur", "callao", "arequipa", "trujillo", "chiclayo_piura", "cusco"],
        is_promo=False,
        delivery_time="20-30 min"
    ),
    FoodDeal(
        id="brg-reg-4",
        title="Hamburguesa Whopper Jr con Papas Medianas",
        category="burger",
        category_name="Hamburguesas",
        brand="Burger King",
        price=12.90,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#ea580c",
        description="Carne a la parrilla de fuego directo, tomate fresco, lechuga cortada, mayonesa suave, pepinillos y papas crocantes.",
        image_url="https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=600&q=80",
        deal_url="https://burgerking.com.pe/menu/hamburguesas",
        expiration="Carta regular",
        location="Lima y Provincias",
        districts=ALL_PERU_DISTRICTS,
        is_promo=False,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="brg-promo-2",
        title="Combo Bembos La Churrita + Papas + Bebida (Rappi Turbo 15 min)",
        category="burger",
        category_name="Hamburguesas",
        brand="Bembos / Rappi",
        price=18.90,
        original_price=28.90,
        discount_percent=35,
        platform="Rappi",
        platform_color="#ff441f",
        description="Carne al carbón, plátano frito, huevo a la plancha, salsa tártara Bembos y papas medianas entregado en minutos.",
        image_url="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.rappi.com.pe/restaurantes/search?query=bembos+churrita",
        coupon_code="RAPPITURBO",
        expiration="Exclusivo Rappi Turbo",
        location="Cajamarca, Lima, Arequipa, Trujillo",
        districts=ALL_PERU_DISTRICTS,
        is_promo=True,
        delivery_time="10-15 min (Turbo)"
    ),
    FoodDeal(
        id="brg-reg-5",
        title="Hamburguesa A lo Pobre: Huevo, Plátano Frito y Tártara",
        category="burger",
        category_name="Hamburguesas",
        brand="Bembos",
        price=19.90,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#0284c7",
        description="La emblemática hamburguesa con carne gruesa al carbón, plátano frito dulce, huevo frito tierno y crema tártara.",
        image_url="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.bembos.com.pe/hamburguesas",
        expiration="Carta regular",
        location="Real Plaza Cajamarca y nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=False,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="brg-promo-3",
        title="Dúo Hamburguesas Cuarto de Libra con Queso + 2 Papas",
        category="burger",
        category_name="Hamburguesas",
        brand="McDonald's",
        price=24.90,
        original_price=42.90,
        discount_percent=42,
        platform="Yape Promos",
        platform_color="#7c3aed",
        description="Dos hamburguesas cuarto de libra con doble cheddar derretido, cebolla picada y pepinillos más 2 porciones de papas medianas.",
        image_url="https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.mcdonalds.com.pe/menu/hamburguesas",
        coupon_code="MCDUOYAPE",
        expiration="Lunes a Viernes con Yape",
        location="Lima y principales ciudades",
        districts=["miraflores", "surco", "lima_centro", "lima_norte", "lima_sur", "callao", "arequipa", "trujillo"],
        is_promo=True,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="brg-reg-6",
        title="Hamburguesa Doble Parrillera con Chimichurri Artesanal",
        category="burger",
        category_name="Hamburguesas",
        brand="Bembos",
        price=23.90,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#0284c7",
        description="Doble carne a la brasa, queso fundido, chorizo parrillero laminado y salsa chimichurri con papas amarillas.",
        image_url="https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.bembos.com.pe/hamburguesas",
        expiration="Carta habitual",
        location="Cajamarca y nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=False,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="brg-lima-1",
        title="Hamburguesa Osso Angus Gourmet con Queso Raclette y Tocino",
        category="burger",
        category_name="Hamburguesas",
        brand="Osso Carnicería",
        price=36.00,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#0284c7",
        description="Carne Angus madurada 200g, queso raclette derretido, tocino ahumado artesanal y cebolla caramelizada en pan brioche.",
        image_url="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=600&q=80",
        deal_url="https://osso.pe/menu-carniceria",
        expiration="Carta gourmet exclusiva",
        location="Miraflores, San Isidro y Surco (Lima)",
        districts=LIMA_PREMIUM_DISTRICTS,
        is_promo=False,
        delivery_time="35-50 min"
    ),

    # =========================================================================
    # --- 3. POLLO A LA BRASA & BROASTER (CARTA COMPLETA + OFERTAS) ---
    # =========================================================================
    FoodDeal(
        id="pol-reg-1",
        title="1/4 Pollo a la Brasa Solo con Ají Pollero",
        category="pollo",
        category_name="Pollo a la Brasa",
        brand="Rókys Chicken",
        price=13.90,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#dc2626",
        description="Pierna o pecho macerado con cerveza negra, especias peruanas y ajíes nativos dorado al carbón en su punto.",
        image_url="https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?auto=format&fit=crop&w=600&q=80",
        deal_url="https://rokys.pe/carta/pollos",
        expiration="Carta regular diaria",
        location="Cajamarca (El Quinde / Centro) y nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=False,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="pol-promo-1",
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
        deal_url="https://www.kfc.com.pe/para-uno",
        coupon_code="YAPEKFC13",
        expiration="Hasta agotar cupones Yape",
        location="El Quinde Cajamarca y nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=True,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="pol-promo-2",
        title="Combo 1/4 Pollo a la Brasa + Papas Fritas + Ensalada y Ají",
        category="pollo",
        category_name="Pollo a la Brasa",
        brand="Rókys Chicken",
        price=16.90,
        original_price=27.90,
        discount_percent=39,
        platform="Yape Promos",
        platform_color="#7c3aed",
        description="Cuarto de pollo a la brasa marinado a la leña, porción de papas amarillas fritas crocantes, ensalada fresca y cremas.",
        image_url="https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?auto=format&fit=crop&w=600&q=80",
        deal_url="https://rokys.pe/promociones",
        coupon_code="YAPEROKYS",
        expiration="Válido en salón y delivery con Yape",
        location="Cajamarca (El Quinde y Centro) y a nivel nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=True,
        delivery_time="30-40 min"
    ),
    FoodDeal(
        id="pol-reg-2",
        title="Mostrito Tradicional: Arroz Chaufa + 1/4 Pollo Broaster + Papas",
        category="pollo",
        category_name="Pollo a la Brasa",
        brand="Pollerías Perú",
        price=18.50,
        original_price=None,
        discount_percent=None,
        platform="PedidosYa",
        platform_color="#ea1d2c",
        description="El clásico Mostrito peruano: generoso arroz chaufa salteado al wok, cuarto de pollo crocante broaster, papas fritas y cremas.",
        image_url="https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.pedidosya.com.pe/restaurantes?q=mostrito",
        expiration="Carta del día",
        location="Cajamarca y nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=False,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="pol-promo-3",
        title="Twister Tradicional KFC con Papas Fritas Medianas",
        category="pollo",
        category_name="Pollo a la Brasa",
        brand="KFC",
        price=14.90,
        original_price=21.90,
        discount_percent=32,
        platform="App Oficial",
        platform_color="#dc2626",
        description="Tortilla de trigo tostada enrollada con dos tiras crujientes de pechuga de pollo, lechuga, tomate y mayonesa con papas.",
        image_url="https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.kfc.com.pe/para-uno",
        coupon_code="TWISTERKFC",
        expiration="De Lunes a Domingo",
        location="El Quinde Cajamarca y nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=True,
        delivery_time="20-30 min"
    ),
    FoodDeal(
        id="pol-reg-3",
        title="1/4 Pollo a la Brasa Pardos Gourmet + Papas Onduladas",
        category="pollo",
        category_name="Pollo a la Brasa",
        brand="Pardos Chicken",
        price=26.90,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#dc2626",
        description="El insuperable sabor Pardos a la brasa con papas fritas onduladas crocantes, ensalada fresca y su célebre ají de la casa.",
        image_url="https://images.unsplash.com/photo-1527477321005-4d01d702334b?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.pardoschicken.pe/carta/",
        expiration="Carta habitual",
        location="Lima, Arequipa, Trujillo, Chiclayo",
        districts=["miraflores", "surco", "lima_centro", "lima_sur", "callao", "arequipa", "trujillo"],
        is_promo=False,
        delivery_time="30-40 min"
    ),
    FoodDeal(
        id="pol-reg-4",
        title="1/2 Pollo a la Brasa con Papas Fritas y Ensalada Familiar",
        category="pollo",
        category_name="Pollo a la Brasa",
        brand="Norky's",
        price=32.90,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#c5a880",
        description="Medio pollo dorado a la brasa con porción grande de papas amarillas fritas, vinagreta tradicional y variedad de ajíes.",
        image_url="https://images.unsplash.com/photo-1567620832903-9fc6debc209f?auto=format&fit=crop&w=600&q=80",
        deal_url="https://norkys.pe/categoria-producto/pollos-a-la-brasa/",
        expiration="Carta regular",
        location="Cajamarca y sedes a nivel nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=False,
        delivery_time="30-45 min"
    ),
    FoodDeal(
        id="pol-promo-4",
        title="Mega Bucket KFC 8 Piezas Crujientes + Papas Familiares",
        category="pollo",
        category_name="Pollo a la Brasa",
        brand="KFC / Rappi",
        price=39.90,
        original_price=59.90,
        discount_percent=33,
        platform="Rappi",
        platform_color="#ff441f",
        description="Balde familiar con 8 presas crujientes de pollo receta original o crispy, porción familiar de papas fritas y salsas.",
        image_url="https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.rappi.com.pe/restaurantes/search?query=kfc+mega+bucket",
        coupon_code="RAPPIKFC",
        expiration="Viernes a Domingo en Rappi",
        location="El Quinde Cajamarca y cobertura nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=True,
        delivery_time="30-40 min"
    ),
    FoodDeal(
        id="pol-promo-5",
        title="1 Pollo Entero a la Brasa + Papas Familiares + Gaseosa 1.5L",
        category="pollo",
        category_name="Pollo a la Brasa",
        brand="Norky's",
        price=54.90,
        original_price=79.90,
        discount_percent=31,
        platform="Cuponera / Delivery",
        platform_color="#c5a880",
        description="Pollo entero dorado y jugoso, acompañado de papas fritas familiares, ensalada clásica con vinagreta y gaseosa de 1.5L.",
        image_url="https://images.unsplash.com/photo-1567620832903-9fc6debc209f?auto=format&fit=crop&w=600&q=80",
        deal_url="https://norkys.pe/categoria-producto/pollos-a-la-brasa/",
        coupon_code="POLLAZO",
        expiration="Todo el mes",
        location="Cajamarca y nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=True,
        delivery_time="35-50 min"
    ),

    # =========================================================================
    # --- 4. CHIFA (CARTA COMPLETA + OFERTAS) ---
    # =========================================================================
    FoodDeal(
        id="chi-reg-1",
        title="Porción de 6 Wantanes Fritos con Salsa Tamarindo",
        category="chifa",
        category_name="Chifa",
        brand="Chinawok",
        price=7.90,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#0284c7",
        description="Wantanes crujientes rellenos de pollo sazonado, acompañados de abundante salsa de tamarindo agridulce caliente.",
        image_url="https://images.unsplash.com/photo-1541696432-82c6da8ce7bf?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.chinawok.com.pe/entradas",
        expiration="Carta habitual",
        location="Cajamarca (Real Plaza / Centro) y nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=False,
        delivery_time="20-30 min"
    ),
    FoodDeal(
        id="chi-reg-2",
        title="Arroz Chaufa de Pollo Individual al Wok",
        category="chifa",
        category_name="Chifa",
        brand="Chifa Express",
        price=13.50,
        original_price=None,
        discount_percent=None,
        platform="PedidosYa",
        platform_color="#ea1d2c",
        description="Arroz salteado a fuego vivo con sillao cantonés, trozos de pechuga de pollo, huevo revuelto y cebolla china fresca.",
        image_url="https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.pedidosya.com.pe/restaurantes?q=arroz+chaufa+pollo",
        expiration="Menú del día",
        location="Cajamarca y provincias",
        districts=ALL_PERU_DISTRICTS,
        is_promo=False,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="chi-promo-1",
        title="Combo Chifa Aeropuerto Especial + 4 Wantanes Fritos",
        category="chifa",
        category_name="Chifa",
        brand="Chinawok",
        price=16.90,
        original_price=26.90,
        discount_percent=37,
        platform="Yape Promos",
        platform_color="#7c3aed",
        description="Arroz chaufa al wok salteado con tallarín chino, frijolito chino, pollo en cubos y 4 wantanes dorados con tamarindo.",
        image_url="https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.chinawok.com.pe/combos-personales",
        coupon_code="YAPEWOK16",
        expiration="Exclusivo con Yape",
        location="Real Plaza Cajamarca y nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=True,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="chi-reg-3",
        title="Plato Chi Jau Kay Crujiente con Porción de Arroz Chaufa",
        category="chifa",
        category_name="Chifa",
        brand="Chinawok",
        price=19.90,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#0284c7",
        description="Pechuga de pollo marinada y empanizada al panko chino bañado en salsa de ostión y sésamo con chaufa al wok.",
        image_url="https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.chinawok.com.pe/platos",
        expiration="Carta habitual",
        location="Cajamarca y nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=False,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="chi-reg-4",
        title="Plato Tipakay Agridulce con Piña y Wantán Frito",
        category="chifa",
        category_name="Chifa",
        brand="Chinawok",
        price=19.90,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#0284c7",
        description="Filete de pollo arrebozado con salsa tamarindo agridulce, trozos de piña, durazno y porción de arroz chaufa.",
        image_url="https://images.unsplash.com/photo-1541696432-82c6da8ce7bf?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.chinawok.com.pe/platos",
        expiration="Carta habitual",
        location="Cajamarca y nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=False,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="chi-reg-5",
        title="Sopa Wantán Especial con Pollo, Huevo de Codorniz y Fideos",
        category="chifa",
        category_name="Chifa",
        brand="Chifa Tradicional",
        price=16.50,
        original_price=None,
        discount_percent=None,
        platform="Delivery Local",
        platform_color="#c5a880",
        description="Caldo reconfortante de ave con wantanes sancochados rellenos de langostino y pollo, col china, pac choi y fideos finos.",
        image_url="https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.pedidosya.com.pe/restaurantes?q=sopa+wantan",
        expiration="Carta permanente",
        location="Cajamarca y nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=False,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="chi-promo-2",
        title="Banquete Familiar Chinawok: Chaufa Familiar + 8 Wantanes + Gaseosa",
        category="chifa",
        category_name="Chifa",
        brand="Chinawok / Rappi",
        price=29.90,
        original_price=45.90,
        discount_percent=35,
        platform="Rappi",
        platform_color="#ff441f",
        description="Fuente familiar de arroz chaufa especial con trozos de pollo, sillao cantonés, 8 wantanes fritos y gaseosa familiar.",
        image_url="https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.rappi.com.pe/restaurantes/search?query=chinawok+banquete",
        coupon_code="RAPPIWOK",
        expiration="Válido en delivery Rappi",
        location="Cajamarca, Lima, Arequipa, Trujillo",
        districts=ALL_PERU_DISTRICTS,
        is_promo=True,
        delivery_time="25-35 min"
    ),

    # =========================================================================
    # --- 5. MAKIS & SUSHI (CARTA COMPLETA + OFERTAS) ---
    # =========================================================================
    FoodDeal(
        id="mak-reg-1",
        title="Porción de 5 Makis Furai Tradicionales Crujientes",
        category="makis",
        category_name="Makis & Sushi",
        brand="Maki Express",
        price=12.00,
        original_price=None,
        discount_percent=None,
        platform="Cuponera / Delivery",
        platform_color="#c5a880",
        description="5 cortes de roll empanizado al panko crujiente relleno de trucha o langostino y queso crema, con salsa tare dulce.",
        image_url="https://images.unsplash.com/photo-1611143669185-af224c5e3252?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.pedidosya.com.pe/restaurantes?q=makis+furai",
        expiration="Carta diaria",
        location="Lima y principales ciudades",
        districts=["miraflores", "surco", "lima_centro", "lima_sur", "arequipa", "trujillo", "cajamarca"],
        is_promo=False,
        delivery_time="30-40 min"
    ),
    FoodDeal(
        id="mak-promo-1",
        title="Tabla 10 Makis Acebichados o Furai + Bebida",
        category="makis",
        category_name="Makis & Sushi",
        brand="Shimaya Ramen & Makis",
        price=18.90,
        original_price=32.90,
        discount_percent=43,
        platform="Yape Promos",
        platform_color="#7c3aed",
        description="10 cortes de maki acebichado con langostino al panko, palta fresca, cubierto de láminas de atún y salsa acebichada artesanal.",
        image_url="https://images.unsplash.com/photo-1611143669185-af224c5e3252?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.rappi.com.pe/restaurantes/search?query=shimaya+makis+acevichados",
        coupon_code="YAPEMAKI18",
        expiration="Lunes a Jueves con Yape",
        location="Lima, Arequipa y Trujillo",
        districts=["miraflores", "surco", "lima_centro", "lima_sur", "arequipa", "trujillo"],
        is_promo=True,
        delivery_time="30-40 min"
    ),
    FoodDeal(
        id="mak-reg-2",
        title="Tabla 10 Cortes California Roll con Ajonjolí Tostado",
        category="makis",
        category_name="Makis & Sushi",
        brand="Itamae Sushi",
        price=21.90,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#0284c7",
        description="Roll clásico con kanikama, palta cremosa y pepino fresco, envuelto en arroz japonés con semillas de ajonjolí blanco y negro.",
        image_url="https://images.unsplash.com/photo-1579871494447-9811cf80d66c?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.rappi.com.pe/restaurantes/search?query=itamae+california+roll",
        expiration="Carta regular",
        location="Miraflores, San Isidro, Surco, Arequipa",
        districts=["miraflores", "surco", "lima_centro", "lima_sur", "arequipa"],
        is_promo=False,
        delivery_time="30-45 min"
    ),
    FoodDeal(
        id="mak-promo-2",
        title="2x1 Tabla 20 Makis Nikkei: 10 Acebichados + 10 Furai",
        category="makis",
        category_name="Makis & Sushi",
        brand="Hanzo Nikkei / Rappi",
        price=32.90,
        original_price=58.00,
        discount_percent=43,
        platform="Rappi",
        platform_color="#ff441f",
        description="Dúo de 20 cortes nikkei: 10 acebichados con salsa clásica de la casa y 10 furai empanizados con panko crujiente y salsa dulce tare.",
        image_url="https://images.unsplash.com/photo-1579871494447-9811cf80d66c?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.rappi.com.pe/restaurantes/search?query=hanzo+makis",
        coupon_code="RAPPIMAKI",
        expiration="De Lunes a Jueves en Rappi",
        location="Miraflores, San Isidro, Surco, San Borja",
        districts=LIMA_PREMIUM_DISTRICTS,
        is_promo=True,
        delivery_time="30-40 min"
    ),
    FoodDeal(
        id="mak-lima-1",
        title="Combo Imperial Edo: 30 Makis Variados de la Casa",
        category="makis",
        category_name="Makis & Sushi",
        brand="Edo Sushi Bar",
        price=49.90,
        original_price=75.00,
        discount_percent=33,
        platform="App Oficial",
        platform_color="#0284c7",
        description="30 cortes de autor: 10 Acevichado Edo, 10 Lomo Saltado Maki flameado y 10 Furai Tokio con salsa tare especial.",
        image_url="https://images.unsplash.com/photo-1611143669185-af224c5e3252?auto=format&fit=crop&w=600&q=80",
        deal_url="https://edosushibar.com/carta/makis",
        expiration="Carta oficial",
        location="Miraflores, San Isidro, Surco, Magdalena",
        districts=LIMA_PREMIUM_DISTRICTS,
        is_promo=True,
        delivery_time="35-50 min"
    ),

    # =========================================================================
    # --- 6. POSTRES & CAFÉ (CARTA COMPLETA + OFERTAS) ---
    # =========================================================================
    FoodDeal(
        id="pos-reg-1",
        title="Donut Glaseada Tradicional Recién Horneada",
        category="postres",
        category_name="Postres & Café",
        brand="Dunkin'",
        price=4.90,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#0284c7",
        description="Donut clásica esponjosa con el glaseado dulce original Dunkin' recién horneada artesanalmente.",
        image_url="https://images.unsplash.com/photo-1527515637462-cff94eecc1ac?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.dunkin.pe/categoria/donuts",
        expiration="Carta diaria permanente",
        location="Cajamarca (El Quinde) y a nivel nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=False,
        delivery_time="20-30 min"
    ),
    FoodDeal(
        id="pos-reg-2",
        title="Café Americano Caliente 12oz Grano Seleccionado",
        category="postres",
        category_name="Postres & Café",
        brand="Starbucks Perú",
        price=8.50,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#0284c7",
        description="Espresso shots de café 100% arábica cubiertos con agua caliente produciendo una capa fina de crema dorada aromática.",
        image_url="https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.starbucks.com.pe/menu-list",
        expiration="Todo el día",
        location="Lima y principales ciudades",
        districts=["miraflores", "surco", "lima_centro", "lima_sur", "callao", "arequipa", "trujillo"],
        is_promo=False,
        delivery_time="15-25 min"
    ),
    FoodDeal(
        id="pos-reg-3",
        title="Helado McFlurry Clásico con Galletas Oreo Trituradas",
        category="postres",
        category_name="Postres & Café",
        brand="McDonald's",
        price=9.90,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#0284c7",
        description="Cremoso helado de vainilla batido con abundantes trozos crujientes de galletas Oreo originales y sirope dulce.",
        image_url="https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.mcdonalds.com.pe/menu/postres",
        expiration="Carta permanente",
        location="Lima, Arequipa, Trujillo, Chiclayo",
        districts=["miraflores", "surco", "lima_centro", "lima_norte", "lima_sur", "callao", "arequipa", "trujillo"],
        is_promo=False,
        delivery_time="15-25 min"
    ),
    FoodDeal(
        id="pos-reg-4",
        title="Porción Torta Húmeda de Chocolate con Fudge Casero",
        category="postres",
        category_name="Postres & Café",
        brand="Pastelería San Antonio",
        price=14.50,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#0284c7",
        description="Bizcochuelo artesanal húmedo relleno y bañado con generoso fudge espeso de cacao peruano y chocolate bitter.",
        image_url="https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=600&q=80",
        deal_url="https://sanantonio.pe/pasteleria",
        expiration="Carta diaria",
        location="Miraflores, San Isidro, Surco, San Borja",
        districts=LIMA_PREMIUM_DISTRICTS,
        is_promo=False,
        delivery_time="25-40 min"
    ),
    FoodDeal(
        id="pos-promo-1",
        title="2x1 Frappuccino Mediano Caramel o Mocha con Crema",
        category="postres",
        category_name="Postres & Café",
        brand="Starbucks Perú",
        price=18.50,
        original_price=32.00,
        discount_percent=42,
        platform="Yape Promos",
        platform_color="#7c3aed",
        description="Dos frappuccinos tamaño tall de café arábica con leche, jarabe de caramelo o mocha batido con hielo y crema batida chantilly.",
        image_url="https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.starbucks.com.pe/menu-list",
        coupon_code="YAPESTARBUCKS",
        expiration="De 3:00 PM a 7:00 PM con Yape",
        location="Lima, Arequipa y Trujillo",
        districts=["miraflores", "surco", "lima_centro", "lima_sur", "callao", "arequipa", "trujillo"],
        is_promo=True,
        delivery_time="20-30 min"
    ),
    FoodDeal(
        id="pos-promo-2",
        title="Caja de 6 Donuts Variadas (Glaseadas, Chocolate, Crema Bavaria)",
        category="postres",
        category_name="Postres & Café",
        brand="Dunkin'",
        price=19.90,
        original_price=32.90,
        discount_percent=40,
        platform="Yape Promos",
        platform_color="#7c3aed",
        description="Media docena de donas surtidas clásicas: glaseado dulce original, manjar blanco, crema bávara y cobertura de chocolate oscuro.",
        image_url="https://images.unsplash.com/photo-1527515637462-cff94eecc1ac?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.dunkin.pe/categoria/donuts",
        coupon_code="YAPEDUNKIN",
        expiration="Válido en todos los locales Dunkin'",
        location="Cajamarca (El Quinde) y a nivel nacional",
        districts=ALL_PERU_DISTRICTS,
        is_promo=True,
        delivery_time="25-35 min"
    ),

    # =========================================================================
    # --- 7. ESPECIALIDADES Y RESTAURANTES DE CAJAMARCA (LOCAL & DELIVERY) ---
    # =========================================================================
    FoodDeal(
        id="caj-reg-1",
        title="Caldo Verde Tradicional Cajamarquino con Quesillo Fresco",
        category="pollo",
        category_name="Especial Cajamarca",
        brand="Picantería Tradición Cajamarquina",
        price=11.90,
        original_price=None,
        discount_percent=None,
        platform="Delivery Local",
        platform_color="#c5a880",
        description="El plato bandera de Cajamarca: caldo aromático de paico, ruda y hierbabuena molidos al batán, con papa amarilla y abundante quesillo fresco.",
        image_url="https://images.unsplash.com/photo-1541696432-82c6da8ce7bf?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.pedidosya.com.pe/restaurantes/cajamarca?q=caldo+verde",
        expiration="Todos los días de 7am a 2pm",
        location="Cajamarca (Centro Histórico y Baños del Inca)",
        districts=CAJAMARCA_ONLY_DISTRICTS,
        is_promo=False,
        delivery_time="20-30 min"
    ),
    FoodDeal(
        id="caj-promo-1",
        title="Combo Bembos Real Plaza Cajamarca: Clásica + Papas + Gaseosa",
        category="burger",
        category_name="Hamburguesas",
        brand="Bembos / Real Plaza Cajamarca",
        price=11.90,
        original_price=22.90,
        discount_percent=48,
        platform="Yape Promos",
        platform_color="#7c3aed",
        description="Hamburguesa a la parrilla de carbón con papas crocantes y bebida en Real Plaza Cajamarca pagando con Yape.",
        image_url="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.bembos.com.pe/promociones",
        coupon_code="YAPECAJAMARCA",
        expiration="Válido en Real Plaza Cajamarca",
        location="Real Plaza Cajamarca (Av. Evitamiento)",
        districts=CAJAMARCA_ONLY_DISTRICTS,
        is_promo=True,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="caj-reg-2",
        title="Queso Mantecoso Cajamarquino con Miel de Abeja y Rosquitas",
        category="postres",
        category_name="Especial Cajamarca",
        brand="Lácteos Huacariz Cajamarca",
        price=12.50,
        original_price=None,
        discount_percent=None,
        platform="Delivery Local",
        platform_color="#c5a880",
        description="Porción generosa de auténtico queso mantecoso de leche fresca de vaca cajamarquina, acompañado de miel pura de valle y rosquitas artesanales.",
        image_url="https://images.unsplash.com/photo-1541696432-82c6da8ce7bf?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.pedidosya.com.pe/restaurantes/cajamarca?q=huacariz",
        expiration="Carta diaria",
        location="Cajamarca (Huacariz / Centro)",
        districts=CAJAMARCA_ONLY_DISTRICTS,
        is_promo=False,
        delivery_time="20-30 min"
    ),
    FoodDeal(
        id="caj-promo-2",
        title="Manjar Blanco Huacariz Pote 500g + Paquete de Rosquitas",
        category="postres",
        category_name="Especial Cajamarca",
        brand="Lácteos Huacariz Cajamarca",
        price=13.90,
        original_price=19.90,
        discount_percent=30,
        platform="Yape Promos",
        platform_color="#7c3aed",
        description="Pote familiar de 500g del tradicional manjar blanco cajamarquino a fuego de leña con paquete de rosquitas crujientes tradicionales.",
        image_url="https://images.unsplash.com/photo-1527515637462-cff94eecc1ac?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.pedidosya.com.pe/restaurantes/cajamarca?q=manjar+blanco",
        coupon_code="YAPEHUACARIZ",
        expiration="Hasta agotar stock en Cajamarca",
        location="Cajamarca (Centro Histórico y Baños del Inca)",
        districts=CAJAMARCA_ONLY_DISTRICTS,
        is_promo=True,
        delivery_time="20-35 min"
    ),
    FoodDeal(
        id="caj-reg-3",
        title="Chifa Cajamarquino: Aeropuerto Salteado al Wok con Wantanes",
        category="chifa",
        category_name="Chifa",
        brand="Chifa Central Cajamarca",
        price=14.90,
        original_price=None,
        discount_percent=None,
        platform="PedidosYa",
        platform_color="#ea1d2c",
        description="Arroz chaufa con tallarín saltado criollo al wok, trozos tiernos de pollo marinado, cebolla china y wantanes fritos con salsa tamarindo dulce.",
        image_url="https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.pedidosya.com.pe/restaurantes/cajamarca?q=chifa",
        expiration="Carta del día",
        location="Cajamarca Ciudad (Delivery PedidosYa)",
        districts=CAJAMARCA_ONLY_DISTRICTS,
        is_promo=False,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="caj-promo-3",
        title="Combo 1/4 Pollo a la Brasa en El Quinde Cajamarca + Chicha",
        category="pollo",
        category_name="Pollo a la Brasa",
        brand="Rókys / El Quinde Cajamarca",
        price=15.90,
        original_price=26.90,
        discount_percent=41,
        platform="PedidosYa",
        platform_color="#ea1d2c",
        description="Cuarto de pollo a la brasa dorado, papas fritas crocantes, cremas de ají casero y vaso de chicha morada en El Quinde Cajamarca.",
        image_url="https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.pedidosya.com.pe/restaurantes/cajamarca?q=rokys",
        coupon_code="PEDIDOSCAJ",
        expiration="Válido en delivery PedidosYa Cajamarca",
        location="El Quinde Cajamarca (Av. Hoyos Rubio)",
        districts=CAJAMARCA_ONLY_DISTRICTS,
        is_promo=True,
        delivery_time="25-40 min"
    ),
    FoodDeal(
        id="caj-promo-4",
        title="Pizza Mediana Americana o Pepperoni en El Quinde Cajamarca",
        category="pizza",
        category_name="Pizzas",
        brand="Pizza Hut / El Quinde",
        price=16.90,
        original_price=32.90,
        discount_percent=49,
        platform="Yape Promos",
        platform_color="#7c3aed",
        description="Pizza mediana recién horneada con queso mozzarella y pepperoni americano en el patio de comidas El Quinde Cajamarca pagando con Yape.",
        image_url="https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.pizzahut.com.pe/promociones",
        coupon_code="YAPEHUTCAJ",
        expiration="Todo el mes con Yape",
        location="El Quinde Cajamarca (Patio de Comidas)",
        districts=CAJAMARCA_ONLY_DISTRICTS,
        is_promo=True,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="caj-reg-4",
        title="Chicharrón Cajamarquino con Mote, Camote Dorado y Salsa Criolla",
        category="pollo",
        category_name="Especial Cajamarca",
        brand="Chicharronería Don Pedro Cajamarca",
        price=18.00,
        original_price=None,
        discount_percent=None,
        platform="Delivery Local",
        platform_color="#c5a880",
        description="Trozos crujientes de chicharrón de cerdo dorado en su propia manteca, servido con abundante mote tierno cajamarquino y camote dorado.",
        image_url="https://images.unsplash.com/photo-1541696432-82c6da8ce7bf?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.pedidosya.com.pe/restaurantes/cajamarca?q=chicharron",
        expiration="Carta de fin de semana y diario",
        location="Cajamarca (Jr. Amalia Puga / Centro)",
        districts=CAJAMARCA_ONLY_DISTRICTS,
        is_promo=False,
        delivery_time="25-40 min"
    ),
    FoodDeal(
        id="caj-reg-5",
        title="Cuy Chactado Cajamarquino Entero con Papas Amarillas Doradas",
        category="pollo",
        category_name="Especial Cajamarca",
        brand="Picantería Campestre Cajamarca",
        price=45.00,
        original_price=None,
        discount_percent=None,
        platform="Delivery Local",
        platform_color="#c5a880",
        description="Cuy entero macerado con ajos, comino y ají panca, prensado y frito a la piedra hasta quedar crocante por fuera y tierno por dentro.",
        image_url="https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.pedidosya.com.pe/restaurantes/cajamarca?q=cuy+chactado",
        expiration="Carta tradicional",
        location="Baños del Inca y Cajamarca Centro",
        districts=CAJAMARCA_ONLY_DISTRICTS,
        is_promo=False,
        delivery_time="35-50 min"
    )
]

SUPPORTED_LOCATIONS = [
    {"id": "todas", "name": "Todo el Perú (Todas las sedes)"},
    {"id": "cajamarca", "name": "Cajamarca (El Quinde / Real Plaza / Baños del Inca)"},
    {"id": "miraflores", "name": "Miraflores / San Isidro / San Borja"},
    {"id": "surco", "name": "Surco / La Molina"},
    {"id": "lima_centro", "name": "Lima Centro / Jesús María / Magdalena"},
    {"id": "lima_norte", "name": "Lima Norte (Los Olivos / Comas / Indep.)"},
    {"id": "lima_sur", "name": "Lima Sur (Chorrillos / SJM / Barranco)"},
    {"id": "lima_este", "name": "Lima Este (San Juan de Lurigancho / Ate)"},
    {"id": "callao", "name": "Callao / Bellavista / San Miguel"},
    {"id": "arequipa", "name": "Arequipa (Cayma / Cercado)"},
    {"id": "trujillo", "name": "Trujillo (Centro / El Golf)"},
    {"id": "chiclayo_piura", "name": "Chiclayo / Piura"},
    {"id": "cusco", "name": "Cusco / Huancayo"}
]

def search_food_deals(
    category: Optional[str] = None,
    platform: Optional[str] = None,
    location: Optional[str] = None,
    only_discounts: bool = False,
    query: Optional[str] = None,
    sort_by: str = "asc" # 'asc' = menor a mayor precio (default), 'desc', 'discount'
) -> Dict[str, Any]:
    filtered = list(RAW_FOOD_DEALS)

    # 1. Filter by category if provided
    if category and category.lower() not in ("todas", "all", ""):
        clean_cat = category.strip().lower()
        filtered = [f for f in filtered if f.category.lower() == clean_cat]

    # 2. Filter by platform/app if provided (Yape, Rappi, App Oficial, etc.)
    if platform and platform.lower() not in ("todas", "all", ""):
        clean_plat = platform.strip().lower()
        filtered = [f for f in filtered if clean_plat in f.platform.lower()]

    # 3. Filter strictly by location / district if provided
    # IMPORTANT: Only include items that actually service the selected locality!
    is_specific_loc = bool(location and location.lower() not in ("todas", "all", ""))
    if is_specific_loc:
        loc = location.strip().lower()
        filtered = [
            f for f in filtered
            if loc in f.districts
        ]

    # 4. Filter by only discounts / promotions if requested
    # When False, shows the FULL CARTA (regular menu + promos)
    # When True, shows ONLY items with a real active discount
    if only_discounts:
        filtered = [
            f for f in filtered 
            if f.is_promo and (f.discount_percent or 0) > 0 and (f.original_price or 0) > f.price
        ]

    # 5. Filter by search query if provided
    if query:
        q = query.strip().lower()
        filtered = [
            f for f in filtered
            if q in f.title.lower() or q in f.brand.lower() or q in f.description.lower() or q in f.category_name.lower() or q in f.platform.lower() or q in f.location.lower()
        ]

    # 6. Sort strictly: default is ASCENDING (menor precio a mayor precio)
    if sort_by == "desc":
        filtered.sort(key=lambda x: x.price, reverse=True)
    elif sort_by == "discount":
        filtered.sort(key=lambda x: (x.discount_percent or 0), reverse=True)
    else: # 'asc'
        filtered.sort(key=lambda x: x.price)

    # Create clones to dynamically adjust location display if a specific locality is chosen
    results_list = []
    for item in filtered:
        item_dict = item.to_dict()
        if is_specific_loc:
            loc = location.strip().lower()
            if loc == "cajamarca":
                if "pedidosya.com.pe/restaurantes?" in item_dict["deal_url"]:
                    item_dict["deal_url"] = item_dict["deal_url"].replace(
                        "pedidosya.com.pe/restaurantes?",
                        "pedidosya.com.pe/restaurantes/cajamarca?"
                    )
                if "bembos" in item.brand.lower() or "real plaza" in item.brand.lower():
                    item_dict["location"] = "Real Plaza Cajamarca (Av. Evitamiento)"
                elif "pizza hut" in item.brand.lower() or "kfc" in item.brand.lower() or "papa john" in item.brand.lower():
                    item_dict["location"] = "El Quinde Cajamarca (Patio de Comidas)"
                elif "huacariz" in item.brand.lower():
                    item_dict["location"] = "Huacariz / Cajamarca Centro"
                elif "cajamarca" in item.location.lower():
                    pass # keep existing local Cajamarca string
                else:
                    item_dict["location"] = "Cajamarca (El Quinde / Delivery)"
            elif loc == "arequipa":
                if "pedidosya.com.pe/restaurantes?" in item_dict["deal_url"]:
                    item_dict["deal_url"] = item_dict["deal_url"].replace(
                        "pedidosya.com.pe/restaurantes?",
                        "pedidosya.com.pe/restaurantes/arequipa?"
                    )
                if "nacional" in item.location.lower() or "provincias" in item.location.lower():
                    item_dict["location"] = "Arequipa (Mall Aventura / Cayma)"
            elif loc == "trujillo":
                if "pedidosya.com.pe/restaurantes?" in item_dict["deal_url"]:
                    item_dict["deal_url"] = item_dict["deal_url"].replace(
                        "pedidosya.com.pe/restaurantes?",
                        "pedidosya.com.pe/restaurantes/trujillo?"
                    )
                if "nacional" in item.location.lower() or "provincias" in item.location.lower():
                    item_dict["location"] = "Trujillo (Mallplaza / Real Plaza)"
            elif loc in ("miraflores", "surco", "lima_centro", "lima_norte", "lima_sur"):
                if "nacional" in item.location.lower():
                    item_dict["location"] = "Lima Metropolitana (Tiendas & Delivery)"
        results_list.append(item_dict)

    prices = [f["price"] for f in results_list]
    stats = {
        "total_results": len(results_list),
        "lowest_price": min(prices) if prices else 0.0,
        "highest_price": max(prices) if prices else 0.0,
        "average_price": round(sum(prices) / len(prices), 2) if prices else 0.0,
        "cheapest_item": results_list[0] if results_list else None
    }

    # Dynamic Category counts based on active locality & discount filters
    # So category pill counts accurately match what the user will see
    base_pool = RAW_FOOD_DEALS
    if is_specific_loc:
        loc = location.strip().lower()
        base_pool = [f for f in base_pool if loc in f.districts]
    if only_discounts:
        base_pool = [f for f in base_pool if f.is_promo and (f.discount_percent or 0) > 0 and (f.original_price or 0) > f.price]

    cat_counts = {}
    for f in base_pool:
        cat_counts[f.category] = cat_counts.get(f.category, 0) + 1

    return {
        "query": query,
        "category": category,
        "platform": platform,
        "location": location,
        "only_discounts": only_discounts,
        "sort_by": sort_by,
        "stats": stats,
        "categories": cat_counts,
        "supported_locations": SUPPORTED_LOCATIONS,
        "results": results_list
    }
