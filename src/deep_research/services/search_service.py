"""Utility module for Tavily search API interactions"""

from typing import Optional, Dict, Any, List
from deep_research.core.config import SearchConfig
from deep_research.services.search_template import SearchTemplate

class SearchClient:
    """Client for interacting with Tavily Search API"""
    def __init__(self, config: Optional[SearchConfig] = None, template_dir: Optional[str] = None):
        self.config = config or SearchConfig()
        self.template = SearchTemplate()
        
        try:
            from tavily import TavilyClient
            self.client = TavilyClient(api_key=self.config.api_key)
        except ImportError:
            raise ImportError(
                'Tavily package is not installed. '
                'Please install it with: pip install tavily-python'
            )
    
    def search_with_template(
        self,
        query: str,
        template_name: str,
        **override_params: Any
    ) -> Dict[str, Any]:
        """Perform a search using a parameter template

        Args:
            query: The search query string
            template_name: Name of the template to use
            **override_params: Parameters to override from the template

        Returns:
            The search results as a dictionary
        """
        template_result = self.template.apply_template(template_name, **override_params)
        if not template_result["success"]:
            return {"error": f"Template error: {template_result.get('error', 'Unknown error')}"}
            
        params = template_result["data"]
        params["query"] = query  # Ensure query is included in params
        return self.search(**params)
    
    def search(
        self,
        query: str,
        search_depth: str = "basic",
        max_results: int = 5,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Perform a search using the Tavily API

        Args:
            query: The search query string
            search_depth: The depth of search ('basic' or 'advanced')
            max_results: Maximum number of results to return
            **kwargs: Additional parameters to pass to the API

        Returns:
            The search results as a dictionary
        """
        try:
            response = self.client.search(
                query=query,
                search_depth=search_depth,
                max_results=max_results,
                **kwargs
            )
            return response
        except Exception as e:
            return {"error": str(e)}

    def get_search_results(
        self,
        query: str,
        max_results: int = 5
    ) -> List[Dict[str, str]]:
        """Get formatted search results

        Args:
            query: The search query string
            max_results: Maximum number of results to return

        Returns:
            List of dictionaries containing title, content, and url for each result
        """
        response = self.search(query, max_results=max_results)
        
        if "error" in response:
            return [{"error": response["error"]}]
            
        results = []
        for result in response.get("results", []):
            results.append({
                "title": result.get("title", ""),
                "content": result.get("content", ""),
                "url": result.get("url", "")
            })
        return results


if __name__ == '__main__':
    # Example usage of SearchClient
    try:
        client = SearchClient()
        response = client.search_with_template(
            query="What is DeepSeek R1",
            template_name="advanced"
        )
        
        print(response)
            
    except Exception as e:
        print(f"Error: {str(e)}")