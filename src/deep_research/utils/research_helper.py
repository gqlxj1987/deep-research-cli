"""Utility module for business-level operations and prompts"""

from typing import Dict, Any
from deep_research.services.ai_service import LLMClient
from deep_research.services.search_service import SearchClient

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
        {"role": "user", "content": f"""You are a professional translator. Translate the [{text}] to English. Only return translated text in Json format: {{response:""}}"""}
    ]
    return client.chat_completion(messages, **kwargs)['response']

def generate_research_content(
    text: str,
    client: LLMClient = None,
    **kwargs: Any
) -> Dict[str, str]:
    if client is None:
        client = LLMClient()

    messages = [
        {"role": "user", "content": f'''You are a research planner, to provide comprehensive framework of searching keywords for user to search information for research purpose.

User will provide a topic or target for research.

You will think about the topic or target, deep dive in the core question and target, define the scope of the research and goal and meaning of the research to help set up a solid background content of the whole research.

return your result in JSON format:

```
{{
  original_topic: "",
  core_research_topic:"",
  research_scope:"",
  research_target:""
}}
```
Research Topic: [{text}]'''}
    ]

    response = client.smart_completion(messages, **kwargs)
    #print(response)
    return response


def generate_research_plan(
    research_content: Dict[str, str],
    client: LLMClient = None,
    **kwargs: Any
) -> Dict[str, str]:
    if client is None:
        client = LLMClient()

    messages = [
        {"role": "user", "content": f'''You are a research planner, to provide comprehensive framework of searching keywords for user to search information for research purpose.

Based on below research information, you will work out a comprehensive list of queries for user to collect informations on Search Engines cover everything aspect of the research goal.

```
{research_content}
```
You will provide the research plan in below  in JSON format:

```
{{
  research_plan: [
    {{
      category: "",
      category_research_goal: "",
      queries_list: ["",""]
    }},
    {{
      category: "",
      category_research_goal: "",
      queries_list: ["",""]
    }}
  ]
}}
```

rethink until you think the plan is comprehensive for a profressional research. Adjust or append if you think still missing some. 
Provide output in pure JSON format.
'''}
    ]

    response = client.smart_completion(messages, **kwargs)
    #print(response)
    return response

def search_advanced(
    query: str,
    **kwargs: Any
) -> Dict[str, Any]:
    client = SearchClient()
    response = client.search_with_template(
        query=query,
        template_name="advanced"
    )
    print(response)
    return response


if __name__ == '__main__':
    # Example usage of translate_to_english
    re = search_advanced("What impact of X platform in 2025")
    print(re)


    