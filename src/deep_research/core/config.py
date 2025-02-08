"""Configuration module for deep-research-cli"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for model settings"""
    SMART_MODEL = "deepseek/deepseek-r1"
    NORMAL_MODEL = "deepseek/deepseek-r1-distill-llama-70b"
    LONG_MODEL = "google/gemini-2.0-flash-001"
    REPORT_MODEL = "google/gemini-2.0-pro-exp-02-05:free"
    #SMART_MODEL = "deepseek-reasoner"
    #NORMAL_MODEL = "deepseek-reasoner"
    REPORT_LANG = "Chinese"

class LLMConfig:
    """Configuration class for LLM models"""
    def __init__(self):
        self.api_key = os.getenv('OPENAI_KEY')
        self.api_base = os.getenv('OPENAI_BASE')
        self.smart_model = os.getenv('SMART_MODEL', Config.SMART_MODEL)
        self.normal_model = os.getenv('NORMAL_MODEL', Config.NORMAL_MODEL)
        self.long_model = os.getenv('LONG_MODEL', Config.LONG_MODEL)

        if not self.api_key:
            raise ValueError('OPENAI_KEY environment variable is not set')

class SearchConfig:
    """Configuration class for Tavily Search API"""
    def __init__(self):
        self.api_key = os.getenv('TAVILY_API_KEY')
        if not self.api_key:
            raise ValueError('TAVILY_API_KEY environment variable is not set')