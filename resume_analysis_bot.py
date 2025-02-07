"""
resume_analysis_bot.py

A resume analysis bot that extracts text from a PDF resume and uses a custom LLM (powered by your LM Studio server)
to provide detailed, expert feedback. After the initial analysis, the bot allows you to ask follow-up questions to
further refine the advice on how to improve the resume.

Usage:
    python resume_analysis_bot.py
"""

import os
import requests
from typing import Optional

from langchain.llms.base import LLM
from langchain.prompts import PromptTemplate
from pdfminer.high_level import extract_text


# ------------------------------
# Custom LLM Class
# ------------------------------
class CustomLLM(LLM):
    api_url: str
    model_name: str
    temperature: float = 0.7

    def __init__(self, api_url: str, model_name: str, temperature: float = 0.7, **kwargs):
        """
        Initialize the CustomLLM with API details and model parameters.
        Delegates field assignment to Pydantic's BaseModel.

        :param api_url: URL of the LM Studio server API.
        :param model_name: Name of the model to use.
        :param temperature: Sampling temperature for response variability.
        """
        super().__init__(api_url=api_url, model_name=model_name, temperature=temperature, **kwargs)

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[list[str]] = None) -> str:
        """
        Send a prompt to the LM Studio server and retrieve the response.

        :param prompt: The prompt string.
        :param stop: Optional list of stop tokens.
        :return: The response from the LM Studio server.
        """
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": "You are a seasoned career advisor and resume expert."},
                {"role": "user", "content": prompt}
            ],
            "temperature": self.temperature,
            "max_tokens": 1000,
            "stream": False
        }
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            return f"Network or request error: {e}"

        response_json = response.json()
        # Return the feedback text from the LM's response
        return response_json.get('choices', [{}])[0].get('message', {}).get('content', "No valid response.")

    def __call__(self, prompt: str) -> str:
        """Allow calling the LLM instance directly like a function."""
        return self._call(prompt)


# ------------------------------
# Utility Functions
# ------------------------------
def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text content from a PDF file.

    :param pdf_path: Path to the PDF file.
    :return: Extracted text as a string.
    """
    return extract_text(pdf_path)


def run_analysis(api_url: str, model_name: str, pdf_path: str) -> None:
    """
    Run the resume analysis process: extract text from the PDF, send it to the LLM for analysis,
    display feedback, and allow follow-up questions for further improvements.

    :param api_url: URL of the LM Studio server API.
    :param model_name: Name of the model to use.
    :param pdf_path: Path to the resume PDF.
    """
    # Validate file existence
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return

    try:
        resume_text = extract_text_from_pdf(pdf_path)
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return

    if not resume_text.strip():
        print("No text extracted from PDF.")
        return

    # Display a preview of the extracted text (first 500 characters)
    print("\nExtracted Resume Text Preview:\n")
    preview = resume_text[:500] + "..." if len(resume_text) > 500 else resume_text
    print(preview)

    # Define a prompt template for resume analysis
    resume_prompt = PromptTemplate(
        input_variables=["resume_text"],
        template=(
            "You are a seasoned career advisor and resume expert. Analyze the resume provided below and perform the following tasks:\n"
            "1. Identify the candidate's key skills and competencies.\n"
            "2. Highlight the strengths and areas for improvement in the resume.\n"
            "3. Provide actionable suggestions for formatting, content, and clarity enhancements.\n\n"
            "Resume:\n{resume_text}\n\n"
            "Please provide your analysis in a clear and concise manner."
        )
    )

    # Format the prompt using the extracted resume text
    formatted_prompt = resume_prompt.format(resume_text=resume_text)

    # Instantiate the custom LLM and get the analysis feedback
    llm = CustomLLM(api_url=api_url, model_name=model_name, temperature=0.7)
    print("\nAnalyzing resume with the language model...\n")
    feedback = llm(formatted_prompt)

    print("Model Feedback:\n")
    print(feedback)

    # ------------------------------
    # Follow-Up Question Loop
    # ------------------------------
    followup_template = PromptTemplate(
        input_variables=["analysis", "question"],
        template=(
            "You are a seasoned career advisor and resume expert. The following is the previous analysis of a candidate's resume:\n"
            "{analysis}\n\n"
            "Now, the candidate has a follow-up question: {question}\n\n"
            "Please provide detailed, actionable suggestions on how to improve the resume based on this question."
        )
    )

    while True:
        user_choice = input("\nWould you like to ask a follow-up question regarding resume improvements? (yes/no): ").strip().lower()
        if user_choice not in ['yes', 'y']:
            break
        question = input("Enter your follow-up question: ").strip()
        if not question:
            print("No question entered. Exiting follow-up.")
            break
        formatted_followup = followup_template.format(analysis=feedback, question=question)
        print("\nProcessing your follow-up question...\n")
        followup_response = llm(formatted_followup)
        print("Follow-Up Advice:\n")
        print(followup_response)


def main():
    """
    Main entry point for the resume analysis bot.
    """
    # ------------------------------
    # Configuration
    # ------------------------------
    # Update these with your LM Studio server details as needed.
    API_URL = "http://localhost:1234/v1/chat/completions"
    MODEL_NAME = "mistral-nemo-instruct-2407"

    # ------------------------------
    # User Input
    # ------------------------------
    pdf_path = input("Enter the path to the resume PDF: ").strip().strip('"')
    run_analysis(api_url=API_URL, model_name=MODEL_NAME, pdf_path=pdf_path)


if __name__ == "__main__":
    main()
