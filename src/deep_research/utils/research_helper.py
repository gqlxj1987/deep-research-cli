"""Utility module for business-level operations and prompts"""

from typing import Dict, Any, List
from deep_research.services.ai_service import LLMClient
from deep_research.services.search_service import SearchClient
from deep_research.core.config import Config

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
        {"role": "user", "content": f'''You are a research expert, to provide comprehensive framework of searching keywords for user to search information for research purpose.

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

rethink until you think the plan is comprehensive for finding the answer or support the research. Adjust or append if you think still missing some. 
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

def generate_research_category_report(research_content: Dict[str, str], category: str, category_resrouces: List[Dict[str, str]]):
    print(f'Generating summary report for category: {category}...')
    client = LLMClient()
    messages = [
        {"role": "user", "content": f'''You are a pro researcher. Current research topic is:

{research_content}

Under sub research category [{category}]

Please read all the collected resources and integrate into one comprehensive report.

Follow below:

- Based on the specified theme, please collect relevant literature and materials to generate a comprehensive report. 
- The report should be lengthy and thorough, with each section fully elaborated to ensure no detail from the literature is overlooked.
- Every section is written in a detailed and elaborate manner, with no omission of information.
- The analysis integrates all relevant literature, avoiding any gaps or oversights.
- structured the report

Collected resources to read:
```
{category_resrouces}
```

Provide output in Markdown format.
'''}
    ]
    response = client.long_completion(messages, response_format='markdown')
    #print(response)
    return response

def generate_research_final_report(research_content: Dict[str, str], reports: List[Dict[str, str]], model: str = Config.REPORT_MODEL):
    client = LLMClient()
    messages = [
        {"role": "system", "content": f'''Your Task: Based on the provided literature and materials, your goal is to compile a comprehensive and detailed investigative report. 
The report provide extensive analysis, insights, and explanations to ensure sufficient length and depth. Provide report with more than 6000 Tokens.

Instructions:

- Integrate the Literature: First, you need to integrate all the content from the provided literature. Avoid deleting or simplifying the information; instead, reorganize it logically. 
- Each section should be written in a detailed and elaborate manner, with no omission of information. Make sure Add as much explanations to make the every section more detailed and easier to understand.
- Develop Insights: After summarizing, carefully analyze the content and the research topic to develop meaningful insights. These insights should go beyond what is explicitly mentioned in the literature and uncover new perspectives or implications.
- Deepen the Insights: Continuously reflect on your insights to generate even deeper and more profound observations. The goal is to create a report that offers truly insightful analysis.
- Structure Your Insights: You should identify at least five key insights. Each insight should be thoroughly explained in its own section, detailing your thought process and reasoning.
- Ensure Clarity and Logic: The final report should have a clear structure and logical flow.
- Use tables and graphs when necessary to support your insights.
- Format the Output: Use Markdown to format the report and present it to me. 

---

Research Topic: 
{research_content}


Collected Literatures: 
{reports}

---
Report format:

- Use [{Config.REPORT_LANG}]
- Markdown format
- with Key highlighted using ** bold
- Title #, Section ##, Subsection ###


Provide your output in markdown format.

'''}
    ]
    response = client.chat_completion(messages, model=model, response_format='markdown')
    #print(response)
    return response



if __name__ == '__main__':
    # Example usage of translate_to_english
    re = search_advanced("What impact of X platform in 2025")
    print(re)


    