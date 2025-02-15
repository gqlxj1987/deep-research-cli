"""Module for handling report generation operations

This module provides functionality for generating various types of research reports,
including WeChat articles, research reports, and detailed research reports.
It uses LLM models for content generation and handles file operations for saving reports.
"""

from typing import Dict, Any, List
from deep_research.core.config import Config
from deep_research.services.persistence_service import PersistenceClient
from deep_research.utils.research_helper import ResearchHelper
from deep_research.services.ai_service import LLMClient
from deep_research.utils.log_util import LogUtil
import time
import os
from datetime import datetime

class Report:
    """Class for managing report generation operations
    
    This class handles the generation of different types of research reports,
    including WeChat articles and comprehensive research reports. It manages
    the loading of research data, report generation using LLM models, and
    saving of generated reports.
    """

    def __init__(self, research_id: str):
        """Initialize a new report instance

        Args:
            research_id: The ID of the research to generate reports for

        Raises:
            ValueError: If research data cannot be loaded for the given ID
        """
        self.research_id = research_id
        self._persistence_client = PersistenceClient()
        self._research_helper = ResearchHelper(research_id)
        self._logger = LogUtil().logger
        self._logger.info(f"Initializing Report instance for research ID: {research_id}")
        self._load_research_data()

    def _load_research_data(self) -> None:
        """Load research metadata from local storage
        
        Raises:
            ValueError: If research data cannot be loaded or is invalid
        """
        file_path = f'output/{self.research_id}/{self.research_id}_meta.json'
        try:
            self._logger.debug(f"Loading research data from {file_path}")
            data = self._persistence_client.load_json(file_path)
            self.research_content = data['research_content']
            self.research_plan = data['research_plan']
            self._logger.info("Successfully loaded research data")
        except Exception as e:
            error_msg = f"Failed to load research data for ID {self.research_id}: {str(e)}"
            self._logger.error(error_msg)
            raise ValueError(error_msg)


    def generate_wechat_article(self, model: str = Config.SMART_MODEL) -> str:
        """Generate a WeChat article based on research data

        This method generates a user-friendly article suitable for WeChat platform,
        incorporating research findings in an engaging and accessible format.

        Args:
            model: The LLM model to use for report generation

        Returns:
            The generated article content as a string

        Raises:
            ValueError: If no research plan is available
        """
        if not self.research_plan:
            self._logger.error("No research plan available for WeChat article generation")
            raise ValueError("No research plan available")

        self._logger.info(f"Starting WeChat article generation using model: {model}")
        reports = self._research_helper.read_category_reports()


        client = LLMClient()
        messages = [
                {"role": "system", "content": f'''你的任务是根据课题和收集到的资料，编写一篇温柔的微信公众号文章。 

要求:

- {os.getenv('REPORT_WECHAT_PROMPT', "")}
- 要有一个吸引眼球但不要太肤浅的标题
- 文本要具有亲和力，每个段落要有感情，要有温度，要有代入感，要有深度，并添加你非常详细的解释涉及到的原理或者知识的背景。
- 不要有太多奇怪的比喻。
- 内容有情绪，有代入感，文字通俗，偶尔使用 emoji。
- 文章最后要把所有相关的科学的依据罗列出来。


---

话题和相关信息: 
{self.research_content}


收集的资料和全文报告: 
{reports}

---
输出文章格式:

- Use [{Config.REPORT_LANG}]
- Markdown format
- with Key highlighted using ** bold
- Title #
- Section ## with insights
- Subsection ### with lengthy explaination on each section

Provide your output in markdown format. 简体中文编写，字数需要大于 2000 字。

        '''}
            ]
        try:
            report_content = client.chat_completion(messages, model=model, response_format='markdown')
            model_name = self._research_helper.sanitize_filename(model)
            file_path = f'output/{self.research_id}/{self.research_id}_{model_name}_wechat.md'
            self._persistence_client.save_file(file_path, report_content)
            self._logger.info(f"Successfully generated and saved WeChat article to {file_path}")
            return report_content
        except Exception as e:
            error_msg = f"Failed to generate WeChat article: {str(e)}"
            self._logger.error(error_msg)
            raise


    def generate_research_report(self, model=Config.SMART_MODEL) -> Dict[str, Any]:
        """Generate a comprehensive research report

        This method creates a detailed research report that includes analysis,
        insights, and explanations based on the collected literature.

        Args:
            model: The LLM model to use for report generation

        Returns:
            The generated report content

        Raises:
            ValueError: If no research plan is available
        """
        if not self.research_plan:
            self._logger.error("No research plan available for research report generation")
            raise ValueError("No research plan available")

        self._logger.info(f"Starting research report generation using model: {model}")
        reports = self._research_helper.read_category_reports()


        client = LLMClient()
        messages = [
            {"role": "system", "content": f'''Your Task: Based on the provided literature and materials, your goal is to compile a comprehensive and detailed investigative report. 
    The report provide extensive analysis, insights, and explanations to ensure sufficient length and depth. 

    Instructions:

    - {os.getenv('REPORT_PROMPT', "")}
    - Always Focus on the research goal.
    - Integrate the Literature: First, you need to integrate all the content from the provided literature. Avoid deleting or simplifying the information; instead, reorganize it logically with explain content for each. 
    - Numbers and Statistics: Always leave the reference source together.
    - Develop Insights: carefully analyze the content and the research topic to develop meaningful insights. These insights should go beyond what is explicitly mentioned in the literature and uncover new perspectives or implications.
    - Do not mention numbers you don't have evidence to support or skip sections without actual numbers from literature.
    - Use Tables or Mermaid Graphs to illustrate but only if needed.

    ---

    Research Topic: 
    {self.research_content}


    Collected Literatures: 
    {reports}

    ---
    Report format:

    - Use [{Config.REPORT_LANG}]
    - Markdown format
    - with Key highlighted using ** bold
    - Title #
    - Section ## with insights
    - Subsection ### with lengthy explaination on each section


    Provide your output in markdown format. 

    '''}
        ]
        try:
            report_content = client.chat_completion(messages, model=model, response_format='markdown')
            model_name = self._research_helper.sanitize_filename(model)
            file_path = f'output/{self.research_id}/{self.research_id}_{model_name}_research.md'
            persistence_client = PersistenceClient()
            persistence_client.save_file(file_path, report_content)
            self._logger.info(f"Successfully generated and saved research report to {file_path}")
            return report_content
        except Exception as e:
            error_msg = f"Failed to generate research report: {str(e)}"
            self._logger.error(error_msg)
            raise


    def generate_research_report_detailed(self, model=Config.REPORT_MODEL) -> Dict[str, Any]:
        """Generate a detailed research report

        This method creates a comprehensive and detailed research report with
        extensive analysis and insights from the collected literature.

        Args:
            model: The LLM model to use for report generation

        Returns:
            The generated detailed report content

        Raises:
            ValueError: If no research plan is available
        """
        if not self.research_plan:
            self._logger.error("No research plan available for detailed research report generation")
            raise ValueError("No research plan available")

        self._logger.info(f"Starting detailed research report generation using model: {model}")
        reports = self._research_helper.read_category_reports()


        client = LLMClient()
        messages = [
            {"role": "system", "content": f'''Your Task: Based on the provided literature and materials, your goal is to compile a comprehensive and detailed investigative report. 
 
    Instructions:

    - {os.getenv('REPORT_PROMPT', "")}
    - Always Focus on the research goal.
    - Integrate the Literature: First, you need to integrate all the content from the provided literature. 
    - Numbers and Statistics: Always leave the reference source together.
    - Comprehensive and detail, organized structured report with logical section order, do not summarize.
    - Conclusion with deepen insights
    - Use Tables or Mermaid Graphs to illustrate but if needed.
    
    ---

    Research Topic: 
    {self.research_content}


    Collected Literatures: 
    {reports}

    ---
    Report format:

    - Use [{Config.REPORT_LANG}]
    - Markdown format
    - with Key highlighted using ** bold
    - Title #
    - Section ## with insights
    - Subsection ### with detailed content

    Provide your output in markdown format. 

    '''}
        ]
        try:
            report_content = client.chat_completion(messages, model=model, response_format='markdown')
            model_name = self._research_helper.sanitize_filename(model)
            file_path = f'output/{self.research_id}/{self.research_id}_{model_name}_detail_research.md'
            persistence_client = PersistenceClient()
            persistence_client.save_file(file_path, report_content)
            self._logger.info(f"Successfully generated and saved detailed research report to {file_path}")
            return report_content
        except Exception as e:
            error_msg = f"Failed to generate detailed research report: {str(e)}"
            self._logger.error(error_msg)
            raise


if __name__ == "__main__":
    research_id = "RS_20250210_214128"  # Example research ID
    report = Report(research_id)
    article_content = report.generate_wechat_article(model='deepseek/deepseek-r1')
