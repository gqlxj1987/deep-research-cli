import click
from rich import print as rprint

@click.group()
def main():
    """Deep Research CLI - A tool for conducting deep research"""
    pass

@main.command()
@click.argument('query')
def search(query):
    """Search for research papers based on a query"""
    rprint(f"[bold green]Searching for:[/] {query}")

if __name__ == '__main__':
    main()