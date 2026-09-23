#!/usr/bin/env python3
import asyncio
import argparse
from datetime import datetime, timezone
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from scrapers.manager import SearchManager
from scrapers.events_data import get_events
from scrapers.food_deals import search_food_deals
from scrapers.groceries_data import search_groceries

console = Console()

def show_groceries_cli(category: str = None, query: str = None):
    clean_cat = category.lower() if category and category.lower() != "todas" else None
    data = search_groceries(category=clean_cat, query=query)
    results = data.get("results", [])
    stats = data.get("stats", {})

    console.print()
    cat_title = f" - Categoría: {category.capitalize()}" if clean_cat else ""
    console.print(Panel.fit(
        f"[bold #dfc38a]CANASTA BÁSICA FAMILIAR • SUPERMERCADOS PERÚ[/bold #dfc38a]{cat_title}\n"
        f"[dim #cbd5e1]Comparativa de precios entre PlazaVea, Metro y Tottus con retiro en Cajamarca[/dim #cbd5e1]",
        border_style="#8c734b"
    ))

    if not results:
        console.print("[red]No se encontraron productos en la canasta básica.[/red]\n")
        return

    table = Table(border_style="#334155", box=None)
    table.add_column("#", justify="right", style="dim #64748b", no_wrap=True)
    table.add_column("Producto", style="bold #f8fafc")
    table.add_column("Unidad", style="dim #94a3b8", no_wrap=True)
    table.add_column("Metro (El Quinde)", justify="right", style="#ffd200", no_wrap=True)
    table.add_column("Tottus (Envío)", justify="right", style="#00873d", no_wrap=True)
    table.add_column("PlazaVea (Real Plaza)", justify="right", style="#d9232a", no_wrap=True)
    table.add_column("Mejor Precio", justify="right", style="bold #dfc38a", no_wrap=True)
    table.add_column("Ahorro", justify="center", style="bold #10b981", no_wrap=True)

    for i, item in enumerate(results, 1):
        prices_by_store = {p["store_id"]: p["price"] for p in item["prices"]}
        metro_p = f"S/ {prices_by_store['metro']:,.2f}" if 'metro' in prices_by_store else "-"
        tottus_p = f"S/ {prices_by_store['tottus']:,.2f}" if 'tottus' in prices_by_store else "-"
        vea_p = f"S/ {prices_by_store['plazavea']:,.2f}" if 'plazavea' in prices_by_store else "-"
        best_p = f"S/ {item['lowest_price']:,.2f} ({item['cheapest_store']})"
        saving_p = f"+S/ {item['saving_amount']:,.2f}" if item['saving_amount'] > 0 else "-"

        table.add_row(
            str(i),
            item["name"],
            item["unit"],
            metro_p,
            tottus_p,
            vea_p,
            best_p,
            saving_p
        )

    console.print(table)
    console.print(
        f"\n[bold #f8fafc]Resumen Canasta Completa:[/bold #f8fafc] "
        f"Metro: [bold #ffd200]S/ {stats['total_metro_basket']:,.2f}[/bold #ffd200]  •  "
        f"Tottus: [bold #00873d]S/ {stats['total_tottus_basket']:,.2f}[/bold #00873d]  •  "
        f"PlazaVea: [bold #d9232a]S/ {stats['total_plazavea_basket']:,.2f}[/bold #d9232a]  •  "
        f"Ahorro inteligente: [bold #dfc38a]S/ {stats['max_possible_saving']:,.2f}[/bold #dfc38a]\n"
    )

