from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field

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
    platform: str # 'Yape Promos', 'Rappi', 'App Oficial', 'Cuponera / Delivery'
    platform_color: str
    description: str
    image_url: str
    deal_url: str
    coupon_code: Optional[str] = None
    expiration: str = "Válido hoy"
    location: str = "Nacional (Lima y Provincias)"
    districts: List[str] = field(default_factory=lambda: ["todas"])
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

# Curated catalog: Both real-world promotions (Yape, Rappi, Cuponeras) and full menu/regular carta items
RAW_FOOD_DEALS: List[FoodDeal] = [
    # ==========================================
    # --- ENTRADAS, SNACKS & CARTA REGULAR (DESDE S/ 4.90) ---
    # ==========================================
    FoodDeal(
        id="food-reg-1",
        title="Donut Glaseada Tradicional Recién Horneada",
        category="postres",
        category_name="Postres & Café",
        brand="Dunkin'",
        price=4.90,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#0284c7",
        description="Donut clásica con glaseado dulce original recién horneada artesanalmente.",
        image_url="https://images.unsplash.com/photo-1527515637462-cff94eecc1ac?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.dunkin.pe/",
        expiration="Carta regular diaria",
        location="Nacional (Todas las tiendas)",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_norte", "lima_sur", "lima_este", "callao", "arequipa", "trujillo"],
        is_promo=False,
        delivery_time="20-30 min"
    ),
    FoodDeal(
        id="food-reg-2",
        title="Porción de Papas Fritas Amarillas Medianas Crocantes",
        category="burger",
        category_name="Hamburguesas",
        brand="Bembos",
        price=6.90,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#0284c7",
        description="Porción de papas amarillas fritas al punto exacto con crema tártara y mayonesa.",
        image_url="https://images.unsplash.com/photo-1576107232684-1279f3908594?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.bembos.com.pe/",
        expiration="Carta permanente",
        location="Nacional",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_norte", "lima_sur", "lima_este", "callao", "arequipa", "trujillo"],
        is_promo=False,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="food-reg-3",
        title="Porción 6 Wantanes Fritos con Salsa Tamarindo",
        category="chifa",
        category_name="Chifa",
        brand="Chinawok",
        price=7.90,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#0284c7",
        description="Wantanes crocantes rellenos de masa sazonada con abundante salsa tamarindo dulce.",
        image_url="https://images.unsplash.com/photo-1541696432-82c6da8ce7bf?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.chinawok.com.pe/",
        expiration="Carta regular",
        location="Lima y Provincias",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_norte", "lima_sur", "callao", "arequipa"],
        is_promo=False,
        delivery_time="25-40 min"
    ),
    FoodDeal(
        id="food-reg-4",
        title="Café Americano Caliente 12oz Grano Seleccionado",
        category="postres",
        category_name="Postres & Café",
        brand="Starbucks Perú",
        price=8.50,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#0284c7",
        description="Espresso shots cubiertos con agua caliente produciendo una capa ligera de crema.",
        image_url="https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.starbucks.com.pe/",
        expiration="Todo el día",
        location="Lima y Provincias",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_sur", "callao", "arequipa", "trujillo"],
        is_promo=False,
        delivery_time="15-25 min"
    ),
    FoodDeal(
        id="food-reg-5",
        title="Hamburguesa Simple Clásica al Carbón",
        category="burger",
        category_name="Hamburguesas",
        brand="Bembos",
        price=8.90,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#0284c7",
        description="Carne 100% de res a la parrilla de carbón, lechuga fresca, tomate y mayonesa.",
        image_url="https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.bembos.com.pe/",
        expiration="Carta habitual",
        location="Nacional",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_norte", "lima_sur", "lima_este", "callao", "arequipa", "trujillo"],
        is_promo=False,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="food-reg-6",
        title="Pizza Personal Americana 4 Cortes",
        category="pizza",
        category_name="Pizzas",
        brand="Little Caesars",
        price=11.90,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#ea580c",
        description="Pizza personal individual con salsa italiana y queso mozzarella horneada al momento.",
        image_url="https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=600&q=80",
        deal_url="https://littlecaesars.pe/",
        expiration="Precio regular",
        location="Lima Metropolitana",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_norte", "lima_sur", "callao"],
        is_promo=False,
        delivery_time="20-30 min"
    ),
    FoodDeal(
        id="food-reg-7",
        title="Porción 5 Makis Furai Tradicionales",
        category="makis",
        category_name="Makis & Sushi",
        brand="Maki Express",
        price=12.00,
        original_price=None,
        discount_percent=None,
        platform="Cuponera / Delivery",
        platform_color="#c5a880",
        description="5 cortes de maki empanizado al panko relleno de trucha y palta con salsa tare.",
        image_url="https://images.unsplash.com/photo-1611143669185-af224c5e3252?auto=format&fit=crop&w=600&q=80",
        deal_url="https://yape.com.pe/promociones",
        expiration="Carta diaria",
        location="Lima Centro y Sur",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_sur"],
        is_promo=False,
        delivery_time="30-40 min"
    ),
    FoodDeal(
        id="food-reg-8",
        title="Plato Chaufa de Pollo Individual al Wok",
        category="chifa",
        category_name="Chifa",
        brand="Chifa Express",
        price=13.50,
        original_price=None,
        discount_percent=None,
        platform="Cuponera / Delivery",
        platform_color="#c5a880",
        description="Arroz salteado con sillao chino, huevo en trozos, cebolla china y pollo marinado.",
        image_url="https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=600&q=80",
        deal_url="https://yape.com.pe/promociones",
        expiration="Menú del día",
        location="Lima y Provincias",
        districts=["todas", "lima_centro", "lima_norte", "lima_este", "callao", "arequipa", "trujillo"],
        is_promo=False,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="food-reg-9",
        title="1/4 Pollo a la Brasa Solo sin Guarnición",
        category="pollo",
        category_name="Pollo a la Brasa",
        brand="Rókys Chicken",
        price=13.90,
        original_price=None,
        discount_percent=None,
        platform="App Oficial",
        platform_color="#0284c7",
        description="Pierna o pecho a la brasa dorado con macerado especial y cremas de ají casero.",
        image_url="https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?auto=format&fit=crop&w=600&q=80",
        deal_url="https://rokys.pe/",
        expiration="Carta permanente",
        location="Nacional",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_norte", "lima_sur", "lima_este", "callao", "arequipa", "trujillo"],
        is_promo=False,
        delivery_time="30-45 min"
    ),

    # ==========================================
    # --- RAPPI PROMOS & RAPPI TURBO ---
    # ==========================================
    FoodDeal(
        id="food-rap-1",
        title="Rappi Turbo: Combo Bembos La Churrita + Papas + Bebida en 15 min",
        category="burger",
        category_name="Hamburguesas",
        brand="Bembos / Rappi",
        price=18.90,
        original_price=28.90,
        discount_percent=35,
        platform="Rappi",
        platform_color="#ff441f", # Rappi Orange-Red
        description="Doble carne al carbón, plátano, huevo, salsa tártara y papas medianas entregado en tiempo récord por Rappi Turbo.",
        image_url="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.rappi.com.pe/",
        coupon_code="RAPPITURBO",
        expiration="Exclusivo Rappi Turbo",
        location="Cobertura Rappi (Lima, Arequipa, Trujillo)",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_norte", "lima_sur", "callao", "arequipa", "trujillo"],
        is_promo=True,
        delivery_time="10-15 min (Turbo)"
    ),
    FoodDeal(
        id="food-rap-2",
        title="Rappi Promo: Pizza Mediana Papa John's Pepperoni + Garlic Dip",
        category="pizza",
        category_name="Pizzas",
        brand="Papa John's / Rappi",
        price=21.90,
        original_price=36.90,
        discount_percent=41,
        platform="Rappi",
        platform_color="#ff441f",
        description="Masa clásica recién horneada con mozzarella 100%, pepperoni premium y la inconfundible salsa especial de ajo.",
        image_url="https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.rappi.com.pe/",
        coupon_code="RAPPIPAPA",
        expiration="Hasta fin de mes en Rappi",
        location="Lima Metropolitana",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_sur", "callao"],
        is_promo=True,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="food-rap-3",
        title="Rappi Exclusivo: 2x1 Tabla 20 Makis Acebichados y Furai",
        category="makis",
        category_name="Makis & Sushi",
        brand="Hanzo Nikkei / Rappi",
        price=32.90,
        original_price=58.00,
        discount_percent=43,
        platform="Rappi",
        platform_color="#ff441f",
        description="Dúo de 20 cortes nikkei: 10 acebichados con salsa clásica de la casa y 10 furai empanizados con panko crujiente.",
        image_url="https://images.unsplash.com/photo-1579871494447-9811cf80d66c?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.rappi.com.pe/",
        coupon_code="RAPPIMAKI",
        expiration="De Lunes a Jueves en Rappi",
        location="Miraflores, San Isidro, Surco, San Borja",
        districts=["todas", "miraflores", "surco", "lima_centro"],
        is_promo=True,
        delivery_time="30-40 min"
    ),
    FoodDeal(
        id="food-rap-4",
        title="Rappi Prime: 1/4 Pollo a la Brasa Pardos + Papas + Ensalada",
        category="pollo",
        category_name="Pollo a la Brasa",
        brand="Pardos Chicken / Rappi",
        price=26.90,
        original_price=38.90,
        discount_percent=31,
        platform="Rappi",
        platform_color="#ff441f",
        description="Cuarto de pollo marinado con sabor tradicional Pardos, papas fritas doradas y todas sus cremas peruanas.",
        image_url="https://images.unsplash.com/photo-1527477321005-4d01d702334b?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.rappi.com.pe/",
        coupon_code="PRIMEPOLLO",
        expiration="Exclusivo miembros Rappi",
        location="Lima Metropolitana",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_sur", "callao", "arequipa"],
        is_promo=True,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="food-rap-5",
        title="Rappi Super Pack: KFC Mega Bucket 8 Piezas Broaster + Papas",
        category="pollo",
        category_name="Pollo a la Brasa",
        brand="KFC / Rappi",
        price=39.90,
        original_price=59.90,
        discount_percent=33,
        platform="Rappi",
        platform_color="#ff441f",
        description="Balde familiar con 8 presas crujientes de pollo receta original o crispy, porción familiar de papas y salsas.",
        image_url="https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.rappi.com.pe/",
        coupon_code="RAPPIKFC",
        expiration="Viernes, Sábado y Domingo",
        location="Nacional",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_norte", "lima_sur", "lima_este", "callao", "arequipa", "trujillo"],
        is_promo=True,
        delivery_time="30-40 min"
    ),
    FoodDeal(
        id="food-rap-6",
        title="Rappi Chifa: Banquete Chinawok Chaufa Familiar + 8 Wantanes",
        category="chifa",
        category_name="Chifa",
        brand="Chinawok / Rappi",
        price=29.90,
        original_price=45.90,
        discount_percent=35,
        platform="Rappi",
        platform_color="#ff441f",
        description="Fuente familiar de arroz chaufa especial con trozos de pollo, cebollita china, sillao cantonés y 8 wantanes crocantes.",
        image_url="https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.rappi.com.pe/",
        coupon_code="RAPPIWOK",
        expiration="Válido en delivery Rappi",
        location="Lima y Provincias",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_norte", "lima_sur", "callao", "arequipa"],
        is_promo=True,
        delivery_time="25-35 min"
    ),

    # ==========================================
    # --- YAPE PROMOS (VERIFICADAS PERÚ) ---
    # ==========================================
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
        platform_color="#7c3aed", # Yape Purple
        description="La clásica hamburguesa peruana al carbón con tomate, lechuga, mayonesa casera, papas fritas crocantes y gaseosa.",
        image_url="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.bembos.com.pe/",
        coupon_code="YAPEBEMBOS",
        expiration="Exclusivo pagando con Yape",
        location="Nacional (Todas las sedes)",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_norte", "lima_sur", "lima_este", "callao", "arequipa", "trujillo"],
        is_promo=True,
        delivery_time="25-35 min"
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
        expiration="Hasta agotar cupones",
        location="Nacional",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_norte", "lima_sur", "lima_este", "callao", "arequipa", "trujillo"],
        is_promo=True,
        delivery_time="25-35 min"
    ),
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
        platform_color="#7c3aed",
        description="Masa clásica artesanal con queso mozzarella, salsa de tomate de la casa y pepperoni americano. Incluye gaseosa personal.",
        image_url="https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.pizzahut.com.pe/",
        coupon_code="YAPEHUT15",
        expiration="Válido de Lunes a Domingo",
        location="Nacional",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_norte", "lima_sur", "lima_este", "callao", "arequipa", "trujillo"],
        is_promo=True,
        delivery_time="30-40 min"
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
        expiration="Lunes a Domingo",
        location="Lima y Provincias",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_norte", "lima_sur", "callao", "arequipa"],
        is_promo=True,
        delivery_time="25-35 min"
    ),
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
        expiration="Todo el día",
        location="Nacional",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_norte", "lima_sur", "lima_este", "callao", "arequipa", "trujillo"],
        is_promo=True,
        delivery_time="30-45 min"
    ),
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
        expiration="Lunes a Jueves",
        location="Lima Centro, Miraflores, Surco",
        districts=["todas", "miraflores", "surco", "lima_centro"],
        is_promo=True,
        delivery_time="30-40 min"
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
        expiration="De 3:00 PM a 7:00 PM",
        location="Lima y Provincias",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_sur", "callao", "arequipa", "trujillo"],
        is_promo=True,
        delivery_time="20-30 min"
    ),
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
        expiration="Válido en todos los locales",
        location="Nacional",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_norte", "lima_sur", "lima_este", "callao", "arequipa", "trujillo"],
        is_promo=True,
        delivery_time="25-35 min"
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
        expiration="Hasta agotar stock",
        location="Nacional",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_norte", "lima_sur", "lima_este", "callao", "arequipa", "trujillo"],
        is_promo=True,
        delivery_time="30-40 min"
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
        expiration="Lunes a Viernes",
        location="Lima y Provincias",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_sur", "callao", "arequipa", "trujillo"],
        is_promo=True,
        delivery_time="25-35 min"
    ),

    # ==========================================
    # --- COMBOS FAMILIARES & APPS OFICIALES ---
    # ==========================================
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
        platform_color="#ea580c",
        description="Pizza grande de 8 porciones recién horneada al instante con mozzarella premium y pepperoni abundante.",
        image_url="https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=600&q=80",
        deal_url="https://littlecaesars.pe/",
        coupon_code=None,
        expiration="Precio permanente en tienda y delivery",
        location="Lima Metropolitana",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_norte", "lima_sur", "callao"],
        is_promo=True,
        delivery_time="20-30 min"
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
        platform_color="#0284c7",
        description="Dúo de pizzas medianas masa delgada o pan con salsa marinara italiana y queso 100% mozzarella.",
        image_url="https://images.unsplash.com/photo-1593560708920-61dd98c46a4e?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.dominos.com.pe/",
        coupon_code="DUODOMINOS",
        expiration="Todo el mes",
        location="Nacional",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_norte", "lima_sur", "lima_este", "callao", "arequipa", "trujillo"],
        is_promo=True,
        delivery_time="30-40 min"
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
        platform_color="#dc2626",
        description="Medio pollo con el inconfundible sabor Pardos a la brasa, papas fritas doradas y sus cremas tradicionales.",
        image_url="https://images.unsplash.com/photo-1527477321005-4d01d702334b?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.pardoschicken.pe/",
        coupon_code="PARDOSAPP",
        expiration="Pedidos online",
        location="Lima y Provincias",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_sur", "callao", "arequipa", "trujillo"],
        is_promo=True,
        delivery_time="30-45 min"
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
        platform_color="#c5a880",
        description="Dos pizzas familiares a elección (Super Papa, All the Meats o Pepperoni) con salsa de ajo especial y gaseosa familiar.",
        image_url="https://images.unsplash.com/photo-1534308983496-4fabb1a015ee?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.papajohns.com.pe/",
        coupon_code="FAMILIAR50",
        expiration="Fines de semana y feriados",
        location="Nacional",
        districts=["todas", "miraflores", "surco", "lima_centro", "lima_norte", "lima_sur", "lima_este", "callao", "arequipa", "trujillo"],
        is_promo=True,
        delivery_time="35-45 min"
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
        expiration="Válido de Lunes a Domingo",
        location="Nacional",
        districts=["todas", "cajamarca", "miraflores", "surco", "lima_centro", "lima_norte", "lima_sur", "lima_este", "callao", "arequipa", "trujillo"],
        is_promo=True,
        delivery_time="35-50 min"
    ),

    # ==========================================
    # --- ESPECIALES CAJAMARCA (DELIVERY & LOCAL) ---
    # ==========================================
    FoodDeal(
        id="food-caj-1",
        title="Combo Bembos Cajamarca: Clásica Mediana + Papas + Gaseosa",
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
        deal_url="https://www.bembos.com.pe/",
        coupon_code="YAPECAJAMARCA",
        expiration="Válido en Real Plaza Cajamarca",
        location="Cajamarca (Real Plaza / Centro)",
        districts=["todas", "cajamarca"],
        is_promo=True,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="food-caj-2",
        title="Porción Manjar Blanco Tradicional con Queso Mantecoso y Rosquitas",
        category="postres",
        category_name="Postres & Café",
        brand="Dulces Tradicionales Cajamarca",
        price=12.50,
        original_price=18.00,
        discount_percent=31,
        platform="Delivery Local",
        platform_color="#c5a880",
        description="Auténtico manjar blanco de leche fresca cajamarquina acompañado de queso mantecoso y paquete de rosquitas artesanales.",
        image_url="https://images.unsplash.com/photo-1541696432-82c6da8ce7bf?auto=format&fit=crop&w=600&q=80",
        deal_url="https://yape.com.pe/promociones",
        coupon_code="DULCECAJ",
        expiration="Todo el año",
        location="Cajamarca (Centro y Baños del Inca)",
        districts=["todas", "cajamarca"],
        is_promo=True,
        delivery_time="20-30 min"
    ),
    FoodDeal(
        id="food-caj-3",
        title="Chifa Cajamarca: Aeropuerto Salteado al Wok + 4 Wantanes Fritos",
        category="chifa",
        category_name="Chifa",
        brand="Chifa Tradicional Cajamarca",
        price=14.90,
        original_price=22.00,
        discount_percent=32,
        platform="PedidosYa",
        platform_color="#ea1d2c",
        description="Arroz chaufa con tallarín saltado, trozos de pollo, cebolla china y 4 wantanes crujientes con salsa tamarindo en Cajamarca.",
        image_url="https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.pedidosya.com.pe/",
        coupon_code="WOKCAJ",
        expiration="Válido en delivery PedidosYa Cajamarca",
        location="Cajamarca Ciudad",
        districts=["todas", "cajamarca"],
        is_promo=True,
        delivery_time="25-35 min"
    ),
    FoodDeal(
        id="food-caj-4",
        title="Combo 1/4 Pollo a la Brasa con Papas y Chicha en El Quinde",
        category="pollo",
        category_name="Pollo a la Brasa",
        brand="Rókys / El Quinde Cajamarca",
        price=15.90,
        original_price=26.90,
        discount_percent=41,
        platform="PedidosYa",
        platform_color="#ea1d2c",
        description="Cuarto de pollo dorado a la leña, papas fritas doradas, cremas de ají casero y chicha en El Quinde Shopping Plaza Cajamarca.",
        image_url="https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.pedidosya.com.pe/",
        coupon_code="PEDIDOSCAJ",
        expiration="Lunes a Domingo por PedidosYa",
        location="Cajamarca (El Quinde y Centro)",
        districts=["todas", "cajamarca"],
        is_promo=True,
        delivery_time="25-40 min"
    ),
    FoodDeal(
        id="food-caj-5",
        title="Pizza Mediana Americana o Pepperoni en El Quinde Cajamarca",
        category="pizza",
        category_name="Pizzas",
        brand="Pizza Hut / El Quinde",
        price=16.90,
        original_price=32.90,
        discount_percent=49,
        platform="Yape Promos",
        platform_color="#7c3aed",
        description="Pizza mediana recién horneada con mozzarella y pepperoni americano en El Quinde Cajamarca pagando con Yape.",
        image_url="https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=600&q=80",
        deal_url="https://www.pizzahut.com.pe/",
        coupon_code="YAPEHUTCAJ",
        expiration="Todo el mes con Yape",
        location="Cajamarca (El Quinde)",
        districts=["todas", "cajamarca"],
        is_promo=True,
        delivery_time="30-45 min"
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
    if category and category.lower() != "todas":
        clean_cat = category.strip().lower()
        filtered = [f for f in filtered if f.category.lower() == clean_cat]

    # 2. Filter by platform/app if provided (Yape, Rappi, App Oficial, etc.)
    if platform and platform.lower() != "todas":
        clean_plat = platform.strip().lower()
        filtered = [f for f in filtered if clean_plat in f.platform.lower()]

    # 3. Filter by location / district if provided
    if location and location.lower() != "todas":
        loc = location.strip().lower()
        filtered = [
            f for f in filtered
            if "todas" in f.districts or "nacional" in f.location.lower() or loc in f.districts or loc in f.location.lower()
        ]

    # 4. Filter by only discounts / promotions if requested
    if only_discounts:
        filtered = [f for f in filtered if f.is_promo and (f.discount_percent or 0) > 0]

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
        "location": location,
        "only_discounts": only_discounts,
        "sort_by": sort_by,
        "stats": stats,
        "categories": cat_counts,
        "supported_locations": SUPPORTED_LOCATIONS,
        "results": [f.to_dict() for f in filtered]
    }
