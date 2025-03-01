from google import genai
import os
import dotenv
from pydub import AudioSegment
import ffmpeg
from google.genai import types
from datetime import datetime
dotenv.load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))



def transcribe_youtube_video(url: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=f"Transcribe this youtube link: {url}"
        )
        if response.text:
            return response.text
        else:
            raise ValueError("No transcription received from Gemini")
    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        return ""

if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/watch?v=wQA8vi9z5cU&list=PLMbMZz4DZESf3-EtmQ-N6lZh9I6LvI4h-&index=131&ab_channel=OlivierLarose"
    topic = "WebDev"
    yt_transcription_file_name = f"{topic}_transcription_{datetime.now().strftime('%Y-%m-%d')}.md"
    
    # Get the transcription
    yt_transcription = transcribe_youtube_video(youtube_url)
    if not yt_transcription:
        print("Failed to get transcription. Exiting.")
        exit(1)
    
    print("Transcription received successfully")
    
    # Create the topic directory if it doesn't exist
    topic_dir = f"DB/YtTranscripts/{topic}"
    os.makedirs(topic_dir, exist_ok=True)
    
    # Full path to the output file
    output_file = os.path.join(topic_dir, yt_transcription_file_name)
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Transcription for {youtube_url}\n\n")
            f.write(yt_transcription)
        print(f"Successfully wrote transcription to {output_file}")
    except Exception as e:
        print(f"Error writing to file: {str(e)}")





