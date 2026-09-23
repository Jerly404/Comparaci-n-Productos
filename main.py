from typing import Optional, List
import uvicorn
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from scrapers.manager import SearchManager

app = FastAPI(
    title="Comparador de Precios de Celulares Perú",
    description="Sistema inteligente que busca teléfonos en las principales tiendas peruanas y los ordena de menor a mayor precio.",
    version="1.0.0"
)

manager = SearchManager()

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

@app.get("/api/search")
async def search_phones(
    q: str = Query(..., description="Nombre o modelo del celular (ej: iPhone 13, Samsung S24, Xiaomi Redmi Note 13)"),
    stores: Optional[str] = Query(None, description="Tiendas separadas por comas (falabella,ripley,plazavea,coolbox,oechsle,promart,hiraoka)"),
    sort: str = Query("asc", description="Criterio de ordenación: 'asc' (menor a mayor precio), 'desc', 'discount'"),
    hide_accessories: bool = Query(True, description="Filtrar fundas, cables, micas y accesorios"),
    include_refurbished: bool = Query(True, description="Incluir celulares reacondicionados o seminuevos"),
    min_price: Optional[float] = Query(None, description="Precio mínimo en soles"),
    max_price: Optional[float] = Query(None, description="Precio máximo en soles")
):
    selected_stores = [s.strip().lower() for s in stores.split(",")] if stores else None
    
    result = await manager.search_all(
        query=q,
        stores=selected_stores,
        hide_accessories=hide_accessories,
        include_refurbished=include_refurbished,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort
    )
    return result

@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "phone-price-comparator"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
