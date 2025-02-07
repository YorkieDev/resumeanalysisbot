# Resume Analysis Bot

A resume analysis bot that extracts text from a PDF resume and uses a custom LLM (powered by your LM Studio server) to provide detailed, expert feedback. The bot acts as a seasoned career advisor—identifying key skills, highlighting strengths and weaknesses, and providing actionable suggestions for improvement. After the initial analysis, you can ask follow-up questions to get further advice on how to improve the resume.

## Features

- **PDF Text Extraction:** Uses [pdfminer.six](https://github.com/pdfminer/pdfminer.six) to extract resume text from PDF files.
- **LLM Integration:** Leverages a custom LLM class that interacts with your LM Studio server API.
- **Prompt Template:** Uses [LangChain](https://github.com/hwchase17/langchain) to structure the input prompt.
- **Interactive Follow-Up:** Allows you to ask follow-up questions about resume improvements after the initial analysis.
- **Modular & Modern Pipeline:** Formats prompts and directly invokes the LLM, avoiding deprecated classes.

## Prerequisites

- Python 3.7 or higher (tested on Python 3.12)
- An operational LM Studio server with an available API endpoint.
- A PDF resume to analyze.

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/YorkieDev/resumeanalysisbot/
    cd resume-analysis-bot
    ```

2. **Create a Virtual Environment (Recommended):**

    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3. **Install Dependencies:**

    Create a `requirements.txt` file with the following content:

    ```txt
    requests
    pdfminer.six
    langchain
    ```

    Then, install them using:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Configure the Bot:**

   Open `resume_analysis_bot.py` and update the configuration variables in the `main()` function if needed:

   - **API_URL:** The URL of your LM Studio server API endpoint.
   - **MODEL_NAME:** The model name you wish to use.

2. **Run the Bot:**

    ```bash
    python resume_analysis_bot.py
    ```

3. **Follow the Prompts:**

   - When prompted, enter the full path to the resume PDF (e.g., `C:\Users\YourName\Documents\YourCV.pdf`).
   - The bot will extract and analyze the resume, then display detailed feedback.
   - After the analysis, you can choose to ask follow-up questions to get further improvement advice.

## Contributing

Contributions are welcome! If you have suggestions or improvements, please open an issue or submit a pull request.
