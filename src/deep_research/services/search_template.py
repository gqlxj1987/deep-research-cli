"""Module for managing search parameter templates"""

from typing import Dict, Any

class SearchTemplate:
    """Class for managing search parameter templates with predefined configurations"""

    # Predefined search templates
    TEMPLATES = {
        "basic": {
            "search_depth": "basic",
            "include_raw_content": True,
            "max_results": 5
        },
        "advanced": {
            "search_depth": "advanced",
            "max_results": 10,
            "include_domains": [],
            "exclude_domains": [],
            "include_raw_content": True,
        },
        "news": {
            "search_depth": "advanced",
            "max_results": 8,
            "include_raw_content": True,
            "topic": "news"
        },
        "academic": {
            "search_depth": "advanced",
            "max_results": 15,
            "include_raw_content": True,
            "include_domains": [".edu", ".org", "scholar.google.com"],
            "topic": "general"
        }
    }

    def load_template(self, name: str) -> Dict[str, Any]:
        """Load a predefined search parameter template
        
        Args:
            name: Name of the template to load
            
        Returns:
            Dictionary containing the template parameters or error message
        """
        if name in self.TEMPLATES:
            return {"success": True, "data": self.TEMPLATES[name].copy()}
        return {"success": False, "error": f"Template not found: {name}"}
    
    def apply_template(self, name: str, **override_params: Any) -> Dict[str, Any]:
        """Load a template and optionally override specific parameters
        
        Args:
            name: Name of the template to load
            **override_params: Optional parameters to override in the template
            
        Returns:
            Dictionary containing the final parameters or error message
        """
        result = self.load_template(name)
        if result["success"]:
            params = result["data"]
            params.update(override_params)
            return {"success": True, "data": params}
        return result