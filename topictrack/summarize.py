import openai
import json
import sys
import os
import re
import glob
import subprocess

from dotenv import load_dotenv
from rich import print
from rich.console import Console

console = Console()

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')  # Insert your API key here

def split_text(text, n=800):
    """Splits the text into smaller parts with at most n words."""
    words = text.split()
    return [" ".join(words[i : i + n]) for i in range(0, len(words), n)]

def summarize_text(text, title, api_key):
    """Generates a summary of the text using the OpenAI API."""
    openai.api_key = api_key

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Titulo:{title}\n\n{text}\n\nFaça um resumo detalhado em português brasileiro sobre essa transcrição, cite alguns tópicos importantes e explique cada um.",
        temperature=0.3,
        max_tokens=500,
    )
    return response.choices[0].text.strip()

def summarize_text_part(text, api_key):
    """Generates a summary of the text using the OpenAI API."""
    openai.api_key = api_key

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{text}\n\nFaça um resumo.",
        temperature=0.3,
        max_tokens=500,
    )
    return response.choices[0].text.strip()


def continue_summary(text, api_key):
    """Continues a summary of the text using the OpenAI API."""
    openai.api_key = api_key

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{text}\n\nContinue",
        temperature=0.3,
        max_tokens=500,
    )
    return response.choices[0].text.strip()

def split_transcription(text, title, api_key):
    """Creates a request for the OpenAI API from the text and the title."""
    text_with_title = f"Titulo: {title}\n\n{text}"
    chunks = split_text(text_with_title)
    summaries = []
    total_words = 0

    for remaining, chunk in enumerate(chunks, start=1):
        print(f"Please wait while we are summarizing the text... {remaining} parts remaining")
        summary = summarize_text_part(chunk, api_key)
        total_words += len(summary.split())
        summaries.append(summary)

        if total_words > 3500:
            break

    content = " ".join(summaries)
    return content

def replace_newline(match):
    newline = os.linesep
    digit = match.group(1) if match.group(1) else ''
    return f'{newline}{digit}'

def choose_video_file():
    """Choose a video file from the data/media directory."""
    media_path = 'data/media'

    if not os.path.exists(media_path):
        print(f"The directory '{media_path}' does not exist.")
        return

    files = [f for f in os.listdir(media_path) if os.path.isfile(os.path.join(media_path, f))]
    if not files:
        print(f"\nThere are no files in the '{media_path}' directory yet.\n[cyan]Please add your media in 'data/media directory' first[/cyan]\n")
        return

    print("Available files:")
    for i, f in enumerate(files):
        print(f"{i + 1}. {f}")

    file_choice = int(input("\nChoose a file by number: ")) - 1
    chosen_file = files[file_choice]

    return os.path.join(media_path, chosen_file)

def run_whisper_command(chosen_video_path, language="Portuguese", output_dir="data", verbose=False):
    """Run the whisper command to process the video."""
    if not os.path.isfile(chosen_video_path):
        print(f"The file '{chosen_video_path}' does not exist.")
        return

    output_name = os.path.splitext(os.path.basename(chosen_video_path))[0]
    output_path = os.path.join(output_dir, output_name)
    output_file = os.path.join(output_path, f"{output_name}.txt")

    os.makedirs(output_path, exist_ok=True)

    command = f"whisper {chosen_video_path} --language {language} --output_dir {output_path} --verbose {verbose}"

    try:
        subprocess.run(command, shell=True, check=True)
        print("Whisper command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the Whisper command: {e}")

    return output_file

def finish(summarized_transcription_json_formatted):
    end = console.input("\n[bold cyan]Continue Y | New transcription P [/bold cyan]").lower()

    if end == "y":
        summary = continue_summary(summarized_transcription_json_formatted, openai_api_key)
        console.print(f"\n[bold magenta]Continue:[/bold magenta]\n\n{summary}\n")
        finish(summarized_transcription_json_formatted)

    elif end == "p":
        main()

def main():
    console.print("\n[bold green]Welcome to the TopicTrack Video Summarizer![/bold green]")
    console.print("[cyan]Please enter the following information:[/cyan]")

    video_path = choose_video_file()
    if(not video_path):
        return

    file_path = run_whisper_command(video_path)

    console.print(f"\n[bold cyan]Filepath:[/bold cyan]\n[magenta]{file_path}[/magenta]\n")

    title = console.input('[bold]Title of the video (optional):[/bold] ')

    with open(file_path, 'r') as f:
        text = f.read()

    total_words = len(text)
    print(f"Quantidade de palavras: {total_words}")

    if(total_words > 3900):
        text = split_transcription(text, title, openai_api_key)

    summarized_transcription = summarize_text(text, title, openai_api_key)

    pattern = re.compile(r'\n(\d?)')
    summarized_transcription_json_formatted = pattern.sub(replace_newline, summarized_transcription)

    console.print(f"\n[bold magenta]Result:[/bold magenta]\n\n{summarized_transcription_json_formatted}\n")

    finish(summarized_transcription_json_formatted)

if __name__ == "__main__":
    main()

