# Start by making sure the `assemblyai` package is installed.
# If not, you can install it by running the following command:
# pip install -U assemblyai
#
# Note: Some macOS users may need to use `pip3` instead of `pip`.

import assemblyai as aai
import os
import dotenv

def setup_environment():
    """Initialize environment variables and API settings"""
    dotenv.load_dotenv()
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not aai.settings.api_key:
        raise ValueError("ASSEMBLYAI_API_KEY not found in environment variables")

def transcribe_audio(file_path):
    """
    Transcribe audio file using AssemblyAI
    
    Args:
        file_path (str): Path to the audio file
        
    Returns:
        aai.Transcript: Transcript object
    """
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_path)
    
    if transcript.status == aai.TranscriptStatus.error:
        raise Exception(f"Transcription error: {transcript.error}")
        
    return transcript

def save_transcript(transcript, source_file):
    """
    Save transcript to markdown file
    
    Args:
        transcript (aai.Transcript): Transcript object
        source_file (str): Original audio file path
    """
    transcript_file_name = os.path.splitext(os.path.basename(source_file))[0]
    output_dir = "DB/AudioTranscripts"
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, f"{transcript_file_name}_transcript.md")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Audio Transcription\n\n")
        f.write(f"Source: {source_file}\n\n")
        f.write("## Content\n\n")
        f.write(transcript.text)
    
    print(f"Successfully wrote transcription to {output_file}")

def main():
    try:
        # Initialize environment
        setup_environment()
        
        # File to transcribe
        FILE_URL = 'recordings/channel_General_20250302_182217.wav'
        
        # Process transcription
        print("Starting transcription...")
        transcript = transcribe_audio(FILE_URL)
        print("Transcription completed successfully")
        
        # Save results
        save_transcript(transcript, FILE_URL)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
