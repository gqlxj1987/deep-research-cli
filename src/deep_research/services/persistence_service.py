"""Utility module for JSON data persistence operations"""

import json
import os
from typing import Any, Dict, Optional

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
            return {"success": True, "data": data}
        except FileNotFoundError:
            return {"success": False, "error": f"File not found: {file_path}"}
        except json.JSONDecodeError:
            return {"success": False, "error": f"Invalid JSON format in file: {file_path}"}
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