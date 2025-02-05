


"""Utility module for workflow management"""

import json
from typing import Dict, Any
from datetime import datetime

class WorkflowManager:
    """Manager class for handling research workflow operations"""
    
    def __init__(self):
        """Initialize WorkflowManager with a unique ID based on current datetime"""
        self.workflow_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def save_research_results(self, results: Dict[str, Any], output_file: str) -> None:
        """Save research results to a JSON file
        Args:
            results: The research results to save
            output_file: The path to the output file
        """
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
    
    def save_research_metadata(self, metadata: Dict[str, Any], output_file: str) -> None:
        """Save research metadata to a JSON file
        Args:
            metadata: The research metadata to save
            output_file: The path to the output file
        """
        with open(output_file, 'w') as f:
            json.dump(metadata, f, indent=4)
    
    @property
    def id(self) -> str:
        """Get the workflow's unique ID
        Returns:
            The workflow's unique ID string
        """
        return self.workflow_id


