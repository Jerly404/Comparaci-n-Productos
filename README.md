# ComparaYa Perú

Comparador web de precios que consulta en paralelo las principales tiendas peruanas, ordena las ofertas y envía al usuario directamente a la tienda elegida.

## Funciones

- Búsqueda concurrente en 14 tiendas.
- Filtros por tienda, ubicación, descuento, accesorios y condición.
- Mejor oferta, precio promedio y ahorro posible.
- Favoritos persistentes en el navegador y comparación de hasta tres productos.
- Exportación CSV, diseño responsive y API documentada en `/docs`.
- Compresión HTTP y caché temporal de búsquedas repetidas.

## Ejecutar localmente

Requiere Python 3.10 o superior.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Abre `http://localhost:8000`. Comprueba el servicio en `http://localhost:8000/api/health`.

## Publicar gratis en Render

El repositorio incluye `render.yaml`, por lo que no hace falta configurar comandos manualmente.

1. Sube este proyecto a GitHub:

   ```bash
   git add .
   git commit -m "Mejora diseño y prepara despliegue"
   git branch -M main
   git remote add origin https://github.com/Jerly404/Comparaci-n-Productos.git
   git push -u origin main
   ```

   Si `origin` ya existe, omite el comando `git remote add origin`.

2. Crea una cuenta en [Render](https://render.com), selecciona **New → Blueprint** y conecta el repositorio.
3. Confirma el servicio `comparaya-peru`. Render detectará el plan gratuito y publicará una URL `*.onrender.com`.
4. Cuando el estado sea **Live**, abre la URL y prueba una búsqueda.

Render apaga los servicios gratuitos tras 15 minutos sin tráfico. La primera visita posterior puede tardar cerca de un minuto; las siguientes serán rápidas. Para un comparador de uso personal o demostración es una buena opción porque FastAPI necesita un servidor y no puede alojarse únicamente en GitHub Pages.

## Estructura

```text
main.py              API FastAPI y frontend
static/              HTML, CSS y JavaScript sin dependencias externas
scrapers/            conectores y normalización de productos
render.yaml          despliegue gratuito reproducible
requirements.txt     dependencias Python
```

## Aviso

Los precios, stock, envío y medios de pago pueden cambiar en la tienda. ComparaYa no procesa pagos: solo organiza información pública y enlaza al comercio.
