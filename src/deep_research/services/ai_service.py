"""Utility module for OpenAI LLM model interactions"""

import os
import json
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from ..core.config import LLMConfig

class LLMClient:
    """Client for interacting with OpenAI LLM models"""
    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig()
        
        try:
            import openai
            self.client = openai.OpenAI(
                api_key=self.config.api_key,
                base_url=self.config.api_base
            )
        except ImportError:
            raise ImportError(
                'OpenAI package is not installed. '
                'Please install it with: pip install openai'
            )

    def chat_completion(
        self,
        messages: list[Dict[str, str]],
        model: Optional[str] = None,
        response_format: Optional[Dict[str, str]] = {"type": "json_object"},
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Send a chat completion request to the OpenAI API

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Optional model override, defaults to normal_model
            response_format: Optional response format, e.g. {"type": "json_object"}
            **kwargs: Additional parameters to pass to the API

        Returns:
            The response content as a JSON object
        """
        params = {
            "model": model or self.config.normal_model,
            "messages": messages
        }
        
        if response_format:
            params["response_format"] = response_format
            
        response = self.client.chat.completions.create(
            **params,
            **kwargs
        )
        content = response.choices[0].message.content
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"response": content}

    def smart_completion(
        self,
        messages: list[Dict[str, str]],
        response_format: Optional[Dict[str, str]] = {"type": "json_object"},
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Use the smart model (e.g. GPT-4) for chat completion

        Args:
            messages: List of message dictionaries
            response_format: Optional response format, e.g. {"type": "json_object"}
            **kwargs: Additional parameters to pass to the API

        Returns:
            The response content as a JSON object
        """
        return self.chat_completion(
            messages=messages,
            model=self.config.smart_model,
            response_format=response_format,
            **kwargs
        )

if __name__ == '__main__':
    # Example usage of LLMClient
    try:
        client = LLMClient()
        
        # Test normal completion
        messages = [
            {"role": "user", "content": "What is Python?"}
        ]
        print("\nNormal Completion Test:")
        response = client.chat_completion(messages)
        print(response)
        
    except Exception as e:
        print(f"Error: {str(e)}")