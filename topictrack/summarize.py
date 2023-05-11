import openai
import json
import sys
import os
import re
import glob
import subprocess
import warnings
import yt_dlp
import tempfile
from moviepy.editor import *

from dotenv import load_dotenv
from rich import print
from rich.console import Console
from tqdm import tqdm
from summarizer import Summarizer
from transformers import logging

console = Console()

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')  # Insert your API key here

def split_text(text, max_length=2000):
    """Splits the text into smaller parts."""
    words = text.split()
    parts = []
    current_part = []

    for word in words:
        current_part.append(word)
        if len(" ".join(current_part)) > max_length:
            parts.append(" ".join(current_part[:-1]))
            current_part = [word]

    if current_part:
        parts.append(" ".join(current_part))

    return parts

def save_summary(file_path, summary):
    summary_dir = os.path.join("data", "summaries")
    os.makedirs(summary_dir, exist_ok=True)

    file_base, _ = os.path.splitext(os.path.basename(file_path))
    summary_file_path = os.path.join(summary_dir, f"{file_base}_summary.txt")

    with open(summary_file_path, "a") as f:
        if os.stat(summary_file_path).st_size > 0:  # If the file is not empty
            f.write("\n\n")  # Add two blank lines to separate summaries
        f.write(summary)

    print(f"Summary saved to: {summary_file_path}")


def summarize_text(file_path):
    option = console.input(f'\nDo you wish to have a ...\nSummarize (S)\nImportant topics (I)\n').lower()

    if(option != 's' and option != 'i'):
        console.print(f'\n[bold red]You need to choose an option:\n[/bold red]')
        summarize_text(file_path)

    with open(file_path, 'r') as f:
        text = f.read()

    title = console.input('\n[bold]Title of the video (optional):[/bold] ')

    total_words = len(text)
    print(f"Words count: {total_words}")

    if(total_words > 3900):
        text = split_transcription(text, title, openai_api_key)
    """Generates a summary of the text using the OpenAI API."""
    openai.api_key = openai_api_key

    if(option == 's'):
        custom = 'Faça um resumo detalhado em português brasileiro sobre o seguinte, começe com Em resumo nessa transcrição:'
    elif(option == 'i'):
        custom = 'cite alguns tópicos importantes sobre o seguinte texto e explique cada topico'

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{custom}\nTitulo:{title}\n\n{text}\n",
        temperature=0.3,
        max_tokens=1500,
    )
    summary = response.choices[0].text.strip()

    save_summary(file_path, summary)

    return summary

def summarize_text_part(text):
    warnings.filterwarnings("ignore", category=UserWarning, module="transformers")
    warnings.simplefilter(action='ignore', category=FutureWarning)
    logging.set_verbosity_error()

    model = Summarizer()
    summary = model(text, num_sentences=3)
    return summary

def continue_summary(text, api_key):
    """Continues a summary of the text using the OpenAI API."""
    openai.api_key = api_key

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{text}\n\nContinue",
        temperature=0.3,
        max_tokens=1000,
    )
    return response.choices[0].text.strip()

def split_transcription(text, title, api_key):
    """Creates a request for the OpenAI API from the text and the title."""
    text_with_title = f"Titulo: {title}\n\n{text}"
    chunks = split_text(text_with_title)
    summaries = []
    total_words = 0
    remaining = len(chunks)

    console.print("Please wait while we are summarizing the text...")
    for i, chunk in tqdm(enumerate(chunks, start=1), total=len(chunks), desc="Summarizing"):
        summary = summarize_text_part(chunk)
        total_words += len(summary.split())
        summaries.append(summary)
        remaining = remaining - 1
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

def finish(summarized_transcription_json_formatted, file_path):
    end = console.input("\n[bold cyan]Continue Y | New transcription P [/bold cyan]").lower()

    if end == "y":
        summary = continue_summary(summarized_transcription_json_formatted, openai_api_key)
        console.print(f"\n[bold magenta]Continue:[/bold magenta]\n\n{summary}\n")
        save_summary(file_path, summary)
        finish(summarized_transcription_json_formatted, file_path)

    elif end == "p":
        main()

def list_txt_files(path):
    txt_files = []
    summaries_path = os.path.join(path, "summaries")

    for root, _, files in os.walk(path):
        if root != summaries_path:
            for file in files:
                if file.endswith('.txt'):
                    txt_files.append(os.path.join(root, file))
    return txt_files

def choose_text_file():
    """Choose a text file from the data directory and its subdirectories."""
    media_path = 'data'

    if not os.path.exists(media_path):
        print(f"The directory '{media_path}' does not exist.")
        return

    files = list_txt_files(media_path)
    if not files:
        print(f"\nThere are no text files in the '{media_path}' directory or its subdirectories.\n[cyan]Please add your text files first[/cyan]\n")
        return

    print("Available files:")
    for i, f in enumerate(files):
        print(f"{i + 1}. {f}")

    file_choice = int(input("\nChoose a file by number: ")) - 1
    chosen_file = files[file_choice]

    return chosen_file

