#!/usr/bin/env python3
import asyncio
import argparse
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from scrapers.manager import SearchManager

console = Console()

async def run_cli():
    parser = argparse.ArgumentParser(
        description="BuscaFono CLI - Comparador de precios de celulares en Perú"
    )
    parser.add_argument("query", type=str, help="Modelo de celular a buscar (ej: 'iPhone 13', 'Samsung S24')")
    parser.add_argument("--limit", type=int, default=20, help="Límite de resultados a mostrar (default: 20)")
    parser.add_argument("--no-refurbished", action="store_true", help="Excluir celulares reacondicionados")
    parser.add_argument("--stores", type=str, default=None, help="Tiendas separadas por comas (falabella,ripley,plazavea,claro,coolbox,lacuracao,efe,hiraoka,oechsle,promart,shopstar)")
    parser.add_argument("--order", choices=["asc", "desc", "discount"], default="asc", help="Orden de precios (default: asc = menor a mayor)")

    args = parser.parse_args()
    selected_stores = [s.strip().lower() for s in args.stores.split(",")] if args.stores else None

    console.print()
    console.print(Panel.fit(
        f"[bold white]BuscaFono[/bold white] [dim]| Comparador de Precios[/dim]\n"
        f"[dim]Búsqueda:[/dim] [white]{args.query}[/white]  [dim]•[/dim]  [dim]Orden:[/dim] [green]Menor a mayor[/green]",
        border_style="dim"
    ))

    mgr = SearchManager()

    with Progress(
        SpinnerColumn(style="dim white"),
        TextColumn("[dim]{task.description}[/dim]"),
        transient=True,
    ) as progress:
        task = progress.add_task(description="Consultando tiendas en paralelo...", total=None)
        
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
    console.print(f"[dim]PRECIO MÁS BAJO:[/dim] [bold white]{cheapest['title']}[/bold white]")
    console.print(f"  [bold green]S/ {cheapest['price']:,.2f}[/bold green] en [cyan]{cheapest['store']}[/cyan] ({cheapest['condition']})")
    console.print(f"  [dim]{cheapest['url']}[/dim]\n")

    # Table
    table = Table(title=f"Resultados para '{args.query}'", border_style="dim", box=None)
    table.add_column("#", justify="right", style="dim", no_wrap=True)
    table.add_column("Precio (PEN)", justify="right", style="bold white")
    table.add_column("Tienda", style="cyan")
    table.add_column("Condición", style="dim")
    table.add_column("Modelo / Título", style="white")
    table.add_column("Descuento", justify="center", style="dim")

    for i, item in enumerate(results[:args.limit], 1):
        price_str = f"S/ {item['price']:,.2f}"
        discount_str = f"-{item['discount_percent']}%" if item.get("discount_percent") else "-"
        cond_str = "Nuevo" if item["condition"] == "Nuevo" else "Reacondicionado"
        
        if i == 1:
            table.add_row(
                f"[green]{i}[/green]",
                f"[bold green]{price_str}[/bold green]",
                f"[bold cyan]{item['store']}[/bold cyan]",
                cond_str,
                f"[bold white]{item['title'][:55]}[/bold white]",
                discount_str
            )
        else:
            table.add_row(
                str(i),
                price_str,
                item['store'],
                cond_str,
                item['title'][:55],
                discount_str
            )

    console.print(table)
    console.print(
        f"\n[dim]{min(len(results), args.limit)} de {stats['total_results']} opciones. "
        f"Promedio: S/ {stats['average_price']:,.2f}  •  Rango: S/ {stats['lowest_price']:,.2f} - S/ {stats['highest_price']:,.2f}[/dim]\n"
    )

if __name__ == "__main__":
    asyncio.run(run_cli())
