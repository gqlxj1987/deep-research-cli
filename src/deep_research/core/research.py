"""Module for handling research operations"""

from datetime import datetime
from typing import List, Dict, Any
from deep_research.utils.research_helper import translate_to_english, generate_research_content, generate_research_plan

class Research:
    """Class for managing research operations"""

    def __init__(self, topic: str):
        """Initialize a new research instance

        Args:
            topic: The research topic in any language
        """
        self.topic = topic
        self.research_id = 'RS_' + datetime.now().strftime("%Y%m%d_%H%M%S")
        self.english_topic = self._translate_topic()
        self.research_content = None
        self.research_plan = None

        self.create_research_detail(self.english_topic)

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
        self.research_plan = json_plan


    @property
    def id(self) -> str:
        """Get the research's unique ID

        Returns:
            The research's unique ID string
        """
        return self.research_id


if __name__ == "__main__":
    """Main function to demonstrate Research class usage"""
    topic = "What impact of X platform in 2025"
    research = Research(topic)
    
    print(f"Created research with ID: {research.id}")
    print(f"Original topic: {research.topic}")
    print(f"English topic: {research.english_topic}")
    print("========================================================")
    print(f"Research Content: {research.research_content}")
    print("========================================================")
    print(f"Research Plan: {research.research_plan}")