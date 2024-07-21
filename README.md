# PDF QA Agent

## Problem Statement

Create an AI agent that leverages the capabilities of a large language model. This agent should be able to extract answers based on the content of a large PDF document and post the results on Slack. Ideally, use OpenAI LLMs. If using the Langchain or LLama Index framework to implement this functionality, avoid pre-built chains and implement the logic yourself. Ensure the code is production-grade and maintainable.

## User Journey

1. **Input the PDF**: Provide the path to the PDF file.
2. **Input the Questions**: List the questions you want answered.
3. **Interact with the Agent**: Ask the agent to "Answer the questions and post results on Slack."

## Input Requirements

You need to provide two inputs:
- A list of questions.
- A PDF file containing the document over which the questions will be answered.

## Ideal Output Format

- The output should be a structured JSON blob that pairs each question with its corresponding answer.
- Answers should match word-for-word if the question is a direct match.
- If the answer is of low confidence, respond with “Data Not Available.”

## Solution

The project includes two versions: **v1** and **v2**.

### Version 1 (v1)

1. **Installation**:
   - Install the required dependencies:
     ```bash
     pip install -r requirements.txt
     ```

2. **Configuration**:
   - Update the path to the PDF file and questions in the `main.py` file.
   - Set the Slack channel and token in the same file.

3. **Execution**:
   - Run the script with:
     ```bash
     python3 main.py
     ```

4. **Results**:
   - You will see the appropriate responses in your Slack channel.

### Version 2 (v2)

1. **Installation**:
   - Install the required dependencies:
     ```bash
     pip install -r requirements.txt
     ```

2. **Configuration**:
   - Set up Slack by creating an app and obtaining the necessary tokens and signing secrets.

3. **Execution**:
   - Start the Flask server:
     ```bash
     python app.py
     ```
   - Use `ngrok` to expose your local server:
     ```bash
     ngrok http 5000
     ```

4. **Interaction**:
   - Mention the bot in Slack with details formatted as `path; q1; q2; q3` to get answers to your questions.

5. **Video Tutorial**:
   - [Detailed explanation and Slack setup video](link-to-video)