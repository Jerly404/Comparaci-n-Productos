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

console = Console()

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
        description="BuscaFono CLI - Comparador de precios de celulares y calendario de ofertas en Perú"
    )
    parser.add_argument("query", nargs="?", default=None, type=str, help="Modelo de celular a buscar (ej: 'iPhone 13', 'Samsung S24')")
    parser.add_argument("--events", action="store_true", help="Mostrar calendario de Black Friday, Cyber Wow y fechas de ofertas")
    parser.add_argument("--limit", type=int, default=20, help="Límite de resultados a mostrar (default: 20)")
    parser.add_argument("--no-refurbished", action="store_true", help="Excluir celulares reacondicionados")
    parser.add_argument("--stores", type=str, default=None, help="Tiendas separadas por comas")
    parser.add_argument("--order", choices=["asc", "desc", "discount"], default="asc", help="Orden de precios (default: asc = menor a mayor)")

    args = parser.parse_args()

    if args.events or not args.query:
        show_events_cli()
        if not args.query:
            console.print("[dim #64748b]Para buscar celulares: [white]python cli.py 'modelo'[/white] (ej: python cli.py 'iPhone 13')[/dim #64748b]\n")
            return

    selected_stores = [s.strip().lower() for s in args.stores.split(",")] if args.stores else None

    console.print()
    console.print(Panel.fit(
        f"[bold #dfc38a]BUSCAFONO[/bold #dfc38a] [dim #94a3b8]| Comparador de Precios[/dim #94a3b8]\n"
        f"[dim #64748b]Búsqueda:[/dim #64748b] [bold #f8fafc]{args.query}[/bold #f8fafc]  [dim #64748b]•[/dim #64748b]  [dim #64748b]Orden:[/dim #64748b] [#dfc38a]Menor a mayor[/] [dim #64748b](12 tiendas)[/dim #64748b]",
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
            sort_by=args.order
        )

    results = data.get("results", [])
    stats = data.get("stats", {})

    if not results:
        console.print(f"[red]No se encontraron resultados para '{args.query}'.[/red]\n")
        return

    # Best Deal
    cheapest = stats.get("cheapest_item")
    console.print(f"[bold #dfc38a]MEJOR PRECIO:[/bold #dfc38a] [bold #f8fafc]{cheapest['title']}[/bold #f8fafc]")
    console.print(f"  [bold #dfc38a]S/ {cheapest['price']:,.2f}[/bold #dfc38a] en [#cbd5e1]{cheapest['store']}[/#cbd5e1] ([dim]{cheapest['condition']}[/dim])")
    console.print(f"  [dim #64748b]{cheapest['url']}[/dim #64748b]\n")

    # Table
    table = Table(title=f"Resultados para '{args.query}'", border_style="#334155", box=None)
    table.add_column("#", justify="right", style="dim #64748b", no_wrap=True)
    table.add_column("Precio (PEN)", justify="right", style="bold #dfc38a", no_wrap=True)
    table.add_column("Tienda", style="#cbd5e1", no_wrap=True)
    table.add_column("Condición", style="dim #94a3b8", no_wrap=True)
    table.add_column("Modelo / Título", style="#f8fafc")
    table.add_column("Descuento", justify="center", style="#c5a880", no_wrap=True)

    for i, item in enumerate(results[:args.limit], 1):
        price_str = f"S/ {item['price']:,.2f}"
        discount_str = f"-{item['discount_percent']}%" if item.get("discount_percent") else "-"
        cond_str = "Nuevo" if item["condition"] == "Nuevo" else "Reacondicionado"
        
        if i == 1:
            table.add_row(
                f"[bold #dfc38a]{i}[/bold #dfc38a]",
                f"[bold #dfc38a]{price_str}[/bold #dfc38a]",
                f"[bold #f8fafc]{item['store']}[/bold #f8fafc]",
                cond_str,
                f"[bold #f8fafc]{item['title']}[/bold #f8fafc]",
                discount_str
            )
        else:
            table.add_row(
                str(i),
                price_str,
                item['store'],
                cond_str,
                item['title'],
                discount_str
            )

    console.print(table)
    console.print(
        f"\n[dim #64748b]{min(len(results), args.limit)} de {stats['total_results']} ofertas. "
        f"Promedio: S/ {stats['average_price']:,.2f}  •  Rango: S/ {stats['lowest_price']:,.2f} - S/ {stats['highest_price']:,.2f}[/dim #64748b]\n"
    )

if __name__ == "__main__":
    asyncio.run(run_cli())
