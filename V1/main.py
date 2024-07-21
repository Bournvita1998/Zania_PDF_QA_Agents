import json
from pdf_processor import extract_text_from_pdf
from question_answering import answer_questions
from slack_bot import post_to_slack

def get_user_inputs():
    pdf_path = input("Please enter the path to the PDF file: ")
    print("Please enter the questions you want to ask. Enter 'done' when you are finished.")
    questions = []
    while True:
        question = input("Enter a question: ")
        if question.lower() == 'done':
            break
        questions.append(question)
    return pdf_path, questions

def main(pdf_path, questions, slack_channel, slack_token):
    pdf_text = extract_text_from_pdf(pdf_path)
    answers = answer_questions(pdf_text, questions)
    results = json.dumps(answers, indent=4)
    print(results)

    post_to_slack(slack_channel, f"Question Answers: {results}", slack_token)

if __name__ == "__main__":
    # Path to the pdf file, please update it to your specific path file
    pdf_path = "/Users/mohitkuri/Desktop/handbook.pdf"  # Example PDF path
    questions = [
        "What is the name of the company?",
        "Who is the CEO of the company?",
        "What is their vacation policy?",
        "What is the termination policy?"
    ]

    # pdf_path, questions = get_user_inputs()
    slack_channel = "#pdf-qa-agent"
    slack_token = "xoxb-7454630468131-7454798843682-fFFdWvCgj351R3aRzX3E5Grd"
    main(pdf_path, questions, slack_channel, slack_token)