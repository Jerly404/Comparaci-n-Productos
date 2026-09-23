"""
Peruvian Supermarket Price Comparator (Canasta Básica Familiar)
Compares prices across PlazaVea, Metro, Tottus, and regional Cajamarca stores.
Sorted strictly lowest-to-highest price.
"""

from typing import List, Dict, Optional, Any

GROCERIES_DATABASE = [
    {
        "id": "arroz-costeno-5kg",
        "name": "Arroz Extra Costeño Bolsa 5kg",
        "category": "abarrotes",
        "category_label": "Abarrotes",
        "image_url": "https://plazavea.vteximg.com.br/arquivos/ids/26359560-450-450/47632.jpg",
        "unit": "Bolsa 5 kg",
        "prices": [
            {"store": "Metro", "store_id": "metro", "color": "#ffd200", "price": 21.90, "original_price": 24.50, "url": "https://www.metro.pe/arroz-extra-costeno-bolsa-5-kg/p", "pickup_cajamarca": "El Quinde Cajamarca"},
            {"store": "Tottus", "store_id": "tottus", "color": "#00873d", "price": 22.50, "original_price": 24.90, "url": "https://tottus.falabella.com.pe/tottus-pe", "pickup_cajamarca": "Envío a Domicilio"},
            {"store": "PlazaVea", "store_id": "plazavea", "color": "#d9232a", "price": 22.90, "original_price": 25.20, "url": "https://www.plazavea.com.pe/arroz-extra-costeno-5kg/p", "pickup_cajamarca": "Real Plaza Cajamarca"}
        ]
    },
    {
        "id": "aceite-primor-900ml",
        "name": "Aceite Vegetal Primor Clásico Botella 900ml",
        "category": "abarrotes",
        "category_label": "Abarrotes",
        "image_url": "https://plazavea.vteximg.com.br/arquivos/ids/26360124-450-450/47599.jpg",
        "unit": "Botella 900 ml",
        "prices": [
            {"store": "Metro", "store_id": "metro", "color": "#ffd200", "price": 7.80, "original_price": 8.90, "url": "https://www.metro.pe/aceite-primor-clasico-900ml/p", "pickup_cajamarca": "El Quinde Cajamarca"},
            {"store": "Tottus", "store_id": "tottus", "color": "#00873d", "price": 8.10, "original_price": 9.00, "url": "https://tottus.falabella.com.pe/tottus-pe", "pickup_cajamarca": "Envío a Domicilio"},
            {"store": "PlazaVea", "store_id": "plazavea", "color": "#d9232a", "price": 8.20, "original_price": 9.20, "url": "https://www.plazavea.com.pe/aceite-vegetal-primor-clasico-botella-900ml/p", "pickup_cajamarca": "Real Plaza Cajamarca"}
        ]
    },
    {
        "id": "leche-gloria-pack6",
        "name": "Leche Evaporada Gloria Azul Pack 6 x 400g",
        "category": "lacteos",
        "category_label": "Lácteos & Huevos",
        "image_url": "https://plazavea.vteximg.com.br/arquivos/ids/27981504-450-450/19080.jpg",
        "unit": "Pack 6 latas",
        "prices": [
            {"store": "Metro", "store_id": "metro", "color": "#ffd200", "price": 23.90, "original_price": 26.50, "url": "https://www.metro.pe/pack-leche-evaporada-gloria-azul-6-latas-400-g/p", "pickup_cajamarca": "El Quinde Cajamarca"},
            {"store": "Tottus", "store_id": "tottus", "color": "#00873d", "price": 24.10, "original_price": 26.80, "url": "https://tottus.falabella.com.pe/tottus-pe", "pickup_cajamarca": "Envío a Domicilio"},
            {"store": "PlazaVea", "store_id": "plazavea", "color": "#d9232a", "price": 24.50, "original_price": 27.00, "url": "https://www.plazavea.com.pe/leche-evaporada-gloria-pack-6un-400g/p", "pickup_cajamarca": "Real Plaza Cajamarca"}
        ]
    },
    {
        "id": "atun-campomar-aceite",
        "name": "Filete de Atún Campomar en Aceite Vegetal 170g",
        "category": "abarrotes",
        "category_label": "Abarrotes",
        "image_url": "https://plazavea.vteximg.com.br/arquivos/ids/26359700-450-450/20050867.jpg",
        "unit": "Lata 170 g",
        "prices": [
            {"store": "Metro", "store_id": "metro", "color": "#ffd200", "price": 5.40, "original_price": 6.50, "url": "https://www.metro.pe/filete-atun-campomar-170g/p", "pickup_cajamarca": "El Quinde Cajamarca"},
            {"store": "Tottus", "store_id": "tottus", "color": "#00873d", "price": 5.70, "original_price": 6.60, "url": "https://tottus.falabella.com.pe/tottus-pe", "pickup_cajamarca": "Envío a Domicilio"},
            {"store": "PlazaVea", "store_id": "plazavea", "color": "#d9232a", "price": 5.80, "original_price": 6.80, "url": "https://www.plazavea.com.pe/filete-de-atun-campomar-aceite-170g/p", "pickup_cajamarca": "Real Plaza Cajamarca"}
        ]
    },
    {
        "id": "azucar-rubia-cartavio-5kg",
        "name": "Azúcar Rubia Doméstica Cartavio Bolsa 5kg",
        "category": "abarrotes",
        "category_label": "Abarrotes",
        "image_url": "https://plazavea.vteximg.com.br/arquivos/ids/26359990-450-450/47600.jpg",
        "unit": "Bolsa 5 kg",
        "prices": [
            {"store": "Metro", "store_id": "metro", "color": "#ffd200", "price": 17.90, "original_price": 20.50, "url": "https://www.metro.pe/azucar-rubia-cartavio-5kg/p", "pickup_cajamarca": "El Quinde Cajamarca"},
            {"store": "Tottus", "store_id": "tottus", "color": "#00873d", "price": 18.50, "original_price": 21.00, "url": "https://tottus.falabella.com.pe/tottus-pe", "pickup_cajamarca": "Envío a Domicilio"},
            {"store": "PlazaVea", "store_id": "plazavea", "color": "#d9232a", "price": 18.90, "original_price": 21.50, "url": "https://www.plazavea.com.pe/azucar-rubia-cartavio-5kg/p", "pickup_cajamarca": "Real Plaza Cajamarca"}
        ]
    },
    {
        "id": "fideos-don-vittorio-950g",
        "name": "Fideos Spaghetti Don Vittorio Paquete 950g",
        "category": "abarrotes",
        "category_label": "Abarrotes",
        "image_url": "https://plazavea.vteximg.com.br/arquivos/ids/26360050-450-450/47602.jpg",
        "unit": "Paquete 950 g",
        "prices": [
            {"store": "Metro", "store_id": "metro", "color": "#ffd200", "price": 4.50, "original_price": 5.40, "url": "https://www.metro.pe/fideos-spaghetti-don-vittorio-950g/p", "pickup_cajamarca": "El Quinde Cajamarca"},
            {"store": "PlazaVea", "store_id": "plazavea", "color": "#d9232a", "price": 4.70, "original_price": 5.50, "url": "https://www.plazavea.com.pe/fideos-spaghetti-don-vittorio-950g/p", "pickup_cajamarca": "Real Plaza Cajamarca"},
            {"store": "Tottus", "store_id": "tottus", "color": "#00873d", "price": 4.80, "original_price": 5.60, "url": "https://tottus.falabella.com.pe/tottus-pe", "pickup_cajamarca": "Envío a Domicilio"}
        ]
    },
    {
        "id": "huevos-pardos-bandeja-30",
        "name": "Huevos Pardos Frescos Bandeja x 30 Unidades",
        "category": "lacteos",
        "category_label": "Lácteos & Huevos",
        "image_url": "https://plazavea.vteximg.com.br/arquivos/ids/26360350-450-450/47610.jpg",
        "unit": "Bandeja 30 unid",
        "prices": [
            {"store": "Metro", "store_id": "metro", "color": "#ffd200", "price": 17.50, "original_price": 19.90, "url": "https://www.metro.pe/huevos-pardos-30-unid/p", "pickup_cajamarca": "El Quinde Cajamarca"},
            {"store": "Tottus", "store_id": "tottus", "color": "#00873d", "price": 18.20, "original_price": 20.50, "url": "https://tottus.falabella.com.pe/tottus-pe", "pickup_cajamarca": "Envío a Domicilio"},
            {"store": "PlazaVea", "store_id": "plazavea", "color": "#d9232a", "price": 18.50, "original_price": 20.90, "url": "https://www.plazavea.com.pe/huevos-pardos-bandeja-30-unid/p", "pickup_cajamarca": "Real Plaza Cajamarca"}
        ]
    },
    {
        "id": "pollo-pechuga-1kg",
        "name": "Pechuga de Pollo Fresca con Hueso y Piel 1kg",
        "category": "carnes",
        "category_label": "Carnes & Aves",
        "image_url": "https://plazavea.vteximg.com.br/arquivos/ids/26360480-450-450/47615.jpg",
        "unit": "Por Kilo",
        "prices": [
            {"store": "Metro", "store_id": "metro", "color": "#ffd200", "price": 15.90, "original_price": 18.50, "url": "https://www.metro.pe/pechuga-pollo-kilo/p", "pickup_cajamarca": "El Quinde Cajamarca"},
            {"store": "Tottus", "store_id": "tottus", "color": "#00873d", "price": 16.00, "original_price": 18.90, "url": "https://tottus.falabella.com.pe/tottus-pe", "pickup_cajamarca": "Envío a Domicilio"},
            {"store": "PlazaVea", "store_id": "plazavea", "color": "#d9232a", "price": 16.50, "original_price": 19.20, "url": "https://www.plazavea.com.pe/pechuga-de-pollo-kilo/p", "pickup_cajamarca": "Real Plaza Cajamarca"}
        ]
    },
    {
        "id": "detergente-bolivar-4kg",
        "name": "Detergente en Polvo Bolívar Active Care / Floral 4kg",
        "category": "limpieza",
        "category_label": "Limpieza del Hogar",
        "image_url": "https://plazavea.vteximg.com.br/arquivos/ids/26360600-450-450/47620.jpg",
        "unit": "Bolsa 4 kg",
        "prices": [
            {"store": "Metro", "store_id": "metro", "color": "#ffd200", "price": 36.90, "original_price": 42.00, "url": "https://www.metro.pe/detergente-bolivar-4kg/p", "pickup_cajamarca": "El Quinde Cajamarca"},
            {"store": "Tottus", "store_id": "tottus", "color": "#00873d", "price": 37.90, "original_price": 43.50, "url": "https://tottus.falabella.com.pe/tottus-pe", "pickup_cajamarca": "Envío a Domicilio"},
            {"store": "PlazaVea", "store_id": "plazavea", "color": "#d9232a", "price": 38.90, "original_price": 44.90, "url": "https://www.plazavea.com.pe/detergente-bolivar-active-care-4kg/p", "pickup_cajamarca": "Real Plaza Cajamarca"}
        ]
    },
    {
        "id": "nescafe-tradicion-200g",
        "name": "Café Soluble Nescafé Tradición Frasco 200g",
        "category": "abarrotes",
        "category_label": "Abarrotes",
        "image_url": "https://plazavea.vteximg.com.br/arquivos/ids/26360700-450-450/47625.jpg",
        "unit": "Frasco 200 g",
        "prices": [
            {"store": "Metro", "store_id": "metro", "color": "#ffd200", "price": 24.90, "original_price": 28.90, "url": "https://www.metro.pe/nescafe-tradicion-200g/p", "pickup_cajamarca": "El Quinde Cajamarca"},
            {"store": "Tottus", "store_id": "tottus", "color": "#00873d", "price": 25.90, "original_price": 29.50, "url": "https://tottus.falabella.com.pe/tottus-pe", "pickup_cajamarca": "Envío a Domicilio"},
            {"store": "PlazaVea", "store_id": "plazavea", "color": "#d9232a", "price": 26.50, "original_price": 30.00, "url": "https://www.plazavea.com.pe/nescafe-tradicion-frasco-200g/p", "pickup_cajamarca": "Real Plaza Cajamarca"}
        ]
    },
    {
        "id": "queso-mantecoso-cajamarca-500g",
        "name": "Queso Mantecoso Tradicional de Cajamarca 500g",
        "category": "cajamarca",
        "category_label": "Especial Cajamarca",
        "image_url": "https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?auto=format&fit=crop&w=450&q=80",
        "unit": "Molde 500 g",
        "prices": [
            {"store": "Mercado Local Cajamarca", "store_id": "local_cajamarca", "color": "#c5a880", "price": 13.00, "original_price": 15.00, "url": "https://www.google.com/maps/search/Mercado+Central+Cajamarca", "pickup_cajamarca": "Centro Cajamarca (In situ)"},
            {"store": "Metro", "store_id": "metro", "color": "#ffd200", "price": 15.50, "original_price": 17.50, "url": "https://www.metro.pe/queso-mantecoso-cajamarca/p", "pickup_cajamarca": "El Quinde Cajamarca"},
            {"store": "PlazaVea", "store_id": "plazavea", "color": "#d9232a", "price": 16.90, "original_price": 18.90, "url": "https://www.plazavea.com.pe/queso-mantecoso-cajamarquino-500g/p", "pickup_cajamarca": "Real Plaza Cajamarca"}
        ]
    },
    {
        "id": "manjar-blanco-cajamarca-500g",
        "name": "Manjar Blanco Artesanal Cajamarca Pote 500g",
        "category": "cajamarca",
        "category_label": "Especial Cajamarca",
        "image_url": "https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=450&q=80",
        "unit": "Pote 500 g",
        "prices": [
            {"store": "Dulcería Huacariz Cajamarca", "store_id": "local_cajamarca", "color": "#c5a880", "price": 10.00, "original_price": 12.00, "url": "https://www.google.com/maps/search/Huacariz+Cajamarca", "pickup_cajamarca": "Chonta / Centro Cajamarca"},
            {"store": "Metro", "store_id": "metro", "color": "#ffd200", "price": 11.90, "original_price": 13.50, "url": "https://www.metro.pe/manjar-blanco-cajamarca/p", "pickup_cajamarca": "El Quinde Cajamarca"},
            {"store": "PlazaVea", "store_id": "plazavea", "color": "#d9232a", "price": 12.90, "original_price": 14.50, "url": "https://www.plazavea.com.pe/manjar-blanco-cajamarca-500g/p", "pickup_cajamarca": "Real Plaza Cajamarca"}
        ]
    },
    {
        "id": "avena-3ositos-900g",
        "name": "Avena Tradicional 3 Ositos Bolsa 900g",
        "category": "abarrotes",
        "category_label": "Abarrotes",
        "image_url": "https://plazavea.vteximg.com.br/arquivos/ids/26360800-450-450/47630.jpg",
        "unit": "Bolsa 900 g",
        "prices": [
            {"store": "Metro", "store_id": "metro", "color": "#ffd200", "price": 6.40, "original_price": 7.50, "url": "https://www.metro.pe/avena-3-ositos-900g/p", "pickup_cajamarca": "El Quinde Cajamarca"},
            {"store": "Tottus", "store_id": "tottus", "color": "#00873d", "price": 6.70, "original_price": 7.80, "url": "https://tottus.falabella.com.pe/tottus-pe", "pickup_cajamarca": "Envío a Domicilio"},
            {"store": "PlazaVea", "store_id": "plazavea", "color": "#d9232a", "price": 6.90, "original_price": 7.90, "url": "https://www.plazavea.com.pe/avena-3-ositos-tradicional-900g/p", "pickup_cajamarca": "Real Plaza Cajamarca"}
        ]
    }
]

