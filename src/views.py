import asyncio
import json
import os
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Literal

import aiofiles
from fastapi import UploadFile
from fastapi.responses import FileResponse, JSONResponse

from server import settings

from .agents import AssemblyAiAgent, OpenAiAgent
from .agents_schema import TranscribingConfig
from .constants import Department, KnowledgePattern


@dataclass
class MeetingProcessor:
    language: str
    meeting_subject: str
    knowledge_patterns: List[KnowledgePattern]
    department: Department
    audio_file: UploadFile
    audio_file_path: str = field(default=None, init=False)

    save_dir: str = field(default=None, init=False)

    def __post_init__(self):
        department_dir = self.department.value.lower().replace(" ", "_")
        date_dir = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.save_dir = os.path.join(settings.UPLOAD_DIR, department_dir, date_dir)
        os.makedirs(self.save_dir, exist_ok=True)

    async def _save_audio_file(self) -> bool:
        save_path = os.path.join(self.save_dir, self.audio_file.filename)

        try:
            async with aiofiles.open(save_path, "wb") as buffer:
                chunk_size = 1024 * 1024  # 1 MB chunks
                while True:
                    chunk = await self.audio_file.read(chunk_size)
                    if not chunk:
                        break
                    await buffer.write(chunk)
            self.audio_file_path = save_path
            return True
        except Exception as e:
            settings.LOGGER.error(f"Error saving audio file: {str(e)}")
            return False

    async def _transcribe_audio(self):
        agent = AssemblyAiAgent()
        config = TranscribingConfig(language_code=self.language, speaker_labels=False)
        transcript_data, transcript_status = await agent.transcribe_audio(
            config=config, file_path=self.audio_file_path
        )

        if transcript_status != "completed":
            raise ValueError(f"Transcription failed with status: {transcript_status}")

        return transcript_data.get("text", "")

    async def _process_patterns(self, transcript: str):
        agent = OpenAiAgent(
            knowledge_patterns=self.knowledge_patterns,
            transcript=transcript,
        )
        return await agent.process_all_patterns()

    async def _save_output_files(
        self,
        patterns_results: List[Dict[str, str]],
        return_type: str,
    ):
        combined_content = []

        if return_type == "json":
            filename = "combined_results.json"

            for result in patterns_results:
                pattern = result["pattern"]
                content = result["response"]
                combined_content.append({pattern: content})

            file_content = json.dumps(combined_content, indent=4)

        else:
            filename = "combined_results.md"

            for result in patterns_results:
                pattern = result["pattern"]
                content = result["response"]
                combined_content.append(f"# {pattern.upper()}\n\n{content}")

            # Join all sections with a markdown separator
            file_content = "\n\n---\n\n".join(combined_content)

        file_path = os.path.join(self.save_dir, filename)
        async with aiofiles.open(file_path, "w") as f:
            await f.write(file_content)

    async def _async_task(self, return_type: str):
        transcript = await self._transcribe_audio()
        patterns_results = await self._process_patterns(transcript)
        return await self._save_output_files(patterns_results, return_type)

    async def build_knowledge_base(
        self, return_type: Literal["json", "markdown"] = "markdown"
    ):
        if await self._save_audio_file():
            asyncio.create_task(self._async_task(return_type))

            # save_dir is in /Users/satyarthraghuvanshi/projects/hakuna-matata/uploads/trademan/2024-09-17_12-29-16
            # replace all the / with -
            _save_dir = self.save_dir.replace("/", "+")
            return JSONResponse(
                content={
                    "message": "Audio file saved successfully. Building knowledge base...",
                    "dir_search_path": _save_dir,
                }
            )
        return JSONResponse(
            content={
                "message": "Failed to save audio file",
                "file_path": None,
            },
            status_code=400,
        )


class FetchWisdomFile:
    async def _schedule_file_deletion(self, file_dir: str):
        _del_time = 5
        settings.LOGGER.info(f"Scheduling file deletion in {_del_time} seconds")
        await asyncio.sleep(_del_time)

        # split the file_dir to get the last directory
        _last_dir = file_dir.split("/")[-1]
        settings.LOGGER.info(f"Deleting files in {_last_dir}")

        for file in os.listdir(file_dir):
            os.remove(os.path.join(file_dir, file))
        # delete the _last_dir
        os.rmdir(file_dir)

    async def get(self, dir_search_path: str):
        _file_search_dir = dir_search_path.replace("+", "/")
        print(_file_search_dir)

        # check if file exists
        if not os.path.exists(_file_search_dir):
            return JSONResponse(
                content={
                    "message": "File not found. Try again.",
                    "file_path": None,
                },
                status_code=404,
            )

        # search the file (combined_results) from in dir_search_path. Try for .md first, then .json
        file_path = os.path.join(_file_search_dir, "combined_results.md")
        if not os.path.exists(file_path):
            file_path = os.path.join(_file_search_dir, "combined_results.json")

        if not os.path.exists(file_path):
            return JSONResponse(
                content={
                    "message": "File not found. Try again.",
                    "file_path": None,
                },
                status_code=404,
            )

        # check media type based on file extension
        if file_path.endswith(".json"):
            media_type = "application/json"
        elif file_path.endswith(".md"):
            media_type = "text/markdown"

        filename = os.path.basename(file_path)

        asyncio.create_task(self._schedule_file_deletion(_file_search_dir))
        return FileResponse(path=file_path, filename=filename, media_type=media_type)
