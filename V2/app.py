import os, json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
from dotenv import find_dotenv, load_dotenv
from flask import Flask, request
from functions import main_logic, extract_text_from_pdf, answer_questions, post_to_slack

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Set Slack API credentials
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_BOT_USER_ID = os.environ["SLACK_BOT_USER_ID"]

# Initialize the Slack app
app = App(token=SLACK_BOT_TOKEN)

# Initialize the Flask app
# Flask is a web application framework written in Python
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

def get_bot_user_id():
    try:
        # Initialize the Slack client with your bot token
        slack_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
        response = slack_client.auth_test()
        return response["user_id"]
    except SlackApiError as e:
        print(f"Error: {e}")

@app.event("app_mention")
def handle_mentions(body, say):
    text = body["event"]["text"]

    mention = f"<@{SLACK_BOT_USER_ID}>"
    input_text = text.replace(mention, "").strip()

    # Split the input_text by semicolon to separate the file path and questions
    parts = input_text.split(";")
    if len(parts) < 2:
        say("Please provide a valid file path and questions separated by semicolons.")
        return

    # Extract the file path and questions
    file_path = parts[0].strip()

    if not file_path.startswith("/"):
        file_path = file_path[file_path.find("/"):]  # Remove any leading text before the file path

    questions = ";".join(parts[1:]).strip()

    # Check if the file exists
    if not os.path.isfile(file_path):
        say(f"File not found: {file_path}")
        return

    say("Sure, I'll get right on that!")

    say(file_path)
    pdf_text = extract_text_from_pdf(file_path)

    say("pdf extracted")
    say(pdf_text)

    answers = answer_questions(pdf_text, questions)
    say("received answers")
    results = json.dumps(answers, indent=4)
    # print(results)

    # post_to_slack(f"Question Answers: {results}")

    # response = main_logic(file_path, questions)
    say(results)

    # text = body["event"]["text"]
    #
    # mention = f"<@{SLACK_BOT_USER_ID}>"
    # input_text = text.replace(mention, "").strip()
    #
    # say("Sure, I'll get right on that!")
    # response = main_logic(input_text)
    # say(response)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

# Run the Flask app
if __name__ == "__main__":
    flask_app.run()