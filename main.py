from typing import Optional
import asyncio
import os
import time
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.gzip import GZipMiddleware
from scrapers.manager import SearchManager
from scrapers.events_data import get_events
from scrapers.food_deals import search_food_deals
from scrapers.groceries_data import search_groceries

app = FastAPI(
    title="BuscaProductos Perú - Comparador de Precios Inteligente",
    description="Sistema inteligente de compras en Perú: celulares, tecnología, canasta básica y delivery ordenados de menor a mayor.",
    version="2.0.0"
)

manager = SearchManager()
SEARCH_CACHE_TTL = 300
SEARCH_CACHE_MAX_ITEMS = 100
_search_cache = {}
_cache_lock = asyncio.Lock()

app.add_middleware(GZipMiddleware, minimum_size=700)

@app.middleware("http")
async def production_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    if request.url.path.startswith("/static/"):
        response.headers["Cache-Control"] = "public, max-age=3600"
    elif request.url.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-store"
    return response

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
@app.head("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/api/stores")
async def get_stores():
    """List all supported Peruvian stores."""
    return manager.get_supported_stores()

@app.get("/api/events")
async def get_discount_events():
    """List major upcoming discount events in Peru (Black Friday, Cyber Wow, Cyber Days)."""
    return get_events()

@app.get("/api/groceries")
async def get_groceries(
    category: Optional[str] = Query(None, description="Categoría de canasta básica (abarrotes, lacteos, carnes, limpieza, cajamarca)"),
    q: Optional[str] = Query(None, description="Búsqueda por texto (ej: arroz, aceite, leche Gloria, queso mantecoso)"),
    sort: str = Query("asc", description="Orden: 'asc' (menor a mayor precio), 'desc'")
):
    """Compares prices across Peruvian supermarkets (PlazaVea, Metro, Tottus, Cajamarca local)."""
    return search_groceries(category=category, query=q, sort_by=sort)

@app.get("/api/food-deals")
async def get_food_deals(
    category: Optional[str] = Query(None, description="Categoría de comida (ej: pizza, burger, pollo, makis, chifa, postres)"),
    platform: Optional[str] = Query(None, description="Plataforma (ej: Yape Promos, Rappi, App Oficial, Cuponera / Delivery)"),
    location: Optional[str] = Query(None, description="Localidad o distrito (ej: miraflores, surco, lima_norte, cajamarca, arequipa)"),
    only_discounts: bool = Query(False, description="Filtrar solo ofertas con descuento o ver toda la carta"),
    q: Optional[str] = Query(None, description="Búsqueda por texto (ej: pizza, bembos, kfc, combos)"),
    sort: str = Query("asc", description="Criterio de ordenación: 'asc' (menor a mayor precio), 'desc', 'discount'")
):
    """List real Peruvian food deals, Rappi combos, and menu items sorted strictly lowest-to-highest price."""
    return search_food_deals(
        category=category,
        platform=platform,
        location=location,
        only_discounts=only_discounts,
        query=q,
        sort_by=sort
    )

@app.get("/api/search")
async def search_products(
    q: str = Query(..., min_length=2, max_length=100, description="Nombre o modelo del producto"),
    stores: Optional[str] = Query(None, description="Tiendas separadas por comas (falabella,ripley,plazavea,coolbox,oechsle,promart,hiraoka)"),
    sort: str = Query("asc", description="Criterio de ordenación: 'asc' (menor a mayor precio), 'desc', 'discount'"),
    hide_accessories: bool = Query(True, description="Filtrar fundas, cables, micas y accesorios"),
    include_refurbished: bool = Query(True, description="Incluir celulares reacondicionados o seminuevos"),
    payment: Optional[str] = Query(None, description="Filtro de método de pago: 'all', 'any_card', 'store_cards'"),
    location: Optional[str] = Query("todas", description="Localidad para retiro y disponibilidad (cajamarca, lima, arequipa, trujillo, etc.)"),
    only_discounts: bool = Query(False, description="Filtrar solo productos con descuento activo"),
    pickup_only: bool = Query(False, description="Filtrar solo tiendas con retiro gratis en la localidad seleccionada"),
    pickup_cajamarca: bool = Query(False, description="Filtrar solo tiendas con retiro gratis en Cajamarca (El Quinde / Real Plaza)"),
    verdict: Optional[str] = Query(None, description="Filtro de radar: 'all', 'minimo' (Mínimo Histórico), 'buen_precio'"),
    min_price: Optional[float] = Query(None, description="Precio mínimo en soles"),
    max_price: Optional[float] = Query(None, description="Precio máximo en soles")
):
    q = " ".join(q.split())
    if len(q) < 2:
        raise HTTPException(status_code=422, detail="La búsqueda debe tener al menos 2 caracteres")
    selected_stores = [s.strip().lower() for s in stores.split(",")] if stores else None
    cache_key = (
        q.lower(), tuple(sorted(selected_stores or [])), sort, hide_accessories,
        include_refurbished, payment, location, only_discounts, pickup_only,
        pickup_cajamarca, verdict, min_price, max_price
    )
    now = time.monotonic()
    async with _cache_lock:
        cached = _search_cache.get(cache_key)
        if cached and now - cached[0] < SEARCH_CACHE_TTL:
            return cached[1]

    result = await manager.search_all(
        query=q,
        stores=selected_stores,
        hide_accessories=hide_accessories,
        include_refurbished=include_refurbished,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort,
        payment_filter=payment,
        pickup_cajamarca_only=pickup_cajamarca,
        pickup_only=pickup_only,
        deal_verdict_filter=verdict,
        location=location or "todas",
        only_discounts=only_discounts
    )
    async with _cache_lock:
        if len(_search_cache) >= SEARCH_CACHE_MAX_ITEMS:
            oldest = min(_search_cache, key=lambda key: _search_cache[key][0])
            _search_cache.pop(oldest, None)
        _search_cache[cache_key] = (now, result)
    return result

@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "phone-price-comparator"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
