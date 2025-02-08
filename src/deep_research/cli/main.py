import argparse
from rich import print as rprint
from deep_research.core.research import Research

def main():
    parser = argparse.ArgumentParser(
        description="Deep Research CLI - A tool for conducting deep research",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=\
"""
Examples:
  # Create a new research with a topic
  python main.py --topic "Impact of AI on healthcare in 2024"
  
  # Load and continue an existing research
  python main.py --research-id RS_20240214_123456
  
  # Create a new research and specify model
  python main.py --topic "Future of quantum computing" --model "deepseek/deepseek-r1"
"""
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--topic', '-t', help='Research topic in any language')
    group.add_argument('--research-id', '-r', help='ID of existing research to load')
    parser.add_argument('--model', '-m', default='deepseek/deepseek-r1',
                      help='Model to use for report generation (default: deepseek/deepseek-r1)')

    args = parser.parse_args()

    try:
        if args.topic:
            research = Research(topic=args.topic)
            rprint(f"[bold green]Created new research[/] with ID: {research.id}")
        else:
            research = Research(research_id=args.research_id)
            rprint(f"[bold green]Loaded existing research[/] with ID: {research.id}")

        # Step 1: Execute search
        rprint("\n[bold blue]Step 1:[/] Executing search...")
        research.execute_search()

        # Step 2: Generate category reports
        rprint("\n[bold blue]Step 2:[/] Generating category reports...")
        research.generate_all_category_reports()

        # Step 3: Generate category links
        rprint("\n[bold blue]Step 3:[/] Generating reference links...")
        research.generate_all_category_links()

        # Step 4: Generate final report
        rprint(f"\n[bold blue]Step 4:[/] Generating final research report using model {args.model}...")
        research.generate_research_report(model=args.model)

        rprint("\n[bold green]Research completed successfully![/]")
        rprint(f"[bold]Output files can be found in:[/] output/{research.id}/")

    except Exception as e:
        rprint(f"[bold red]Error:[/] {str(e)}")
        parser.print_help()
        exit(1)

if __name__ == "__main__":
    main()