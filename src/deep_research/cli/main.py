import argparse
from deep_research.core.research import Research
from deep_research.core.report import Report
from deep_research.utils.log_util import LogUtil
from dotenv import load_dotenv
import traceback

# Load environment variables
load_dotenv()

def main():
    logger = LogUtil().logger
    logger.info("Starting Deep Research CLI")
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
"""
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--topic', '-t', help='Research topic in any language')
    group.add_argument('--research-id', '-r', help='ID of existing research to load')
    parser.add_argument('--report-method', '-p', default='generate_research_report_detailed',
                      choices=['generate_research_report', 'generate_research_report_detailed', 'generate_wechat_article'],
                      help='Report generation method to use (default: generate_research_report)')

    args = parser.parse_args()

    try:
        if args.topic:
            logger.info(f"Creating new research with topic: {args.topic}")
            research = Research(topic=args.topic)
            logger.info(f"Created new research with ID: {research.id}")
            logger.info("Starting research execution")
            research.execute()
            logger.info(f"Completed research execution. All data saved to output directory [/output/{research.id}]")
        else:
            logger.info(f"Loading existing research with ID: {args.research_id}")
            research = Research(research_id=args.research_id)
            logger.info(f"Loaded existing research with ID: {research.id}")
            
            # Create report instance and generate report
            logger.info(f"Generating report using method: {args.report_method}")
            report = Report(research.id)
            report_method = getattr(report, args.report_method)
            report_content = report_method()
            logger.info(f"Successfully generated report using {args.report_method}")

    except Exception as e:
        logger.error(f"Error during research execution: {str(e)}")
        logger.error("Full error stack trace:")
        logger.error(traceback.format_exc())
        exit(1)

if __name__ == "__main__":
    main()