def show_food_cli(category: str = None, query: str = None, location: str = None, only_discounts: bool = False, sort_by: str = "asc"):
    clean_cat = category.lower() if category and category.lower() != "todas" else None
    data = search_food_deals(category=clean_cat, query=query, location=location, only_discounts=only_discounts, sort_by=sort_by)
    results = data.get("results", [])
    stats = data.get("stats", {})

    console.print()
    cat_title = f" - Categoría: {category.capitalize()}" if clean_cat else ""
    loc_title = f" - Sede: {location.capitalize()}" if location and location != "todas" else ""
    console.print(Panel.fit(
        f"[bold #dfc38a]ÁREA COMIDAS, RAPPI & YAPE PROMOS PERÚ[/bold #dfc38a]{cat_title}{loc_title}\n"
        f"[dim #cbd5e1]Carta completa y promociones verificadas ordenadas estrictamente de menor a mayor precio[/dim #cbd5e1]",
        border_style="#8c734b"
    ))

    if not results:
        console.print("[red]No se encontraron productos o promociones para los filtros seleccionados.[/red]\n")
        return

    table = Table(border_style="#334155", box=None)
    table.add_column("#", justify="right", style="dim #64748b", no_wrap=True)
    table.add_column("Precio (PEN)", justify="right", style="bold #dfc38a", no_wrap=True)
    table.add_column("Dscto / Tipo", justify="center", style="#dfc38a", no_wrap=True)
    table.add_column("Canal / App", style="#cbd5e1", no_wrap=True)
    table.add_column("Marca", style="bold #f8fafc", no_wrap=True)
    table.add_column("Combo / Plato", style="#f8fafc")
    table.add_column("Localidad", style="dim #94a3b8")
    table.add_column("Cupón / Tiempo", justify="center", style="bold #dfc38a", no_wrap=True)

    for i, item in enumerate(results, 1):
        price_str = f"S/ {item['price']:,.2f}"
        if item.get("discount_percent"):
            discount_str = f"-{item['discount_percent']}%"
        else:
            discount_str = "[dim #94a3b8]Carta[/dim #94a3b8]"

        if item.get("coupon_code"):
            info_str = f"[bold #dfc38a]{item['coupon_code']}[/bold #dfc38a]"
        else:
            info_str = f"[dim #94a3b8]{item.get('delivery_time', '-')}[/dim #94a3b8]"

        is_yape = "Yape" in item["platform"]
        is_rappi = "Rappi" in item["platform"]

        if is_rappi:
            plat_styled = f"[bold #ff441f]{item['platform']}[/bold #ff441f]"
        elif is_yape:
            plat_styled = f"[bold #a855f7]{item['platform']}[/bold #a855f7]"
        else:
            plat_styled = f"[#cbd5e1]{item['platform']}[/#cbd5e1]"

        short_loc = item.get("location", "Nacional").split("(")[0].strip()

        if i == 1:
            table.add_row(
                f"[bold #dfc38a]1 (Más Bajo)[/bold #dfc38a]",
                f"[bold #dfc38a]{price_str}[/bold #dfc38a]",
                f"[bold #dfc38a]{discount_str}[/bold #dfc38a]",
                plat_styled,
                f"[bold #f8fafc]{item['brand']}[/bold #f8fafc]",
                f"[bold #f8fafc]{item['title']}[/bold #f8fafc]",
                short_loc,
                info_str
            )
        else:
            table.add_row(
                str(i),
                price_str,
                discount_str,
                plat_styled,
                item["brand"],
                item["title"],
                short_loc,
                info_str
            )

    console.print(table)
    console.print(
        f"\n[dim #64748b]Total: {stats['total_results']} opciones listadas. "
        f"Menor: S/ {stats['lowest_price']:,.2f}  •  Promedio: S/ {stats['average_price']:,.2f}  •  Mayor: S/ {stats['highest_price']:,.2f}[/dim #64748b]\n"
    )

def show_events_cli():
    events = get_events()
    now = datetime.now().astimezone()

    console.print()
    console.print(Panel.fit(
        f"[bold #dfc38a]CALENDARIO DE OFERTAS & BLACK FRIDAY PERÚ[/bold #dfc38a]\n"
        f"[dim #cbd5e1]Fechas oficiales de liquidaciones y temporadas de descuentos en celulares[/dim #cbd5e1]",
        border_style="#8c734b"
    ))

    table = Table(border_style="#334155", box=None)
    table.add_column("Evento", style="bold #f8fafc")
    table.add_column("Fechas Oficiales", style="#dfc38a")
    table.add_column("Cuenta Regresiva", style="bold #cbd5e1")
    table.add_column("Descuento Est.", justify="center", style="#dfc38a")
    table.add_column("Tiendas Principales", style="dim #94a3b8")

    for evt in events:
        start = datetime.fromisoformat(evt["start_date"])
        diff = start - now
        if diff.total_seconds() <= 0:
            countdown = "[bold green]¡En curso hoy![/bold green]"
        else:
            days = diff.days
            hours = int((diff.seconds) / 3600)
            countdown = f"[bold #dfc38a]Faltan {days}d {hours}h[/bold #dfc38a]"

        stores_str = ", ".join(evt["stores"][:4])
        if len(evt["stores"]) > 4:
            stores_str += f" (+{len(evt['stores']) - 4} más)"

        table.add_row(
            f"{evt['name']}\n[dim #64748b]{evt['badge']}[/dim #64748b]",
            evt["display_date"],
            countdown,
            evt["discount_estimate"],
            stores_str
        )

    console.print(table)
    console.print("\n[dim #64748b]Tip: Para Black Friday y Cyber Wow, los mayores descuentos se lanzan a las 00:00 del primer día.[/dim #64748b]\n")

