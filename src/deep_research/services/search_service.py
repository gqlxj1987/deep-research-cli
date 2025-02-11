"""Utility module for Tavily search API interactions

This module provides a client interface for interacting with the Tavily Search API,
with support for templated searches and configurable parameters.
"""

from typing import Optional, Dict, Any, List
from deep_research.core.config import SearchConfig
from deep_research.services.search_template import SearchTemplate
from deep_research.utils.log_util import LogUtil

class SearchClient:
    """Client for interacting with Tavily Search API
    
    This class provides methods to perform searches using the Tavily API,
    with support for template-based parameter configurations and error handling.
    """
    def __init__(self, config: Optional[SearchConfig] = None, template_dir: Optional[str] = None):
        """Initialize the SearchClient with configuration and templates
        
        Args:
            config: Optional SearchConfig instance for API configuration
            template_dir: Optional directory path for custom templates
        
        Raises:
            ImportError: If tavily-python package is not installed
            ValueError: If TAVILY_API_KEY is not set
        """
        # Initialize logger
        self.logger = LogUtil.get_logger()
        self.logger.debug("Initializing SearchClient")
        
        # Set up configuration and template
        self.config = config or SearchConfig()
        self.template = SearchTemplate()
        
        try:
            from tavily import TavilyClient
            self.client = TavilyClient(api_key=self.config.api_key)
            self.logger.info("Successfully initialized Tavily client")
        except ImportError:
            self.logger.error("Failed to import tavily package")
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
        self.logger.debug(f"Applying template '{template_name}' for query: {query}")
        
        # Apply template and get parameters
        template_result = self.template.apply_template(template_name, **override_params)
        if not template_result["success"]:
            error_msg = f"Template error: {template_result.get('error', 'Unknown error')}"
            self.logger.error(error_msg)
            return {"error": error_msg}
            
        # Prepare search parameters
        params = template_result["data"]
        params["query"] = query  # Ensure query is included in params
        self.logger.debug(f"Search parameters prepared: {params}")
        
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
        self.logger.info(f"Executing search query: {query} with depth: {search_depth}")
        
        try:
            # Execute search request
            response = self.client.search(
                query=query,
                search_depth=search_depth,
                max_results=max_results,
                **kwargs
            )
            self.logger.debug(f"Search completed successfully with {len(response.get('results', []))} results")
            return response
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"Search failed: {error_msg}")
            return {"error": error_msg}


if __name__ == '__main__':
    # Example usage of SearchClient
    logger = LogUtil.get_logger()
    try:
        logger.info("Starting example search")
        client = SearchClient()
        response = client.search_with_template(
            query="What is DeepSeek R1",
            template_name="advanced"
        )
        
        print(response)
        logger.info("Example search completed")
            
    except Exception as e:
        logger.error(f"Example failed: {str(e)}")