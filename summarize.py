import openai
import json
import sys
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY') # Insert your API key here

def split_text(text, n=1000):
    """Splits the text into smaller parts with at most n words."""
    words = text.split()
    return [" ".join(words[i : i + n]) for i in range(0, len(words), n)]

def summarize_text(text):
    """Generates a summary of the text using the OpenAI API."""
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{text}\n\nSummary:",
        temperature=0.3,
        max_tokens=400,
    )
    return response.choices[0].text.strip()

def create_api_request(text, title):
    """Creates a request for the OpenAI API from the text and the title."""
    text_with_title = f"Title: {title}\n\n{text}"
    chunks = split_text(text_with_title)
    summaries = []
    total_words = 0

    for remaining, chunk in enumerate(chunks, start=1):
        print(f"Please wait while we are summarizing the text... {remaining} parts remaining")
        summary = summarize_text(chunk)
        total_words += len(summary.split())
        summaries.append(summary)

        if total_words > 3500:
            break

    content = " ".join(summaries)
    """If you want to build a api request, uncomment the line below"""
#     request = {"role": "user", "content": content}
    return content

def read_input_file_and_title():
    """Reads the text file and the title from the command line arguments."""
    if len(sys.argv) < 3:
        print('Error: title and input file path not provided.')
        sys.exit(1)

    with open(sys.argv[1], "r") as file:
        text = file.read()

    title = sys.argv[2]
    return text, title

def main():
    text, title = read_input_file_and_title()
    api_request = create_api_request(text, title)
    api_request_json = json.dumps(api_request, ensure_ascii=False, indent=2)
    print(f"Request:\n{api_request_json}\n")

if __name__ == "__main__":
    main()
