# 📱 BuscaFono Perú - Comparador de Precios de Celulares

Sistema inteligente y concurrente que busca cualquier modelo de teléfono celular en las principales tiendas de retail de Perú y lista los resultados ordenados estrictamente de **menor precio a mayor precio**, destacando la mejor oferta y permitiendo compras directas al precio más bajo.

---

## 🏬 Tiendas Integradas en Tiempo Real

El sistema realiza búsquedas asíncronas y simultáneas en:

1. **Falabella Perú** (`falabella.com.pe`)
2. **Ripley Perú** (`ripley.com.pe`)
3. **PlazaVea** (`plazavea.com.pe`)
4. **Claro Perú** (`tiendaclaro.pe`)
5. **Entel Perú** (`entel.pe` / `miportal.entel.pe`)
6. **Coolbox Perú** (`coolbox.pe`)
7. **Hiraoka** (`hiraoka.com.pe`)
8. **La Curacao** (`lacuracao.pe`)
9. **Tiendas EFE** (`efe.com.pe`)
10. **Oechsle** (`oechsle.pe`)
11. **Promart** (`promart.pe`)
12. **Shopstar** (`shopstar.pe`)

---

## ✨ Características Principales

- **Orden Estricto por Precio**: Por defecto, los resultados se ordenan de menor a mayor precio (`S/`), permitiendo encontrar de inmediato el celular más barato.
- **Card de Mejor Oferta (#1 Más Barato)**: Destaca visualmente el teléfono con el precio más bajo entre todas las tiendas, mostrando el ahorro estimado frente al promedio del mercado.
- **Filtrado Inteligente de Accesorios**: Elimina automáticamente fundas, protectores, cables, cargadores, micas, monitores y repuestos para asegurar que solo veas teléfonos reales (a menos que busques un accesorio explícitamente).
- **Detección de Condición**: Identifica y etiqueta si el celular es **Nuevo** o **Reacondicionado**, permitiendo filtrar según tu preferencia.
- **Filtros por Tienda y Rango de Precio**: Selecciona o deselecciona tiendas específicas según tus tiendas de confianza.
- **Doble Interfaz**:
  - **Interfaz Web Moderna**: Diseñada con Tailwind CSS, tema oscuro elegante, imágenes de alta resolución, estadísticas en vivo y exportación a CSV.
  - **CLI Interactivo (Terminal)**: Ideal para terminales como Kitty, mostrando tablas estilizadas con colores y emojis usando Python `Rich`.

---

## 🚀 Instalación y Puesta en Marcha

### 1. Requisitos
- Python 3.10+ (probado en Python 3.14 en Arch Linux)

### 2. Configuración del entorno
```bash
cd /home/jerly404/dev/comparador-precios-celulares
# El entorno virtual ya se encuentra creado en ./venv
# Si deseas reinstalar dependencias:
./venv/bin/pip install -r requirements.txt
```

---

## 🌐 1. Iniciar la Interfaz Web

Para iniciar el servidor web:

```bash
./venv/bin/python main.py
```

Luego abre tu navegador en:
👉 **[http://localhost:8000](http://localhost:8000)**

### ¿Qué puedes hacer en la Web?
- Escribir cualquier modelo de teléfono (ej. `iPhone 13`, `Galaxy S24`, `Xiaomi Redmi Note 13`, `POCO X6 Pro`).
- Ver en segundos todas las ofertas ordenadas de menor a mayor.
- Ver la tarjeta destacada **"Mejor Oferta Encontrada"** con enlace directo a la tienda.
- Filtrar por tiendas específicas (Falabella, Ripley, etc.).
- Descargar la comparativa completa a un archivo **CSV**.

---

## 💻 2. Uso desde la Terminal (CLI)

Ideal para consultas ultrarrápidas desde Kitty:

```bash
# Búsqueda básica ordenada de menor a mayor
./venv/bin/python cli.py "iPhone 13"

# Buscar excluyendo teléfonos reacondicionados
./venv/bin/python cli.py "Samsung S24" --no-refurbished

# Limitar a las 10 mejores ofertas
./venv/bin/python cli.py "Xiaomi Redmi Note 13" --limit 10

# Filtrar solo ciertas tiendas (ej: Ripley y PlazaVea)
./venv/bin/python cli.py "iPhone 15" --stores ripley,plazavea
```

---

## 🛠️ Arquitectura del Proyecto

```
comparador-precios-celulares/
├── scrapers/
│   ├── base.py              # Modelo de datos ProductItem y BaseScraper
│   ├── filter_utils.py      # Filtros de accesorios, relevancia y condición
│   ├── falabella.py         # Scraper de Falabella Perú
│   ├── ripley.py            # Scraper de Ripley Perú
│   ├── vtex_base.py         # Scraper base para tiendas VTEX
│   ├── plazavea.py          # Scraper de PlazaVea
│   ├── coolbox.py           # Scraper de Coolbox
│   ├── oechsle.py           # Scraper de Oechsle
│   ├── promart.py           # Scraper de Promart
│   ├── hiraoka.py           # Scraper de Hiraoka
│   └── manager.py           # Orquestador asíncrono y calculador de métricas
├── static/
│   ├── index.html           # Frontend web responsivo con Tailwind CSS
│   ├── app.js               # Lógica cliente y consumo de API
│   └── style.css            # Estilos y animaciones
├── main.py                  # API FastAPI y servidor de archivos estáticos
├── cli.py                   # Herramienta de línea de comandos con Rich
├── requirements.txt
└── README.md
```

---

## 📄 Licencia

MIT - Desarrollado para uso libre y personal.
