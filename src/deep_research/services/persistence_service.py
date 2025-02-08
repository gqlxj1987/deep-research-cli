"""Utility module for JSON data persistence operations"""

import json
import os
from typing import Any, Dict, Optional, List

class PersistenceClient:
    """Client for handling JSON data persistence operations"""
    
    def __init__(self, base_dir: Optional[str] = None):
        """Initialize the persistence client
        
        Args:
            base_dir: Optional base directory for storing files. If not provided,
                     uses the current working directory
        """
        self.base_dir = base_dir or os.getcwd()
        
    def save_json(self, data: Any, file_path: str) -> Dict[str, Any]:
        """Save data to a JSON file
        
        Args:
            data: The data to save (must be JSON serializable)
            file_path: Path to the file where data will be saved
            
        Returns:
            A dictionary indicating success or error
        """
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(os.path.join(self.base_dir, file_path)), exist_ok=True)
            
            # Write data to file
            with open(os.path.join(self.base_dir, file_path), 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return {"success": True, "message": f"Data successfully saved to {file_path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    
    def load_json(self, file_path: str) -> Dict[str, Any]:
        """Load data from a JSON file
        
        Args:
            file_path: Path to the file to load data from
            
        Returns:
            A dictionary containing either the loaded data or an error message
        """
        try:
            with open(os.path.join(self.base_dir, file_path), 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except Exception as e:
            raise ValueError(f"Failed to load JSON data from {file_path}: {str(e)}")

    def save_research_metadata(self, research_id: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Save research metadata to a JSON file
        
        Args:
            research_id: The unique identifier for the research
            metadata: The metadata to save
            
        Returns:
            A dictionary indicating success or error
        """
        output_file = f'output/{research_id}/{research_id}_meta.json'
        return self.save_json(metadata, output_file)

    def load_research_metadata(self, research_id: str) -> Dict[str, Any]:
        """Load research metadata from a JSON file
        
        Args:
            research_id: The unique identifier for the research
            
        Returns:
            A dictionary containing the research metadata
        """
        file_path = f'output/{research_id}/{research_id}_meta.json'
        return self.load_json(file_path)

    def save_search_results(self, research_id: str, category: str, query: str, results: Dict[str, Any]) -> Dict[str, Any]:
        """Save search results to a JSON file
        
        Args:
            research_id: The unique identifier for the research
            category: The category name
            query: The search query
            results: The search results to save
            
        Returns:
            A dictionary indicating success or error
        """
        import re
        # Sanitize category and query for filename
        sanitized_category = re.sub(r'[^\w\s-]', '', category)
        sanitized_category = re.sub(r'[-\s]+', '_', sanitized_category)
        sanitized_query = re.sub(r'[^\w\s-]', '', query)
        sanitized_query = re.sub(r'[-\s]+', '_', sanitized_query)

        output_path = f'output/{research_id}/{sanitized_category}'
        os.makedirs(output_path, exist_ok=True)
        output_file = f'{output_path}/{sanitized_query}.json'
        return self.save_json(results, output_file)

    def load_category_results(self, research_id: str, category: str) -> List[Dict[str, str]]:
        """Load all search results for a specific category
        
        Args:
            research_id: The unique identifier for the research
            category: The category name
            
        Returns:
            A list of dictionaries containing title and content for each result
        """
        import re
        import glob

        # Sanitize category name for folder path
        sanitized_category = re.sub(r'[^\w\s-]', '', category)
        sanitized_category = re.sub(r'[-\s]+', '_', sanitized_category)
        category_path = f'output/{research_id}/{sanitized_category}'

        # Initialize result list
        results = []

        # Check if category directory exists
        if not os.path.exists(category_path):
            return results

        # Get all JSON files in the category directory
        json_files = glob.glob(os.path.join(category_path, '*.json'))

        # Process each JSON file
        for json_file in json_files:
            try:
                # Load the JSON file
                data = self.load_json(os.path.relpath(json_file))

                # Process each result in the file
                for result in data.get('results', []):
                    title = result.get('title', '')
                    # Use raw_content if available, otherwise fall back to content
                    content = result.get('raw_content') or result.get('content', '')
                    url = result.get('url', '')
                    if title and content and result.get('score', 0) > 0.5:
                        results.append({
                            'title': title,
                            'url': url,
                            'content': content
                        })
            except Exception as e:
                print(f"Error processing file {json_file}: {str(e)}")
                continue

        return results

    def load_category_reports(self, research_id: str) -> List[Dict[str, str]]:
        import re
        import glob

        # Initialize list
        reports = []

        report_path = f'output/{research_id}'

        # Check if category directory exists
        if not os.path.exists(report_path):
            return reports

        # Get all JSON files in the category directory
        json_files = glob.glob(os.path.join(report_path, '*_report.json'))

        # Process each JSON file
        for json_file in json_files:
            try:
                # Load the JSON file
                data = self.load_json(os.path.relpath(json_file))
                reports.append(data)
            except Exception as e:
                print(f"Error processing file {json_file}: {str(e)}")
                continue

        return reports

    def save_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Save content to a file
        
        Args:
            file_path: Path to the file where content will be saved
            content: The content to save to the file
            
        Returns:
            A dictionary indicating success or error
        """
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(os.path.join(self.base_dir, file_path)), exist_ok=True)
            
            # Write content to file
            with open(os.path.join(self.base_dir, file_path), 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {"success": True, "message": f"Content successfully saved to {file_path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

if __name__ == '__main__':
    # Example usage of PersistenceClient
    client = PersistenceClient()
    
    # Example data
    test_data = {
        "name": "Test User",
        "age": 30,
        "interests": ["programming", "reading"]
    }
    
    # Save data
    save_result = client.save_json(test_data, "test_data.json")
    print("Save result:", save_result)
    
    # Load data
    load_result = client.load_json("test_data.json")
    print("\nLoad result:", load_result)