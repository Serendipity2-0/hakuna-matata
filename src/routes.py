from typing import List

from fastapi import File, UploadFile

from server import APIRouter

from .constants import Department, KnowledgePattern
from .views import FetchWisdomFile, MeetingProcessor

meeting_router = APIRouter(prefix="/meeting", tags=["meeting"])


@meeting_router.post("/submit-meeting")
async def transcribe_meeting(
    language: str,
    meeting_subject: str,
    knowledge_patterns: List[str],
    department: Department,
    audio_file: UploadFile = File(...),
):
    # knowledge_patterns is in ['keynote,summary']
    knowledge_patterns = knowledge_patterns[0].split(",")
    validated_patterns = [KnowledgePattern(pattern) for pattern in knowledge_patterns]

    return await MeetingProcessor(
        language=language,
        meeting_subject=meeting_subject,
        knowledge_patterns=validated_patterns,
        department=department,
        audio_file=audio_file,
    ).build_knowledge_base()


@meeting_router.get("/wisdom-file/{file_search_dir}")
async def download_file(file_search_dir: str):
    return await FetchWisdomFile().get(file_search_dir)