def first_choice():
    option = console.input('\n\n[bold][cyan]Do you wish to[/cyan]\n\n[cyan]Transcript a media (M)\nSummarize a text (T)[/cyan]\n[/bold]').lower()
    if(option != 't' and option != 'm'):
        return
    return option

def ask_for_language():
    console.print("[bold cyan]Enter the language you want to use for processing the video (e.g., Portuguese, English, Russian):[/bold cyan]")
    language = input().strip()
    return language

def sanitize_filename(filename):
    # Remove espaços e caracteres especiais, mantendo letras, números, hífens e sublinhados
    return re.sub(r'[^a-zA-Z0-9_\-]+', '', filename.replace(' ', '_'))

def download_video(video_url):
    if not video_url:
        return 'URL do vídeo não fornecida', 400

    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(tempfile.gettempdir(), '%(title)s.%(ext)s'),
            'noplaylist': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            video_file_path = ydl.prepare_filename(info)

        # Converter vídeo em áudio usando moviepy
        video = VideoFileClip(video_file_path)
        unsanitized_audio_filename = os.path.splitext(os.path.basename(video_file_path))[0] + '.mp3'
        sanitized_audio_filename = sanitize_filename(unsanitized_audio_filename) + '.mp3'  # Adiciona a extensão .mp3

        output_dir = "data/media"
        os.makedirs(output_dir, exist_ok=True)  # Cria o diretório de saída se não existir
        audio_file_path = os.path.join(output_dir, sanitized_audio_filename)

        video.audio.write_audiofile(audio_file_path, codec='mp3', ffmpeg_params=["-f", "mp3"])  # Especifique o codec 'mp3' e o formato 'mp3'

        # Remover o arquivo de vídeo
        os.remove(video_file_path)

        console.print(f'\n\nCAMINHO DO AUDIO\n\n')
        print(audio_file_path)
        return audio_file_path
    except Exception as e:
        return f'Erro ao baixar o vídeo e converter em áudio: {str(e)}', 500


def get_video_url():
    console.print("[bold cyan]Enter the YouTube video URL you want to download and convert to audio:[/bold cyan]")
    video_url = input().strip()
    return video_url

def main():
    console.print("\n[bold green]Welcome to the TopicTrack Video Summarizer![/bold green]")
    console.print("[cyan]Please enter the following information:[/cyan]")

    option = first_choice()
    file_path = ''

    if(not option):
        console.print(f"\n[bold red]You must choose an option[/bold red]\n")
        main()
    elif(option == 'm'):
        video_path = choose_video_file()
        if(not video_path):
            return
        result = video_path
        console.print(f"\n[bold cyan]Filepath:[/bold cyan]\n[magenta]{file_path}[/magenta]\n")

    elif(option == 't'):
        file_path = choose_text_file()
        summarized_transcription = summarize_text(file_path)

        pattern = re.compile(r'\n(\d?)')
        summarized_transcription_json_formatted = pattern.sub(replace_newline, summarized_transcription)

        console.print(f"\n[bold magenta]Result:[/bold magenta]\n\n{summarized_transcription_json_formatted}\n")

        finish(summarized_transcription_json_formatted, file_path)
    elif(option == 'd'):
        video_url = get_video_url()
        result = download_video(video_url)
        if isinstance(result, tuple):  # Se houver um erro
            console.print(f"\n[bold red]Error:[/bold red]\n[magenta]{result[0]}[/magenta]\n")
        else:
            console.print(f"\n[bold cyan]Audio file downloaded successfully.[/bold cyan]\n")
    
    if result :
        language = ask_for_language()
        file_path = run_whisper_command(result, language=language)
        console.print(f"\n[bold cyan]Filepath:[/bold cyan]\n[magenta]{file_path}[/magenta]\n")

        summarized_transcription = summarize_text(file_path)

        pattern = re.compile(r'\n(\d?)')
        summarized_transcription_json_formatted = pattern.sub(replace_newline, summarized_transcription)

        console.print(f"\n[bold magenta]Result:[/bold magenta]\n\n{summarized_transcription_json_formatted}\n")

    finish(summarized_transcription_json_formatted, file_path)

def first_choice():
    console.print("[bold cyan]Choose an option:[/bold cyan]")
    console.print("[bold cyan]m - Choose a video file from your computer[/bold cyan]")
    console.print("[bold cyan]t - Choose a text file from your computer[/bold cyan]")
    console.print("[bold cyan]d - Download and convert a YouTube video to audio[/bold cyan]")
    console.print("[bold cyan]Enter 'm', 't', or 'd':[/bold cyan]")
    return input().strip().lower()




if __name__ == "__main__":
    main()

