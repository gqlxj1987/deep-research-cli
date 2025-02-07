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

def generate_research_category_report(research_content: Dict[str, str], category: str, category_resrouces: List[Dict[str, str]]):
    client = LLMClient()
    messages = [
        {"role": "user", "content": f'''You are a pro researcher. Current research topic is:

{research_content}

Under sub research category [{category}]

Please read all the collected resources and sorted into one comprehensive report, output in json format.

Follow below:

- Based on the specified theme, please collect and summarize relevant literature and materials to generate a comprehensive report. When summarizing, please ensure that all important numerical data and key information are preserved. Do not condense or omit any critical details. Instead, organize and group similar information together to create a cohesive report that retains all essential and complete key points. The final report should maintain the integrity of the original data and information while presenting it in a structured and organized manner. Ensure that no significant figures, percentages, or other critical numerical values are lost or altered during the summarization process. If there are multiple sources providing similar data, please include all relevant information without merging or simplifying it. The goal is to create a report that serves as a complete and accurate representation of the collected materials, preserving all important details for further analysis or reference.
- Every section is written in a detailed and elaborate manner, with no omission of critical information.
- The analysis integrates all relevant literature, avoiding any gaps or oversights.
- Based on current category and overall research topic and goals, rethink out of box, provide your own deep dive opinions and insights.
- rethink again, provide a deeper insights.
- structured the report

Collected resources to read:
```
{category_resrouces}
```

Provide output in JSON format.

```
{{
  category: "",
  category_report_in_markdown: ""
}}
```'''}
    ]
    response = client.long_completion(messages)
    #print(response)
    return response

def generate_research_final_report(research_content: Dict[str, str], reports: List[Dict[str, str]]):
    client = LLMClient()
    messages = [
        {"role": "system", "content": f'''You are a pro researcher. Current research topic is:

You will be provide a research topic, research content and goal, and all the resources collected for the research under different category research sub-areas.

Based on the collected literature and data, write an exceptionally detailed and comprehensive analytical report. The report should be lengthy and thorough, with each section fully elaborated to ensure no detail from the literature is overlooked. The analysis must be in-depth, integrating all relevant information from the literature to provide deep-dive insights. Avoid any brevity or superficial summaries. Instead, focus on exhaustive descriptions, nuanced discussions, and detailed interpretations of the findings.

- Mention this report is generated by one-short query from [research topic] by [your AI model name]. 
- Every section is written in a detailed and elaborate manner, with no omission of critical information.
- The analysis integrates all relevant literature, avoiding any gaps or oversights.
- The language is clear, professional, and free of jargon unless necessary.
- The report is structured logically, with each section flowing seamlessly into the next.



---

Research Topic: {research_content}
Collected Literatures: {reports}

---
Report format:

- Use [{Config.REPORT_LANG}]
- Markdown format
- with Key highlighted using ** bold
- Title #, Section ##, Subsection ###


Provide your output in JSON :

```json
{{
research_report_markdown: ""
}}
```

'''}
    ]
    response = client.smart_completion(messages)
    #print(response)
    return response



if __name__ == '__main__':
    # Example usage of translate_to_english
    re = search_advanced("What impact of X platform in 2025")
    print(re)


    