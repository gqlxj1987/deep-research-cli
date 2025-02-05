"""Module for handling research operations"""

from datetime import datetime
from typing import List, Dict, Any
from deep_research.utils.research_helper import translate_to_english, generate_research_content, generate_research_plan

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
        self.research_plan = json_plan

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
        output_file = f'output/{self.research_id}/{self.research_id}_meta.json'
        persistence_client.save_json(metadata, output_file)

    

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
    research = Research(research_id="RS_20250205_212326")
    
    print(f"Created research with ID: {research.id}")
    print(f"Original topic: {research.topic}")
    print(f"English topic: {research.english_topic}")
    print("========================================================")
    print(f"Research Content: {research.research_content}")
    print("========================================================")
    print(f"Research Plan: {research.research_plan}")