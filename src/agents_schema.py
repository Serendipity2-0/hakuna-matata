import assemblyai as aai
from pydantic import BaseModel


class TranscribingConfig(BaseModel):
    language_code: str  # Input audio language
    speaker_labels: bool  # Enable Speaker Diarization
    # disfluencies: bool = False  # Transcribe Filler Words, like "umm"
    # punctuate: bool = True  # Automatic Punctuation
    # format_text: bool = True  # Text Formatting
    speech_model: str = aai.SpeechModel.best.value
