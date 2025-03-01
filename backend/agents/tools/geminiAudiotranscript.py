from google import genai
import os
import dotenv
from pydub import AudioSegment
import ffmpeg
from google.genai import types

dotenv.load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def convert_audio_format(audio_file: str) -> str:
    # convert m4a to wav
    audio = AudioSegment.from_file(audio_file, format="m4a")
    audio.export("audio.wav", format="wav")
    return "audio.wav"


def transcribe_audio(audio_file: str) -> str:

    with open(audio_file, 'rb') as f:
        image_bytes = f.read()

    response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=[
        'Transcribe this audio clip entirely word for word',
        types.Part.from_bytes(
        data=image_bytes,
        mime_type='audio/mp3',
        )
    ]
    )

    return response.text


def convert_m4a_to_mp3(input_file_path, output_file_path):
    """
    Convert an M4A file to MP3 format.
    
    Parameters:
    - input_file_path: Path to the M4A file.
    - output_file_path: Path to save the MP3 file.
    """
    try:
        # Load the M4A file
        sound = AudioSegment.from_file(input_file_path)
        
        # Export the audio to MP3 format
        sound.export(output_file_path, format="mp3")
        
        print(f"Conversion successful: {input_file_path} -> {output_file_path}")
    except Exception as e:
        print(f"Error converting file: {e}")


if __name__ == "__main__":
    mp3_file = "/Users/mforce/Desktop/hakuna-matata/KaasDis1.mp3"
    transcription = transcribe_audio(mp3_file)
    print("Transcription:", transcription)
    transcription_file = open("KaasDis1_transcription.md", "+a")
    transcription_file.write(transcription)
    transcription_file.close()