async def run_cli():
    parser = argparse.ArgumentParser(
        description="BuscaProductos CLI - Comparador de precios de tecnología, canasta básica y comidas en Perú"
    )
    parser.add_argument("query", nargs="?", default=None, type=str, help="Producto a buscar (ej: 'iPhone 15', 'Laptop Lenovo', 'Smart TV 55', 'PS5', 'S24 FE')")
    parser.add_argument("--groceries", nargs="?", const="todas", default=None, help="Ver canasta básica y supermercados (Metro, PlazaVea, Tottus, Cajamarca)")
    parser.add_argument("--food", nargs="?", const="todas", default=None, help="Ver comidas, Rappi y Yape Promos (ej: --food, --food pizza, --food burger)")
    parser.add_argument("--location", type=str, default=None, help="Localidad o distrito (ej: cajamarca, miraflores, surco, arequipa)")
    parser.add_argument("--cajamarca", action="store_true", help="Filtrar solo tiendas con retiro gratis en Cajamarca (El Quinde / Real Plaza)")
    parser.add_argument("--payment", choices=["all", "any_card", "store_cards"], default=None, help="Filtro de medio de pago ('any_card' o 'store_cards')")
    parser.add_argument("--only-discounts", action="store_true", help="Mostrar solo ofertas con descuento en comidas")
    parser.add_argument("--events", action="store_true", help="Mostrar calendario de Black Friday, Cyber Wow y fechas de ofertas")
    parser.add_argument("--limit", type=int, default=20, help="Límite de resultados a mostrar (default: 20)")
    parser.add_argument("--no-refurbished", action="store_true", help="Excluir productos reacondicionados")
    parser.add_argument("--stores", type=str, default=None, help="Tiendas separadas por comas")
    parser.add_argument("--order", choices=["asc", "desc", "discount"], default="asc", help="Orden de precios (default: asc = menor a mayor)")

    args = parser.parse_args()

    if args.groceries is not None:
        show_groceries_cli(category=args.groceries, query=args.query)
        return

    if args.food is not None:
        show_food_cli(category=args.food, query=args.query, location=args.location, only_discounts=args.only_discounts, sort_by=args.order)
        return

    if args.events:
        show_events_cli()
        return

    if not args.query:
        show_events_cli()
        console.print("[dim #64748b]Para buscar productos: [white]python cli.py 'producto'[/white] (ej: python cli.py 'S24 FE', 'Laptop Lenovo', 'Smart TV 55')[/dim #64748b]")
        console.print("[dim #64748b]Para filtrar por retiro en Cajamarca: [white]python cli.py 'S24 FE' --cajamarca[/white][/dim #64748b]")
        console.print("[dim #64748b]Para ver canasta básica supermercados: [white]python cli.py --groceries[/white][/dim #64748b]")
        console.print("[dim #64748b]Para ver comidas & Rappi: [white]python cli.py --food[/white] o [white]python cli.py --food pizza --location cajamarca[/white][/dim #64748b]\n")
        return

    selected_stores = [s.strip().lower() for s in args.stores.split(",")] if args.stores else None

    console.print()
    cajamarca_tag = "  [bold #10b981]• Retiro en Cajamarca[/bold #10b981]" if args.cajamarca else ""
    console.print(Panel.fit(
        f"[bold #dfc38a]BUSCAPRODUCTOS[/bold #dfc38a] [dim #94a3b8]| Comparador de Precios Perú[/dim #94a3b8]\n"
        f"[dim #64748b]Búsqueda:[/dim #64748b] [bold #f8fafc]{args.query}[/bold #f8fafc]  [dim #64748b]•[/dim #64748b]  [dim #64748b]Orden:[/dim #64748b] [#dfc38a]Menor a mayor[/]{cajamarca_tag}",
        border_style="#8c734b"
    ))

    mgr = SearchManager()

    with Progress(
        SpinnerColumn(style="#dfc38a"),
        TextColumn("[dim #cbd5e1]{task.description}[/dim #cbd5e1]"),
        transient=True,
    ) as progress:
        task = progress.add_task(description="Consultando 12 tiendas en paralelo...", total=None)
        
        data = await mgr.search_all(
            query=args.query,
            stores=selected_stores,
            hide_accessories=True,
            include_refurbished=not args.no_refurbished,
            sort_by=args.order,
            payment_filter=args.payment,
            pickup_cajamarca_only=args.cajamarca,
            location=args.location or ("cajamarca" if args.cajamarca else "todas"),
            only_discounts=args.only_discounts
        )

    results = data.get("results", [])
    stats = data.get("stats", {})

    if not results:
        console.print(f"[red]No se encontraron resultados para '{args.query}'.[/red]\n")
        return

    # Best Deal
    cheapest = stats.get("cheapest_item")
    console.print(f"[bold #dfc38a]MEJOR PRECIO:[/bold #dfc38a] [bold #f8fafc]{cheapest['title']}[/bold #f8fafc]")
    console.print(f"  [bold #dfc38a]S/ {cheapest['price']:,.2f}[/bold #dfc38a] en [#cbd5e1]{cheapest['store']}[/#cbd5e1] ([dim]{cheapest['condition']}[/dim])  •  [#a855f7]{cheapest['payment_method']}[/#a855f7]")
    console.print(f"  [#10b981]{cheapest['pickup_location']}[/#10b981]")
    console.print(f"  [dim #64748b]{cheapest['url']}[/dim #64748b]\n")

    # Table
    table = Table(title=f"Resultados para '{args.query}'", border_style="#334155", box=None)
    table.add_column("#", justify="right", style="dim #64748b", no_wrap=True)
    table.add_column("Precio (PEN)", justify="right", style="bold #dfc38a", no_wrap=True)
    table.add_column("Tienda", style="#cbd5e1", no_wrap=True)
    table.add_column("Radar", style="bold #f59e0b", no_wrap=True)
    table.add_column("Medio de Pago", style="dim #cbd5e1", no_wrap=True)
    table.add_column("Retiro / Logística", style="#10b981", no_wrap=True)
    table.add_column("Modelo / Título", style="#f8fafc")
    table.add_column("Cuotas 12x", justify="right", style="dim #dfc38a", no_wrap=True)

    for i, item in enumerate(results[:args.limit], 1):
        price_str = f"S/ {item['price']:,.2f}"
        verdict = "🔥 Mínimo" if item.get("deal_verdict") == "Mínimo Histórico" else ("✅ Buen Precio" if item.get("deal_verdict") == "Buen Precio" else "-")
        pay_method = item.get("card_name") or "Cualquier Tarjeta"
        pickup_loc = item.get("pickup_location", "Envío").split("(")[0].strip()
        cuotas = f"S/ {item['installments_12x']:,.2f}" if item.get("installments_12x") else "-"

        if i == 1:
            table.add_row(
                f"[bold #dfc38a]1[/bold #dfc38a]",
                f"[bold #dfc38a]{price_str}[/bold #dfc38a]",
                f"[bold #f8fafc]{item['store']}[/bold #f8fafc]",
                verdict,
                pay_method,
                pickup_loc,
                f"[bold #f8fafc]{item['title']}[/bold #f8fafc]",
                cuotas
            )
        else:
            table.add_row(
                str(i),
                price_str,
                item['store'],
                verdict,
                pay_method,
                pickup_loc,
                item['title'],
                cuotas
            )

    console.print(table)
    console.print(
        f"\n[dim #64748b]{min(len(results), args.limit)} de {stats['total_results']} ofertas. "
        f"Promedio: S/ {stats['average_price']:,.2f}  •  Rango: S/ {stats['lowest_price']:,.2f} - S/ {stats['highest_price']:,.2f}[/dim #64748b]\n"
    )

if __name__ == "__main__":
    asyncio.run(run_cli())
