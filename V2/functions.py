import fitz
import json
import os

from openai import OpenAI
from typing import List, Dict
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import find_dotenv, load_dotenv

client = OpenAI(
    api_key="sk-proj-yHmOlgFMZYrd6a0kOjl6T3BlbkFJBLnwoXqlC5Lnntf3kfil",
)

# Load environment variables from .env file
load_dotenv(find_dotenv())
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

def main_logic(pdf_path, questions):

    pdf_text = extract_text_from_pdf(pdf_path)
    answers = answer_questions(pdf_text, questions)
    results = json.dumps(answers, indent=4)
    print(results)

    post_to_slack(f"Question Answers: {results}")

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def chat_gpt(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def split_text_into_chunks(text: str, chunk_size: int = 15000) -> List[str]:
    # Split the text into chunks of specified size
    chunks = []
    while len(text) > chunk_size:
        # Find the last space within the chunk size to avoid splitting words
        split_index = text.rfind(' ', 0, chunk_size)
        if split_index == -1:
            split_index = chunk_size
        chunks.append(text[:split_index])
        text = text[split_index:]
    chunks.append(text)
    return chunks

def answer_questions(pdf_text: str, questions: List[str]) -> Dict[str, str]:
    # Initialize a dictionary to store the responses
    responses = {}

    # Split the pdf_text into manageable chunks
    chunks = split_text_into_chunks(pdf_text)

    # Iterate over each question
    for question in questions:
        # Initialize an empty answer
        full_answer = ""

        # Process each chunk with the question
        for chunk in chunks:
            # Prepare the prompt by combining the chunk and the question
            prompt = f"Context:\n{chunk}\n\nQuestion: {question}\nAnswer:"

            # Get the answer using the chat_gpt function
            try:
                answer = chat_gpt(prompt)
                full_answer += answer + " "
            except Exception as e:
                # Handle any errors that occur
                full_answer += f"Error: {e} "

        # Store the complete answer in the responses dictionary
        # gpt-3.5-turbo-0125 model does not provide a confidence score hence using this heuristic approach
        if len(full_answer) < 10 or "I don't know" in full_answer or "not sure" in full_answer:
            responses[question] = "Data Not Available"
        else:
            responses[question] = full_answer.strip()

    return responses

def post_to_slack(text: str):
    channel ="#pdf-qa-agent"
    token = SLACK_BOT_TOKEN

    client = WebClient(token=token)
    try:
        response = client.chat_postMessage(channel=channel, text=text)
    except SlackApiError as e:
        assert e.response["error"]