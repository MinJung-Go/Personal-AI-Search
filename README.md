# Personal-AI-Search 
- "Less is More! There is no agent framework at all; only individual simple API call methods."

## Project Overview
Personal Agentic search assistant based on GPT-4o and DeepSeek-R1. This project aims to provide a powerful and flexible search assistant that leverages advanced AI models to enhance search capabilities.

## Project Structure
```
Personal-AI-Search/
├── README.md
├── LICENSE
├── requirements.txt
├── app/
│   ├── api/
│   │   ├── app.py
│   │   ├── api.py
│   │   └── main.py
├── config/
│   ├── __init__.py
│   ├── prompts.py
│   └── setting.py
├── core/
│   ├── agents/
│   │   ├── __init__.py
│   │   └── base.py
│   ├── llm/
│   │   ├── __init__.py
│   │   └── llm.py
│   └── tools/
│       ├── __init__.py
│       └── web_search.py
├── utils/
│   ├── log_utils.py
│   └── utils.py
└── .gitignore
```
## Module Introduction
- **app**: Contains the main application logic and API interfaces.
  - **api**: Provides API endpoints and routing.
    - **app.py**: Entry point of the application.
    - **api.py**: Defines API routes and handling logic.
    - **main.py**: Core API logic.
- **config**: Contains configuration files and settings.
  - **__init__.py**: Initializes the config module.
  - **prompts.py**: Defines various prompts and messages.
  - **setting.py**: Application configuration settings.
- **core**: Contains core functionalities and logic.
  - **agents**: Agent modules.
    - **__init__.py**: Initializes the agents module.
    - **base.py**: Base agent class.
  - **llm**: Language model-related logic.
    - **__init__.py**: Initializes the LLM module.
    - **llm.py**: Implementation of language models.
  - **tools**: Various utility tools.
    - **__init__.py**: Initializes the tools module.
    - **web_search.py**: Web search tool.
- **utils**: Contains utility functions and helpers.
  - **log_utils.py**: Logging utilities.
  - **utils.py**: General utility functions.
- **.gitignore**: List of ignored files.

## Usage Instructions
### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/Personal-AI-Search.git 
   cd Personal-AI-Search
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure settings:
   - Edit the `config/setting.py` file to configure application settings.

### Running the Project
1. Start the application:
   ```bash
   chainlit run app/api/app.py -w --port 5000
   ```
2. Access API endpoints:
   - By default, the Web Demo runs at `http://localhost:5000`.

![20250221-154211.jpg](https://img.picui.cn/free/2025/02/21/67b82e8bc2d27.jpg)
