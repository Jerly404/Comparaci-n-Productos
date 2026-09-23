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
        description="BuscaFono CLI - Comparador de precios de celulares en Perú (de menor a mayor precio)"
    )
    parser.add_argument("query", type=str, help="Modelo de celular a buscar (ej: 'iPhone 13', 'Samsung S24')")
    parser.add_argument("--limit", type=int, default=20, help="Límite de resultados a mostrar (default: 20)")
    parser.add_argument("--no-refurbished", action="store_true", help="Excluir celulares reacondicionados")
    parser.add_argument("--stores", type=str, default=None, help="Tiendas separadas por comas (falabella,ripley,plazavea,coolbox,oechsle,promart,hiraoka)")
    parser.add_argument("--order", choices=["asc", "desc", "discount"], default="asc", help="Orden de precios (default: asc = menor a mayor)")

    args = parser.parse_args()
    selected_stores = [s.strip().lower() for s in args.stores.split(",")] if args.stores else None

    console.print()
    console.print(Panel.fit(
        f"[bold cyan]🔍 Comparador de Precios de Celulares Perú[/bold cyan]\n"
        f"[dim]Buscando:[/dim] [bold white]{args.query}[/bold white] | [dim]Orden:[/dim] [green]Menor a Mayor Precio[/green]",
        border_style="cyan"
    ))

    mgr = SearchManager()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(description="[yellow]Consultando tiendas (Falabella, Ripley, PlazaVea, Coolbox, Hiraoka...)...[/yellow]", total=None)
        
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
        console.print(f"[bold red]❌ No se encontraron teléfonos para '{args.query}'.[/bold red]")
        return

    # Stats banner
    cheapest = stats.get("cheapest_item")
    console.print(f"[bold green]✨ Mejor Oferta Encontrada:[/bold green] [bold white]{cheapest['title']}[/bold white]")
    console.print(f"   [bold yellow]S/ {cheapest['price']:,.2f}[/bold yellow] en [bold magenta]{cheapest['store']}[/bold magenta] ({cheapest['condition']})")
    console.print(f"   [dim]Enlace:[/dim] [underline blue]{cheapest['url']}[/underline blue]")
    console.print()

    # Results Table
    table = Table(title=f"Resultados para '{args.query}' (Ordenados de menor a mayor precio)", border_style="dim")
    table.add_column("#", justify="right", style="cyan", no_wrap=True)
    table.add_column("Precio (PEN)", justify="right", style="bold green")
    table.add_column("Tienda", style="magenta")
    table.add_column("Condición", style="yellow")
    table.add_column("Modelo / Título", style="white")
    table.add_column("Descuento", justify="center", style="red")

    for i, item in enumerate(results[:args.limit], 1):
        price_str = f"S/ {item['price']:,.2f}"
        discount_str = f"-{item['discount_percent']}%" if item.get("discount_percent") else "-"
        cond_style = "[green]Nuevo[/green]" if item["condition"] == "Nuevo" else "[yellow]Reacondicionado[/yellow]"
        
        # Highlight top 1
        if i == 1:
            table.add_row(
                f"[bold gold1]🥇 {i}[/bold gold1]",
                f"[bold gold1]{price_str}[/bold gold1]",
                f"[bold]{item['store']}[/bold]",
                cond_style,
                f"[bold]{item['title'][:55]}[/bold]",
                discount_str
            )
        else:
            table.add_row(
                str(i),
                price_str,
                item['store'],
                cond_style,
                item['title'][:55],
                discount_str
            )

    console.print(table)
    console.print(
        f"[dim]Mostrando {min(len(results), args.limit)} de {stats['total_results']} ofertas. "
        f"Promedio: S/ {stats['average_price']:,.2f} | Rango: S/ {stats['lowest_price']:,.2f} - S/ {stats['highest_price']:,.2f}[/dim]\n"
    )

if __name__ == "__main__":
    asyncio.run(run_cli())
