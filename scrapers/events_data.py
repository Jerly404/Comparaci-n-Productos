from datetime import datetime
from typing import List, Dict, Any

UPCOMING_EVENTS: List[Dict[str, Any]] = [
    {
        "id": "cyber-wow-octubre",
        "name": "Cyber Wow Perú 2026",
        "badge": "Próximo Gran Evento",
        "organizer": "IAB Perú (Interactive Advertising Bureau)",
        "start_date": "2026-10-26T00:00:00-05:00",
        "end_date": "2026-10-30T23:59:59-05:00",
        "display_date": "26 al 30 de Octubre, 2026",
        "discount_estimate": "30% a 55% OFF",
        "stores": ["Falabella", "Ripley", "PlazaVea", "Claro", "Entel", "Coolbox", "La Curacao", "Tiendas EFE", "Oechsle", "Promart", "Shopstar"],
        "description": "El evento de compras online más importante del último trimestre en Perú. Las marcas de tecnología suelen liquidar inventario previo a fiestas de fin de año.",
        "tips": "Los mayores descuentos en iPhone y Samsung suelen agotarse en las primeras 4 horas (a partir de las 00:00 del 26 de octubre)."
    },
    {
        "id": "cyber-days-noviembre",
        "name": "Cyber Days CCL",
        "badge": "Edición Fin de Año",
        "organizer": "Cámara de Comercio de Lima (CCL)",
        "start_date": "2026-11-09T00:00:00-05:00",
        "end_date": "2026-11-13T23:59:59-05:00",
        "display_date": "09 al 13 de Noviembre, 2026",
        "discount_estimate": "25% a 50% OFF",
        "stores": ["Falabella", "Ripley", "Claro", "Entel", "Hiraoka", "Coolbox", "PlazaVea", "La Curacao", "Tiendas EFE"],
        "description": "Edición oficial organizada por la Cámara de Comercio de Lima con foco en garantías oficiales y financiamiento sin intereses.",
        "tips": "Compara las promociones de cuotas sin intereses con tarjetas BBVA, BCP e Interbank en retailers certificados."
    },
    {
        "id": "black-friday",
        "name": "Black Friday Perú 2026",
        "badge": "Mayor Descuento Global",
        "organizer": "Comercio Minorista Global & Retail Perú",
        "start_date": "2026-11-27T00:00:00-05:00",
        "end_date": "2026-11-29T23:59:59-05:00",
        "display_date": "Viernes 27 de Noviembre, 2026",
        "discount_estimate": "35% a 65% OFF",
        "stores": ["Todas las tiendas (Falabella, Ripley, Claro, Entel, Coolbox, Hiraoka, etc.)"],
        "description": "El día con los mayores descuentos internacionales y locales del año. Operadores como Claro y Entel lanzan portabilidades con equipos al costo o cuota inicial cero.",
        "tips": "Revisa los precios base dos semanas antes para confirmar que el descuento de Black Friday sea real y no un precio inflado."
    },
    {
        "id": "cyber-monday",
        "name": "Cyber Monday Perú 2026",
        "badge": "Especial Tecnología",
        "organizer": "E-Commerce Perú",
        "start_date": "2026-11-30T00:00:00-05:00",
        "end_date": "2026-12-02T23:59:59-05:00",
        "display_date": "Lunes 30 de Noviembre, 2026",
        "discount_estimate": "30% a 50% OFF",
        "stores": ["Falabella", "Ripley", "Coolbox", "Hiraoka", "Shopstar", "PlazaVea"],
        "description": "Extensión digital del Black Friday dedicada exclusivamente a productos de electrónica, computación y telefonía móvil.",
        "tips": "Ideal para accesorios premium, combos de celular + smartwatch y modelos tope de gama de la temporada anterior."
    },
    {
        "id": "navidad-tech",
        "name": "Venta Navideña & Fin de Año",
        "badge": "Cierre de Temporada",
        "organizer": "Retail Perú & Operadores",
        "start_date": "2026-12-10T00:00:00-05:00",
        "end_date": "2026-12-24T23:59:59-05:00",
        "display_date": "10 al 24 de Diciembre, 2026",
        "discount_estimate": "20% a 45% OFF",
        "stores": ["Falabella", "Ripley", "Claro", "Entel", "PlazaVea", "Hiraoka", "La Curacao", "Tiendas EFE"],
        "description": "Campañas de renovación de equipos y combos de regalo navideño con alta disponibilidad de stock para entrega inmediata.",
        "tips": "Ten cuidado con los plazos de envío; para compras navideñas, adquiere antes del 18 de diciembre."
    }
]

def get_events() -> List[Dict[str, Any]]:
    return UPCOMING_EVENTS
