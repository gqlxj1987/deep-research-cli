"""Module for handling research operations

This module provides the core functionality for managing research operations, including:
- Research initialization and metadata management
- Topic translation and research plan generation
- Search execution and result management
- Report generation and link compilation

The Research class serves as the main entry point for conducting research tasks,
handling both new research topics and loading existing research data.
"""

from datetime import datetime
from typing import List, Dict, Any
from deep_research.utils.research_helper import ResearchHelper
from deep_research.core.config import Config
from deep_research.utils.log_util import LogUtil

class Research:
    """Class for managing research operations
    
    This class orchestrates the entire research process, from initialization to execution.
    It handles topic translation, research plan generation, search execution, and report
    generation. The class can either start a new research project from a topic or load
    an existing research project using its ID.
    """

    def __init__(self, topic: str = None, research_id: str = None):
        """Initialize a new research instance

        Args:
            topic: The research topic in any language (optional if research_id is provided)
            research_id: Existing research ID to load data from (optional)

        Raises:
            ValueError: If neither topic nor research_id is provided, or if both are provided
        """
        self._logger = LogUtil().logger
        self._logger.info(f"Initializing Research instance with topic='{topic}', research_id='{research_id}')")

        if topic and research_id:
            error_msg = "Cannot provide both topic and research_id"
            self._logger.error(error_msg)
            raise ValueError(error_msg)
        elif not topic and not research_id:
            error_msg = "Must provide either topic or research_id"
            self._logger.error(error_msg)
            raise ValueError(error_msg)

        # Generate new research ID if not provided
        self.research_id = research_id or 'RS_' + datetime.now().strftime("%Y%m%d_%H%M%S")
        self._helper = ResearchHelper(self.research_id)
        self._logger.debug(f"Created research instance with ID: {self.research_id}")

        if topic:
            self._init_from_topic(topic)
        else:
            self._init_from_id()

    def _init_from_topic(self, topic: str):
        self._logger.info(f"Initializing new research from topic: {topic}")
        """Initialize research instance with a new topic

        Args:
            topic: The research topic in any language
        """
        self.topic = topic
        self.english_topic = self._translate_topic()
        self.research_content = None
        self.research_plan = None

        self.create_research_detail(self.english_topic)

    def _init_from_id(self):
        self._logger.info(f"Loading existing research from ID: {self.research_id}")
        """Initialize research instance from existing research ID"""
        try:
            data = self._helper.load_research_metadata()
            self.topic = data['topic']
            self.english_topic = data['english_topic']
            self.research_content = data['research_content']
            self.research_plan = data['research_plan']
        except Exception as e:
            error_msg = f"Failed to load research data for ID {self.research_id}: {str(e)}"
            self._logger.error(error_msg)
            raise ValueError(error_msg)

    def _translate_topic(self) -> str:
        self._logger.debug(f"Translating topic to English: {self.topic}")
        """Translate the research topic to English

        Returns:
            The translated topic in English
        """
        return self._helper.translate_to_english(self.topic)

    def create_research_detail(self, english_topic):
        self._logger.info(f"Generating research details for topic: {english_topic}")
        """Generate research content based on the topic

        Returns:
            A dictionary containing the research content
        """
        self.research_content = self._helper.generate_research_content(english_topic)
        json_plan = self._helper.generate_research_plan(self.research_content)
        self.research_plan = json_plan['research_plan']
        self.save()

    def save(self) -> None:
        self._logger.debug(f"Saving research metadata for ID: {self.research_id}")
        """Save research metadata to a JSON file in the output directory

        Creates a new folder with the research ID and saves metadata as JSON.
        The directory will be created automatically if it doesn't exist.
        """
        metadata = {
            'topic': self.topic,
            'research_id': self.research_id,
            'english_topic': self.english_topic,
            'research_content': self.research_content,
            'research_plan': self.research_plan
        }
        self._helper.save_research_metadata(metadata)

    @property
    def id(self) -> str:
        """Get the research's unique ID

        Returns:
            The research's unique ID string
        """
        return self.research_id

    def execute_search(self) -> None:
        self._logger.info("Starting search execution for all research categories")
        """Execute searches for all queries in the research plan

        Iterates through the research plan, performs advanced searches for each query,
        and saves results in category-specific directories.
        """
        if not self.research_plan:
            error_msg = "No research plan available"
            self._logger.error(error_msg)
            raise ValueError(error_msg)

        self._logger.debug(f'Research plan: {self.research_plan}')
        for category_data in self.research_plan:
            category = category_data.get('category')
            if not category:
                continue
            
            for query in category_data.get('queries_list', []):
                if not query:
                    continue

                search_results = self._helper.search_advanced(query)
                self._helper.save_search_results(category, query, search_results)

    def get_category_reports(self) -> List[Dict[str, str]]:
        self._logger.debug("Retrieving all category reports")
        """Retrieve and process search results from a specific category

        Returns:
            A list of dictionaries containing title and content for each result
        """
        return self._helper.read_category_reports()

    def generate_category_report(self, category: str):
        self._logger.info(f"Generating report for category: {category}")
        """Generate and save a research report for a specific category

        Args:
            category: The category name to generate report for

        Returns:
            A dictionary containing the generated report
        """
        category_results = self._helper.read_category_results(category)
        report = self._helper.generate_category_report(
            research_content=self.research_content,
            category=category,
            category_resources=category_results
        )
        self._helper.save_category_report(category, report)
        return report

    def generate_all_category_links(self) -> List[str]:
        self._logger.info("Generating reference links for all categories")
        """Generate links for all categories in the research plan
        Iterates through each category in the research plan and generates a link for each one.
        Returns:
            A list of strings containing the generated links for each category
        """
        if not self.research_plan:
            error_msg = "No research plan available"
            self._logger.error(error_msg)
            raise ValueError(error_msg)

        links = []
        for category_data in self.research_plan:
            category = category_data.get('category')
            if not category:
                continue

            try:
                category_results = self._helper.read_category_results(category)
                for result in category_results:
                    title = result['title']
                    url = result['url']
                    link = f"[{title}]({url})"
                    links.append(link)
            except Exception as e:
                self._logger.error(f"Error generating link for category {category}: {str(e)}")
                continue

        reference_content = "## Reference\n\n"
        reference_content += '\n'.join(f'- {item}' for item in links)
        file_path = f'output/{self.research_id}/{self.research_id}_reference.md'

        from deep_research.services.persistence_service import PersistenceClient
        persistence_client = PersistenceClient()
        persistence_client.save_file(file_path, reference_content)

        return links

    def generate_all_category_reports(self) -> List[Dict[str, Any]]:
        self._logger.info("Generating reports for all research categories")
        """Generate reports for all categories in the research plan

        Iterates through each category in the research plan and generates a report for each one.

        Returns:
            A list of dictionaries containing the generated reports for each category
        """
        if not self.research_plan:
            error_msg = "No research plan available"
            self._logger.error(error_msg)
            raise ValueError(error_msg)

        reports = []
        for category_data in self.research_plan:
            category = category_data.get('category')
            if not category:
                continue

            try:
                report = self.generate_category_report(category)
                reports.append(report)
            except Exception as e:
                self._logger.error(f"Error generating report for category {category}: {str(e)}")
                continue

        return reports

    def execute(self):
        self._logger.info(f"Starting complete research execution for ID: {self.research_id}")
        """Execute the research process
        This method orchestrates the entire research process, including search, report generation, and saving.
        """
        # Step 1: Execute searches
        self.execute_search()
        # Step 2: Generate reports
        self.generate_all_category_reports()
        # Step 3: Generate links
        self.generate_all_category_links()


if __name__ == "__main__":
    research = Research(research_id="RS_20250210_175342")


    