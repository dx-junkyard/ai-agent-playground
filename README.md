# jhjcpishva/learn-devin

This is a learning repository for working with audio files using Python.

## What to achieve?

- This repo would need to achieve to use python `pydub` library and able to run on docker container.
- Please make `Dockerfile` for python3.12 with ffmpeg available.
- Please make `main.py` for sample script. Achieve to concat `./audio/hello.mp3` and `./audio/goodbye.mp3` and output as `./output.mp3`
- Update README.md by adding section of "## Example" with content "explaining how to use `main.py`"

## Example

### Running with Python

To run the script directly with Python:

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the script:
   ```
   python main.py
   ```

The script will concatenate `./audio/hello.mp3` and `./audio/goodbye.mp3` and save the result as `./output.mp3`.

### Running with Docker

To run the script using Docker:

1. Build the Docker image:
   ```
   docker build -t audio-concat .
   ```

2. Run the container:
   ```
   docker run -v $(pwd):/app audio-concat
   ```

This will mount your current directory to the container and run the script, creating the `output.mp3` file in your local directory.

