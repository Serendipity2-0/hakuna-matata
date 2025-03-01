# Start by making sure the `assemblyai` package is installed.
# If not, you can install it by running the following command:
# pip install -U assemblyai
#
# Note: Some macOS users may need to use `pip3` instead of `pip`.

import assemblyai as aai
import os
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

# Replace with your API key
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

# You can also transcribe a local file by passing in a file path
FILE_URL = '/Users/mforce/Desktop/hakuna-matata/DB/bkp/KaasDis1.mp3'

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(FILE_URL)

if transcript.status == aai.TranscriptStatus.error:
    print(transcript.error)
    exit(1)

print("Transcription completed successfully")
transcript_file_name = os.path.splitext(os.path.basename(FILE_URL))[0]

# Create the transcripts directory if it doesn't exist
output_dir = "DB/AudioTranscripts"
os.makedirs(output_dir, exist_ok=True)

# Full path to the output file
output_file = os.path.join(output_dir, f"{transcript_file_name}_transcript.md")
    
try:
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Audio Transcription\n\n")
        f.write(f"Source: {FILE_URL}\n\n")
        f.write("## Content\n\n")
        f.write(transcript.text)
    print(f"Successfully wrote transcription to {output_file}")
except Exception as e:
    print(f"Error writing to file: {str(e)}")


