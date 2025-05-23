from pydub import AudioSegment
import os

def concat_audio_files(input_files, output_file):
    """
    Concatenate multiple audio files into a single file
    
    Args:
        input_files (list): List of paths to input audio files
        output_file (str): Path to save the concatenated audio file
    """
    for file in input_files:
        if not os.path.exists(file):
            raise FileNotFoundError(f"Input file not found: {file}")
    
    combined = AudioSegment.from_mp3(input_files[0])
    
    for file in input_files[1:]:
        audio = AudioSegment.from_mp3(file)
        combined += audio
    
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    combined.export(output_file, format="mp3")
    print(f"Successfully created {output_file}")

if __name__ == "__main__":
    input_files = ["./audio/hello.mp3", "./audio/goodbye.mp3"]
    
    output_file = "./output.mp3"
    
    concat_audio_files(input_files, output_file)
