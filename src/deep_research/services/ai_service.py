"""Utility module for OpenAI LLM model interactions

This module provides a client interface for interacting with OpenAI-compatible LLM models.
It handles different types of completions (normal, smart, long) and supports various response formats.
"""

import os
import json
import json_repair
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

from ..core.config import LLMConfig
from ..utils.log_util import LogUtil

class LLMClient:
    """Client for interacting with OpenAI LLM models
    
    This class provides methods to interact with different types of LLM models,
    handling authentication, API calls, and response processing.
    """
    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig()
        self.logger = LogUtil.get_logger()
        
        try:
            import openai
            self.client = openai.OpenAI(
                api_key=self.config.api_key,
                base_url=self.config.api_base
            )
            self.google_client = genai.Client(
                api_key=self.config.api_key
            )
            self.logger.info("Successfully initialized OpenAI client")
        except ImportError:
            self.logger.critical("OpenAI package is not installed")
            raise ImportError(
                'OpenAI package is not installed. '
                'Please install it with: pip install openai'
            )

    def chat_completion(
        self,
        messages: list[Dict[str, str]],
        model: Optional[str] = None,
        response_format: str = 'json',
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Send a chat completion request to the OpenAI API

        This method handles the core interaction with the OpenAI API, including
        response format handling and token limit management for certain models.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Optional model override, defaults to normal_model
            response_format: Optional response format, e.g. {"type": "json_object"}
            **kwargs: Additional parameters to pass to the API

        Returns:
            The response content as a JSON object or markdown string
        """
        model = model or self.config.normal_model
        
        if model.startswith('gemini'):
            try:
                # Convert messages to parts.  Gemini expects 'parts' as a list of text strings or image data.
                parts = []
                for message in messages:
                    if message['role'] == 'user':
                        parts.append(types.Part.from_text(message['content'])) #User text becomes a part
                    elif message['role'] == 'model':
                        parts.append(types.Part.from_text(message['content'])) #Model messages need to be converted to Parts
                    else:
                        raise ValueError(f"Invalid role: {message['role']}. Role must be 'user' or 'model'.")
                
                contents=types.Content(parts=parts, role='user')

                response = self.google_client.generate_content(
                    model=model, 
                    contents=contents,
                    config={
                        'response_mime_type': 'application/json'      
                    }
                )
                print(response.text)
                repaired_json = json_repair.loads(response.text)
                return repaired_json
            except Exception as e:
                self.logger.error(f"GenAI error: {str(e)}")
                raise
        else:
            # Prepare request parameters
            params = {
            "model": model or self.config.normal_model,
                "messages": messages
            }
            
            self.logger.debug(f"Sending chat completion request with model: {params['model']}")
                
            try:
                response = self.client.chat.completions.create(
                    **params,
                    **kwargs
                )
                self.logger.debug("Successfully received response from API")
                content = response.choices[0].message.content

                # Handle markdown format with potential token limit handling
                if response_format == 'markdown':
                    # Check if response was truncated due to token limit
                    if response.choices[0].native_finish_reason == 'MAX_TOKENS' and 'google' in model.lower():
                        self.logger.info("Response truncated due to token limit, continuing conversation")
                        # Append the partial response to messages and continue the conversation
                        messages.append({"role": "assistant", "content": content})
                        messages.append({"role": "user", "content": "Please continue from where you left off."})                
                        # Recursively get the rest of the response
                        continuation = self.chat_completion(
                            messages=messages,
                            model=model,
                            response_format='markdown',
                            **kwargs
                        )
                        # Combine the current content with the continuation
                        return content + continuation
                    return content
                
                # Handle JSON format
                if response_format == 'json':
                    try:
                        repaired_json = json_repair.loads(content)
                        return repaired_json
                    except Exception as e:
                        self.logger.error(f"Failed to parse JSON response: {str(e)}")
                        raise
                
                return content
            except Exception as e:
                self.logger.error(f"Error in chat completion: {str(e)}")
                raise

    def smart_completion(
        self,
        messages: list[Dict[str, str]],
        response_format: str = 'json',
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Use the smart model (e.g. GPT-4) for chat completion

        This method is optimized for tasks requiring higher intelligence and reasoning.

        Args:
            messages: List of message dictionaries
            response_format: Optional response format, e.g. {"type": "json_object"}
            **kwargs: Additional parameters to pass to the API

        Returns:
            The response content as a JSON object
        """
        self.logger.info(f"Using smart model: {self.config.smart_model}")
        return self.chat_completion(
            messages=messages,
            model=self.config.smart_model,
            response_format=response_format,
            stream=False,
            **kwargs
        )

    def long_completion(
        self,
        messages: list[Dict[str, str]],
        response_format: str = 'json',
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Use the long context model for chat completion

        This method is designed for handling longer conversations or inputs
        that require more context window.

        Args:
            messages: List of message dictionaries
            response_format: Optional response format, e.g. {"type": "json_object"}
            **kwargs: Additional parameters to pass to the API

        Returns:
            The response content as a JSON object
        """
        self.logger.info(f"Using long context model: {self.config.long_model}")
        return self.chat_completion(
            messages=messages,
            model=self.config.long_model,
            response_format=response_format,
            stream=False,
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