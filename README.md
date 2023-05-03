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

First of all, make sure you have Docker installed on your system.

To use TopicTrack, you will first need to place the video transcription into the text.txt file in the data folder.

To build and run the Docker container, follow the steps below:

1. Clone this repository on your local machine.
2. In the project directory, build the Docker image using the provided Dockerfile:

```bash
docker build -t topictrack .
```

3. After building the image, you can start the container using the `docker run` command. To use the provided docker-compose.yml file, you can also use the `docker-compose up` command:

```bash
TITLE=ExampleTitle docker-compose up
```

Replace "ExampleTitle" with the title of your video.

## Contributions

This project is under development and all contributions are welcome. If you find a bug or want to add a new feature, feel free to create an issue or a pull request.

## Contact

If you have any questions or suggestions, please contact us.

## Acknowledgements

We appreciate all contributors and users of TopicTrack. Your support is greatly appreciated.

## License
This project is licensed under the MIT license.
