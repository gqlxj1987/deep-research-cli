"""Utility module for business-level operations and prompts"""

from typing import Dict, Any
from deep_research.services.ai_service import LLMClient

def translate_to_english(
    text: str,
    client: LLMClient = None,
    **kwargs: Any
) -> Dict[str, str]:
    """Translate any text to English using the LLM model

    Args:
        text: The text to translate to English
        client: Optional LLMClient instance. If not provided, a new one will be created
        **kwargs: Additional parameters to pass to the API

    Returns:
        The English translation as a string in a dictionary format
    """
    if client is None:
        client = LLMClient()

    messages = [
        {"role": "system", "content": "You are a professional translator. Translate the input text to English. Only return the translated text without any explanations or additional content. Return in Json format: {response:\"\"}"},
        {"role": "user", "content": text}
    ]
    return client.smart_completion(messages, **kwargs)




if __name__ == '__main__':
    # Example usage of translate_to_english
    re = translate_to_english("你好")
    print(re)
    
    print(re['response'])
    