def search_groceries(
    category: Optional[str] = None,
    query: Optional[str] = None,
    sort_by: str = "asc" # 'asc' (menor a mayor precio del producto más barato), 'desc'
) -> Dict[str, Any]:
    items = list(GROCERIES_DATABASE)

    if category and category != "todas":
        items = [i for i in items if i["category"] == category]

    if query and query.strip():
        q_norm = query.strip().lower()
        items = [i for i in items if q_norm in i["name"].lower() or q_norm in i["category_label"].lower()]

    enriched_items = []
    total_metro_basket = 0.0
    total_tottus_basket = 0.0
    total_plazavea_basket = 0.0
    total_cheapest_basket = 0.0

    for item in items:
        # Sort prices for each grocery item strictly lowest-to-highest
        sorted_prices = sorted(item["prices"], key=lambda p: p["price"])
        cheapest_option = sorted_prices[0]
        highest_option = sorted_prices[-1]
        saving_amount = round(highest_option["price"] - cheapest_option["price"], 2)

        # Basket accumulators
        for p in item["prices"]:
            if p["store_id"] == "metro":
                total_metro_basket += p["price"]
            elif p["store_id"] == "tottus":
                total_tottus_basket += p["price"]
            elif p["store_id"] == "plazavea":
                total_plazavea_basket += p["price"]
        total_cheapest_basket += cheapest_option["price"]

        enriched_item = dict(item)
        enriched_item["prices"] = sorted_prices
        enriched_item["lowest_price"] = cheapest_option["price"]
        enriched_item["cheapest_store"] = cheapest_option["store"]
        enriched_item["cheapest_store_color"] = cheapest_option["color"]
        enriched_item["highest_price"] = highest_option["price"]
        enriched_item["saving_amount"] = saving_amount
        enriched_items.append(enriched_item)

    # Sort items overall: default is asc (lowest price lowest to highest)
    if sort_by == "desc":
        enriched_items.sort(key=lambda x: x["lowest_price"], reverse=True)
    else:
        enriched_items.sort(key=lambda x: x["lowest_price"])

    return {
        "results": enriched_items,
        "stats": {
            "total_items": len(enriched_items),
            "total_metro_basket": round(total_metro_basket, 2),
            "total_plazavea_basket": round(total_plazavea_basket, 2),
            "total_tottus_basket": round(total_tottus_basket, 2),
            "total_cheapest_basket": round(total_cheapest_basket, 2),
            "max_possible_saving": round(max(total_plazavea_basket, total_metro_basket, total_tottus_basket) - total_cheapest_basket, 2)
        },
        "categories": {
            "abarrotes": len([i for i in GROCERIES_DATABASE if i["category"] == "abarrotes"]),
            "lacteos": len([i for i in GROCERIES_DATABASE if i["category"] == "lacteos"]),
            "carnes": len([i for i in GROCERIES_DATABASE if i["category"] == "carnes"]),
            "limpieza": len([i for i in GROCERIES_DATABASE if i["category"] == "limpieza"]),
            "cajamarca": len([i for i in GROCERIES_DATABASE if i["category"] == "cajamarca"])
        }
    }
