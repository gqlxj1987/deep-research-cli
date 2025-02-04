"""Utility module for Tavily search API interactions"""

from typing import Optional, Dict, Any, List
from deep_research.core.config import SearchConfig

class SearchClient:
    """Client for interacting with Tavily Search API"""
    def __init__(self, config: Optional[SearchConfig] = None):
        self.config = config or SearchConfig()
        
        try:
            from tavily import TavilyClient
            self.client = TavilyClient(api_key=self.config.api_key)
        except ImportError:
            raise ImportError(
                'Tavily package is not installed. '
                'Please install it with: pip install tavily-python'
            )
    
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
        results = client.get_search_results("What is Python programming?")
        
        print("\nSearch Results:")
        for idx, result in enumerate(results, 1):
            print(f"\nResult {idx}:")
            print(f"Title: {result['title']}")
            print(f"Content: {result['content']}")
            print(f"URL: {result['url']}")
            
    except Exception as e:
        print(f"Error: {str(e)}")