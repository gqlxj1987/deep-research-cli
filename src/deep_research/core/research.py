"""Module for handling research operations"""

from datetime import datetime
from typing import List, Dict, Any
from deep_research.utils.research_helper import translate_to_english, generate_research_content, generate_research_plan
from deep_research.core.config import Config

class Research:
    """Class for managing research operations"""

    def __init__(self, topic: str = None, research_id: str = None):
        """Initialize a new research instance

        Args:
            topic: The research topic in any language (optional if research_id is provided)
            research_id: Existing research ID to load data from (optional)
        """
        if topic and research_id:
            raise ValueError("Cannot provide both topic and research_id")
        elif not topic and not research_id:
            raise ValueError("Must provide either topic or research_id")

        if topic:
            self._init_from_topic(topic)
        else:
            self._init_from_id(research_id)

    def _init_from_topic(self, topic: str):
        """Initialize research instance with a new topic

        Args:
            topic: The research topic in any language
        """
        self.topic = topic
        self.research_id = 'RS_' + datetime.now().strftime("%Y%m%d_%H%M%S")
        self.english_topic = self._translate_topic()
        self.research_content = None
        self.research_plan = None

        self.create_research_detail(self.english_topic)

    def _init_from_id(self, research_id: str):
        """Initialize research instance from existing research ID

        Args:
            research_id: The ID of an existing research to load
        """
        from deep_research.services.persistence_service import PersistenceClient

        persistence_client = PersistenceClient()
        file_path = f'output/{research_id}/{research_id}_meta.json'
        
        try:
            data = persistence_client.load_json(file_path)
            print(data)
            self.topic = data['topic']
            self.research_id = data['research_id']
            self.english_topic = data['english_topic']
            self.research_content = data['research_content']
            self.research_plan = data['research_plan']
        except Exception as e:
            raise ValueError(f"Failed to load research data for ID {research_id}: {str(e)}")

    def _translate_topic(self) -> str:
        """Translate the research topic to English

        Returns:
            The translated topic in English
        """
        translated_topic = translate_to_english(self.topic)

        return translated_topic

    def create_research_detail(self, english_topic):
        """Generate research content based on the topic

        Returns:
            A dictionary containing the research content
        """
        json_content = generate_research_content(english_topic)
        self.research_content = json_content

        json_plan = generate_research_plan(json_content)
        self.research_plan = json_plan['research_plan']

        self.save()

    def save(self) -> None:
        """Save research metadata to a JSON file in the output directory

        Creates a new folder with the research ID and saves metadata as JSON.
        The directory will be created automatically if it doesn't exist.
        """
        from deep_research.services.persistence_service import PersistenceClient

        # Prepare metadata
        metadata = {
            'topic': self.topic,
            'research_id': self.research_id,
            'english_topic': self.english_topic,
            'research_content': self.research_content,
            'research_plan': self.research_plan
        }

        # Save metadata using PersistenceClient
        persistence_client = PersistenceClient()
        persistence_client.save_research_metadata(self.research_id, metadata)

    

    @property
    def id(self) -> str:
        """Get the research's unique ID

        Returns:
            The research's unique ID string
        """
        return self.research_id

    def _sanitize_filename(self, name: str) -> str:
        """Sanitize a string to be used as a filename

        Args:
            name: The string to sanitize

        Returns:
            A sanitized string safe for use as a filename
        """
        import re
        # Remove special characters and replace spaces with underscores
        sanitized = re.sub(r'[^\w\s-]', '', name)
        sanitized = re.sub(r'[-\s]+', '_', sanitized)
        return sanitized

    def execute_search(self) -> None:
        """Execute searches for all queries in the research plan

        Iterates through the research plan, performs advanced searches for each query,
        and saves results in category-specific directories.
        """
        from deep_research.utils.research_helper import search_advanced
        from deep_research.services.persistence_service import PersistenceClient

        persistence_client = PersistenceClient()

        if not self.research_plan:
            raise ValueError("No research plan available")

        print(f'research plan: {self.research_plan}')
        for category_data in self.research_plan:
            category = category_data.get('category')
            if not category:
                continue
            
            for query in category_data.get('queries_list', []):
                if not query:
                    continue

                # Perform advanced search
                search_results = search_advanced(query)

                # Save search results using persistence service
                persistence_client.save_search_results(self.research_id, category, query, search_results)

    def get_category_results(self, category: str) -> List[Dict[str, str]]:
        """Retrieve and process search results from a specific category

        Args:
            category: The category name to process

        Returns:
            A list of dictionaries containing title and content for each result
        """
        from deep_research.services.persistence_service import PersistenceClient

        persistence_client = PersistenceClient()
        return persistence_client.load_category_results(self.research_id, category)

    def get_category_reports(self) -> List[Dict[str, str]]:
        """Retrieve and process search results from a specific category

        Args:
            category: The category name to process

        Returns:
            A list of dictionaries containing title and content for each result
        """
        from deep_research.services.persistence_service import PersistenceClient

        persistence_client = PersistenceClient()
        return persistence_client.load_category_reports(self.research_id)

    

    def generate_category_report(self, category: str) -> Dict[str, Any]:
        """Generate and save a research report for a specific category

        Args:
            category: The category name to generate report for

        Returns:
            A dictionary containing the generated report
        """
        from deep_research.utils.research_helper import generate_research_category_report

        # Get category results
        category_results = self.get_category_results(category)

        # Generate report
        report = generate_research_category_report(
            research_content=self.research_content,
            category=category,
            category_resrouces=category_results
        )

        report_json = {
            "category": category,
            "report": report
        }
        # Sanitize category name for file path
        sanitized_category = self._sanitize_filename(category)
        file_path = f'output/{self.research_id}/{sanitized_category}_report.json'

        # Save report
        from deep_research.services.persistence_service import PersistenceClient
        persistence_client = PersistenceClient()
        persistence_client.save_json(report_json, file_path)

        return report_json

    def generate_all_category_links(self) -> List[str]:
        """Generate links for all categories in the research plan
        Iterates through each category in the research plan and generates a link for each one.
        Returns:
            A list of strings containing the generated links for each category
        """
        if not self.research_plan:
            raise ValueError("No research plan available")
        links = []
        for category_data in self.research_plan:
            category = category_data.get('category')
            if not category:
                continue
            try:
                # Get category results
                category_results = self.get_category_results(category)
                for result in category_results:
                    title = result['title']
                    url = result['url']
                    link = f"[{title}]({url})"
                    links.append(link)
            except Exception as e:
                print(f"Error generating link for category {category}: {str(e)}")
                continue
        reference_content = "## Reference\n\n"
        reference_content += '\n'.join(f'- {item}' for item in links)
        file_path = f'output/{self.research_id}/{self.research_id}_reference.md'

            # Save report
        from deep_research.services.persistence_service import PersistenceClient
        persistence_client = PersistenceClient()
        persistence_client.save_file(file_path, reference_content)

        return links


    def generate_all_category_reports(self) -> List[Dict[str, Any]]:
        """Generate reports for all categories in the research plan

        Iterates through each category in the research plan and generates a report for each one.

        Returns:
            A list of dictionaries containing the generated reports for each category
        """
        if not self.research_plan:
            raise ValueError("No research plan available")

        reports = []
        for category_data in self.research_plan:
            category = category_data.get('category')
            if not category:
                continue

            try:
                report = self.generate_category_report(category)
                reports.append(report)
            except Exception as e:
                print(f"Error generating report for category {category}: {str(e)}")
                continue

        return reports

    def generate_research_report(self, model=Config.REPORT_MODEL) -> Dict[str, Any]:
            """Generate final research report
            """
            if not self.research_plan:
                raise ValueError("No research plan available")

            reports = self.get_category_reports()

            from deep_research.utils.research_helper import generate_research_final_report

            # Get category results
            report_content = generate_research_final_report(research_content=self.research_content, reports=reports, model=model)
            
            model_name = self._sanitize_filename(model)
            file_path = f'output/{self.research_id}/{self.research_id}_{model_name}_research.md'

            # Save report
            from deep_research.services.persistence_service import PersistenceClient
            persistence_client = PersistenceClient()
            persistence_client.save_file(file_path, report_content)

            return report_content


if __name__ == "__main__":
    if False:
        research = Research(topic="中国信用卡消费市场最全面的数据分析报告，涵盖所有方面，罗列所有数据并整理，保留数据源形成极大篇幅的数据汇总。")
        #research = Research(research_id="RS_20250208_140344")
        print(f"Created research with ID: {research.id}")

        # Step. 01
        research.execute_search()

        # Step. 02
        research.generate_all_category_reports()

        # Step. 03
        research.generate_all_category_links()

        # Step. 04
        research.generate_research_report(model="deepseek/deepseek-r1")
    else:
        research = Research(research_id="RS_20250209_141723")
        # Step. 04
        # Step. 03
        #research.generate_all_category_links()
        research.generate_research_report(model="google/gemini-2.0-pro-exp-02-05:free")

    