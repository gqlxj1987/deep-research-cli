
from typing import Dict, Any, List
import os
import glob
from deep_research.services.ai_service import LLMClient
from deep_research.services.search_service import SearchClient
from deep_research.services.persistence_service import PersistenceClient
from deep_research.core.config import Config
from deep_research.utils.log_util import LogUtil

class ResearchHelper:
    """Class for managing research helper operations
    
    This class provides utility methods for handling various research operations,
    including translation, content generation, search execution, and result management.
    It integrates with various services (LLM, Search, Persistence) to provide a
    comprehensive research assistance functionality.
    """

    def __init__(self, research_id: str = None):
        """Initialize a new research helper instance

        Args:
            research_id: The ID of the research to work with
        """
        self._logger = LogUtil().logger
        self._logger.info(f"Initializing ResearchHelper with research_id: {research_id}")
        self.research_id = research_id
        self._llm_client = LLMClient()
        self._search_client = SearchClient()
        self._persistence_client = PersistenceClient()

    def translate_to_english(self, text: str, **kwargs: Any) -> Dict[str, str]:
        """Translate any text to English using the LLM model

        Args:
            text: The text to translate to English
            **kwargs: Additional parameters to pass to the API

        Returns:
            The English translation as a string in a dictionary format
        """
        self._logger.debug(f"Translating text to English: {text}")
        messages = [
            {"role": "user", "content": f"""You are a professional translator. Translate the [{text}] to English. Only return translated text in Json format: {{response:""}}"""}
        ]
        try:
            result = self._llm_client.chat_completion(messages, **kwargs)['response']
            self._logger.info(f"Successfully translated text to English")
            return result
        except Exception as e:
            self._logger.error(f"Failed to translate text: {str(e)}")
            raise

    def generate_research_content(self, text: str, **kwargs: Any) -> Dict[str, str]:
        """Generate research content based on the topic

        Args:
            text: The research topic
            **kwargs: Additional parameters to pass to the API

        Returns:
            A dictionary containing the research content
        """
        self._logger.debug(f"Generating research content for topic: {text}")
        messages = [
            {"role": "user", "content": f'''You are a research expert, to provide comprehensive framework of searching keywords for user to search information for research purpose.

User will provide a topic or target for research.

You will think about the topic or target, deep dive in the core question and target, define the scope of the research and goal and meaning of the research to help set up a solid background content of the whole research.

return your result in JSON format:

```
{{
  original_topic: "",
  core_research_topic:"",
  research_scope:"",
  research_target:""
}}
```
Research Topic: [{text}]'''}
        ]
        try:
            result = self._llm_client.smart_completion(messages, **kwargs)
            self._logger.info("Successfully generated research content")
            return result
        except Exception as e:
            self._logger.error(f"Failed to generate research content: {str(e)}")
            raise

    def generate_research_plan(self, research_content: Dict[str, str], **kwargs: Any) -> Dict[str, str]:
        """Generate a research plan based on the research content

        Args:
            research_content: The research content to base the plan on
            **kwargs: Additional parameters to pass to the API

        Returns:
            A dictionary containing the research plan
        """
        self._logger.debug("Generating research plan")
        messages = [
            {"role": "user", "content": f'''You are a research planner, to provide comprehensive framework of searching keywords for user to search information for research purpose.

Based on below research information

- you will work out a comprehensive list of queries for user to collect informations on Search Engines cover everything aspect of the research goal.
- Query need to be specific to the research topic and category to narrow the results.

```
{research_content}
```
You will provide the research plan in below  in JSON format:

```
{{
  research_plan: [
    {{
      category: "",
      category_research_goal: "",
      queries_list: ["",""]
    }},
    {{
      category: "",
      category_research_goal: "",
      queries_list: ["",""]
    }}
  ]
}}
```

rethink until you think the plan is comprehensive for finding the answer or support the research. Adjust or append if you think still missing some. 
Provide output in pure JSON format.
'''}
        ]
        try:
            result = self._llm_client.smart_completion(messages, **kwargs)
            self._logger.info("Successfully generated research plan")
            return result
        except Exception as e:
            self._logger.error(f"Failed to generate research plan: {str(e)}")
            raise

    def save_research_metadata(self, metadata: Dict[str, Any]) -> None:
        """Save research metadata to a JSON file

        Args:
            metadata: The metadata to save
        """
        output_file = f'output/{self.research_id}/{self.research_id}_meta.json'
        self._logger.debug(f"Saving research metadata to {output_file}")
        try:
            result = self._persistence_client.save_json(metadata, output_file)
            self._logger.info("Successfully saved research metadata")
            return result
        except Exception as e:
            self._logger.error(f"Failed to save research metadata: {str(e)}")
            raise

    def load_research_metadata(self) -> Dict[str, Any]:
        """Load research metadata from a JSON file

        Returns:
            A dictionary containing the research metadata
        """
        file_path = f'output/{self.research_id}/{self.research_id}_meta.json'
        self._logger.debug(f"Loading research metadata from {file_path}")
        try:
            result = self._persistence_client.load_json(file_path)
            self._logger.info("Successfully loaded research metadata")
            return result
        except Exception as e:
            self._logger.error(f"Failed to load research metadata: {str(e)}")
            raise

    def search_advanced(self, query: str, **kwargs: Any) -> Dict[str, Any]:
        """Perform an advanced search

        Args:
            query: The search query
            **kwargs: Additional parameters to pass to the API

        Returns:
            The search results
        """
        self._logger.debug(f"Executing advanced search with query: {query}")
        try:
            response = self._search_client.search_with_template(
                query=query,
                template_name="advanced"
            )
            self._logger.info("Successfully executed advanced search")
            return response
        except Exception as e:
            self._logger.error(f"Failed to execute advanced search: {str(e)}")
            raise

    def generate_category_report(self, research_content: Dict[str, str], category: str, category_resources: List[Dict[str, str]]) -> str:
        """Generate a report for a specific category

        Args:
            research_content: The research content
            category: The category to generate a report for
            category_resources: The resources for the category

        Returns:
            The generated report
        """
        self._logger.info(f"Generating summary report for category: {category}")
        messages = [
            {"role": "user", "content": f'''You are a pro researcher. Current research topic is:

{research_content}

Under sub research category [{category}]

Please read all the collected resources and integrate into one comprehensive report.

Follow below:

- Based on the specified theme, please collect relevant literature and materials to generate a comprehensive report. 
- The report should be lengthy and thorough, with each section fully elaborated to ensure no detail from the literature is overlooked.
- Every section is written in a detailed and elaborate manner, with no omission of information.
- The analysis integrates all relevant literature, avoiding any gaps or oversights.
- structured the report

Collected resources to read:
```
{category_resources}
```

Provide output in Markdown format.
'''}
        ]
        try:
            result = self._llm_client.long_completion(messages, response_format='markdown')
            self._logger.info(f"Successfully generated report for category: {category}")
            return result
        except Exception as e:
            self._logger.error(f"Failed to generate category report: {str(e)}")
            raise

    @staticmethod
    def sanitize_filename(name: str) -> str:
        """Sanitize a string to be used as a filename

        Args:
            name: The string to sanitize

        Returns:
            A sanitized string safe for use as a filename
        """
        import re
        sanitized = re.sub(r'[^\w\s-]', '', name)
        sanitized = re.sub(r'[-\s]+', '_', sanitized)
        return sanitized

    def save_search_results(self, category: str, query: str, results: Dict[str, Any]) -> Dict[str, Any]:
        """Save search results to a JSON file

        Args:
            category: The category name
            query: The search query
            results: The search results to save

        Returns:
            A dictionary indicating success or error
        """
        sanitized_category = self.sanitize_filename(category)
        sanitized_query = self.sanitize_filename(query)
        output_path = f'output/{self.research_id}/{sanitized_category}'
        output_file = f'{output_path}/{sanitized_query}.json'

        self._logger.debug(f"Saving search results to {output_file}")
        try:
            os.makedirs(output_path, exist_ok=True)
            result = self._persistence_client.save_json(results, output_file)
            self._logger.info("Successfully saved search results")
            return result
        except Exception as e:
            self._logger.error(f"Failed to save search results: {str(e)}")
            raise

    def save_category_report(self, category: str, report: str) -> None:
        """Save a category report to a JSON file

        Args:
            category: The category name
            report: The report content
        """
        report_json = {
            "category": category,
            "report": report
        }
        sanitized_category = self.sanitize_filename(category)
        file_path = f'output/{self.research_id}/{sanitized_category}_report.json'

        self._logger.debug(f"Saving category report to {file_path}")
        try:
            self._persistence_client.save_json(report_json, file_path)
            self._logger.info(f"Successfully saved report for category: {category}")
        except Exception as e:
            self._logger.error(f"Failed to save category report: {str(e)}")
            raise

    def read_category_results(self, category: str) -> List[Dict[str, str]]:
        """Read results for a specific category

        Args:
            category: The category name

        Returns:
            A list of results for the category
        """
        sanitized_category = self.sanitize_filename(category)
        category_path = f'output/{self.research_id}/{sanitized_category}'

        self._logger.debug(f"Reading category results from {category_path}")
        results = []

        if not os.path.exists(category_path):
            self._logger.warning(f"Category path does not exist: {category_path}")
            return results

        json_files = glob.glob(os.path.join(category_path, '*.json'))
        for json_file in json_files:
            try:
                data = self._persistence_client.load_json(os.path.relpath(json_file))
                for result in data.get('results', []):
                    title = result.get('title', '')
                    content = result.get('raw_content') or result.get('content', '')
                    url = result.get('url', '')
                    if title and content and result.get('score', 0) > 0.6:
                        results.append({
                            'title': title,
                            'url': url,
                            'content': content
                        })
            except Exception as e:
                self._logger.error(f"Error processing file {json_file}: {str(e)}")
                continue

        self._logger.info(f"Successfully read {len(results)} results for category: {category}")
        return results

    def read_category_reports(self) -> List[Dict[str, str]]:
        """Read all category reports

        Returns:
            A list of category reports
        """
        report_path = f'output/{self.research_id}'
        self._logger.debug(f"Reading category reports from {report_path}")
        reports = []

        if not os.path.exists(report_path):
            self._logger.warning(f"Report path does not exist: {report_path}")
            return reports

        json_files = glob.glob(os.path.join(report_path, '*_report.json'))
        for json_file in json_files:
            try:
                data = self._persistence_client.load_json(os.path.relpath(json_file))
                reports.append(data)
            except Exception as e:
                self._logger.error(f"Error processing file {json_file}: {str(e)}")
                continue

        self._logger.info(f"Successfully read {len(reports)} category reports")
        return reports

    