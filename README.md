# TopicTrack: Automatic Video Summarization by Leroy Merlin Brazil

## Description

TopicTrack is a project under development by Leroy Merlin Brazil that aims to provide an effective tool for summarizing videos. The idea is that users can upload videos (such as meeting recordings or trainings) and get accurate transcriptions and summaries of these videos. In addition, TopicTrack is capable of creating summaries of specific topics within the video.

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

We appreciate all contributors and users of TopicTrack. Your support is greatly appreciated. Thanks to Leroy Merlin Brazil for supporting this project.