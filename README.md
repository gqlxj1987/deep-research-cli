# Deep Research CLI

A command-line python tool for conducting comprehensive research on any topic using AI and advanced search capabilities. This tool automates the research process by generating structured research plans, executing targeted searches, and producing detailed reports in multiple formats similar to 'ChatGPT Deep Research'

> !!!!! THIS PROJECT IS UNDER VERY EARLY STAGE OF DEVELOPMENT. NOTHING IS GUARANTEED WORKING. :)

## Features

![](https://cdn.sa.net/2025/02/09/3UPtxEc6eDK4RvA.png)

- **Multi-language Support**: Research topics can be input in any language
- **Automated Research Planning**: Generates comprehensive research plans with categorized queries
- **Advanced Search Integration**: Utilizes Tavily Search API for high-quality search results
- **Multiple Report Formats**:
  - Detailed Research Reports
  - Concise Research Summaries
  - WeChat Article Format
- **Flexible Model Selection**: Supports various AI models for report generation
- **Structured Output**: Organizes research results and reports in a clear directory structure

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/deep-research-cli.git
   cd deep-research-cli
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` file and add your API keys:
   ```
   OPENAI_KEY=your_openai_api_key
   OPENAI_BASE=your_openai_api_base_url
   TAVILY_API_KEY=your_tavily_api_key
   ```

## Usage

### Starting New Research

```bash
# Create a new research project
python main.py --topic "Impact of AI on healthcare in 2024"
```

### Generating Reports from Existing Research

```bash
# Generate a detailed report from existing research
python main.py --research-id RS_20240214_123456 --report-method generate_research_report_detailed

# Generate a WeChat article
python main.py --research-id RS_20240214_123456 --report-method generate_wechat_article
```

### Command Line Arguments

- `--topic, -t`: Research topic in any language
- `--research-id, -r`: ID of existing research to load
- `--model, -m`: Model to use for report generation (default: deepseek/deepseek-r1)
- `--report-method, -p`: Report generation method to use
  - `generate_research_report`: Basic research report
  - `generate_research_report_detailed`: Detailed research report
  - `generate_wechat_article`: WeChat article format

## Research Process

1. **Topic Analysis**: Translates and analyzes the research topic
2. **Plan Generation**: Creates a structured research plan with categories and queries
3. **Data Collection**: Executes searches for each query and category
4. **Report Generation**: Processes collected data into comprehensive reports
5. **Reference Management**: Generates reference links for all sources

## Output Structure

All the progress data will be saved in output folder. Including searching literature, searching results, and generated reports.

```
output/
└── RS_[DATE]_[TIME]/
    ├── RS_[DATE]_[TIME]_meta.json       # Research metadata
    ├── [CATEGORY]/                      # Category-specific results
    │   └── [QUERY].json                 # Search results
    ├── [CATEGORY]_report.json           # Category reports
    ├── RS_[DATE]_[TIME]_reference.md    # Reference links
    └── RS_[DATE]_[TIME]_[MODEL]_[TYPE].md  # Generated reports
```

## Configuration (.env.example)

```
# Madantory Variables
# 1. LLM Model settings, openrouter is recommanded since it integrates multiple model providers.
OPENAI_KEY=
OPENAI_BASE=https://openrouter.ai/api/v1

# 2. Tavily API Token
TAVILY_API_KEY=

# Optional Variables

# a. LLM Model Choice, refer config.py for default settings. 
# SMART_MODEL = "deepseek/deepseek-r1"
# NORMAL_MODEL = "deepseek/deepseek-r1-distill-llama-70b"
# LONG_MODEL = "google/gemini-2.0-flash-001"
# REPORT_MODEL = "google/gemini-2.0-pro-exp-02-05:free"

# b. Log Level in Console, default INFO
# DEEP_RESEARCH_LOG_LEVEL=INFO

# c. Language use to create reports. Default = Chinese. Used in Prompt so just english words.
# REPORT_LANG=Chinese
```

## Research Cost Estimation

> !!!!!! A LOT ROOM FOR OPTIMIZATION

- LLM Cost: $0.1 / Research (default, you can always change to free models)
- Tavily Search: 100 Credit / Research = $0.8 (Tavily provide 1000 free credits per month)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.