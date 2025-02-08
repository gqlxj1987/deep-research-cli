import click
from rich import print as rprint
from deep_research.core.research import Research


@click.group()
def main():
    """Deep Research CLI - A tool for conducting deep research"""
    pass

@main.command()
@click.argument('query')
def search(query):
    """Search for research papers based on a query"""
    rprint(f"[bold green]Searching for:[/] {query}")

if __name__ == "__main__":
    research = Research(topic="Redis 选择单线程执行命令规避了多线程并发模型的一些缺点，而 Dragonfly 和 Tair 选择了多线程设计，他们是如何解决这些问题的？")
    #research = Research(research_id="RS_20250207_220622")
    print(f"Created research with ID: {research.id}")

    # Step. 01
    research.execute_search()

    # Step. 02
    research.generate_all_category_reports()

    # Step. 03
    research.generate_all_category_links()

    # Step. 04
    research.generate_research_report()