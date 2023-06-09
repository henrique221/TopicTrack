# TopicTrack: Automatic Video Summarization

## Description

TopicTrack is a project under development that aims to provide an effective tool for summarizing videos. The idea is that users can upload videos (such as meeting recordings or trainings) and get accurate transcriptions and summaries of these videos. In addition, TopicTrack is capable of creating summaries of specific topics within the video.

## Prerequisites

In order to use TopicTrack, you will need an API key from OpenAI. This is necessary for the text summarization feature of the tool. You can obtain an API key by signing up on the [OpenAI website](https://www.openai.com/).

After obtaining an API key, add it to the `.env` file in the project directory. Set the value of the `OPENAI_API_KEY` variable to your API key:

```
OPENAI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual OpenAI API key.

## Installation and Usage

First of all, make sure you have Python and the required libraries installed on your system.

To use TopicTrack, follow the steps below:

1. Clone this repository on your local machine.
2. Run `execute.sh` (on Linux/macOS) or `execute.bat` (on Windows) in the project directory to set up the environment.
3. Place the audio or video file you want to transcribe and summarize in the `data/media` folder.
4. Run `execute.sh` (on Linux/macOS) or `execute.bat` (on Windows) again to transcribe the media file and generate the summary.

## Contributions

This project is under development and all contributions are welcome. If you find a bug or want to add a new feature, please don't hesitate to open a pull request. We welcome all feedback and contributions.

## Acknowledgements

We appreciate all contributors and users of TopicTrack. Your support is greatly appreciated.

## License
This project is licensed under the [MIT license](https://github.com/henrique221/TopicTrack/blob/main/LICENSE.md).