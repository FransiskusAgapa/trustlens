from dotenv import load_dotenv
from openai import AzureOpenAI
import os

load_dotenv()

def analyze_review(review_text):
    # get the Azure OpenAI API key and endpoint from environment variables
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    model = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    api_version = "2024-02-01"
    
    # create the Azure OpenAI client
    client = AzureOpenAI(
        api_key=api_key, 
        azure_endpoint=endpoint,
        api_version=api_version
    )

    # create the prompt
    message = [
        {"role": "system", "content": """You are a review analyst. Analyze the review and return ONLY a JSON object with exactly these fields:
            - sentiment_label: one of positive, neutral, or negative
            - sentiment_score: decimal between 0 and 1
            - themes: list of exactly 3 short theme labels
            - department_tag: one of compensation, culture, management, growth, or other
            - summary: one sentence summary of the review
            Return only the JSON object, nothing else."""},
        {"role": "user", "content": review_text}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=message,
    )


    # return the response
    return response.choices[0].message.content