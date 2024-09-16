import asyncio
import time
from dataclasses import dataclass
from typing import List, Tuple

import aiofiles
import aiohttp
import assemblyai as aai
from assemblyai import TranscriptStatus
from openai import AsyncOpenAI

from server import settings

from .agents_schema import TranscribingConfig
from .constants import KnowledgePattern


@dataclass
class AssemblyAiAgent:

    def __post_init__(self):
        aai.settings.api_key = settings.ASSEMBLYAI_API_KEY

    async def _upload_local_file(self, file_path: str) -> dict:
        """
        Upload a local file to AssemblyAI for transcription.
        """
        settings.LOGGER.info(f"Uploading local file: {file_path}")
        url = f"{settings.ASSEMBLYAI_BASE_URL}/upload"
        headers = {
            "Authorization": settings.ASSEMBLYAI_API_KEY,
            "Content-Type": "application/octet-stream",
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with aiofiles.open(file_path, "rb") as file:
                    file_content = await file.read()
                    settings.LOGGER.debug(
                        f"File content read, size: {len(file_content)} bytes"
                    )
                    async with session.post(
                        url, data=file_content, headers=headers
                    ) as response:
                        response.raise_for_status()
                        result = await response.json()
                        settings.LOGGER.info(f"File uploaded successfully: {file_path}")
                        return result
            except aiofiles.errors.AIOError as e:
                settings.LOGGER.error(f"Error reading file {file_path}: {str(e)}")
                raise
            except aiohttp.ClientError as e:
                settings.LOGGER.error(f"Error uploading file {file_path}: {str(e)}")
                raise

    async def _submit_audio_file(
        self,
        config_dict: dict,
        public_audio_path: str,
    ):
        url = f"{settings.ASSEMBLYAI_BASE_URL}/transcript"
        headers = {"Authorization": settings.ASSEMBLYAI_API_KEY}
        data = {
            "audio_url": public_audio_path,
            **config_dict,
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=data, headers=headers) as response:
                    response.raise_for_status()
                    transcript = await response.json()
            except Exception as err:
                settings.LOGGER.error(
                    f"Transcription request failed for {public_audio_path} because {err}"
                )
                return

            id, status = transcript["id"], transcript["status"]

            print(f"Transcription ID: {id}")

            if status == TranscriptStatus.error.value:
                settings.LOGGER.error(f"Transcription error for {public_audio_path}.")
            else:
                settings.LOGGER.info(
                    f"Transcription is {status} for {public_audio_path}."
                )
                return id

    async def _get_transcript_response(self, transcript_id: str):
        url = f"{settings.ASSEMBLYAI_BASE_URL}/transcript/{transcript_id}"
        headers = {"Authorization": settings.ASSEMBLYAI_API_KEY}

        transcript = {}
        status = None

        _start_time = time.time()

        async with aiohttp.ClientSession() as session:
            while True:
                settings.LOGGER.info(
                    f"Requesting transcription for SRT-ID: {transcript_id}"
                )

                _elapsed_time = time.time() - _start_time
                async with session.get(url, headers=headers) as response:
                    if response.status in [400, 500] or _elapsed_time > 300:
                        status = TranscriptStatus.error.value
                        break
                    else:
                        task: dict = await response.json()
                        _status = task["status"]

                        if _status == TranscriptStatus.error.value:
                            settings.LOGGER.error(
                                f"Transcription error for {transcript_id}"
                            )
                            status = _status
                            break

                        elif (
                            _status == TranscriptStatus.processing.value
                            or _status == TranscriptStatus.queued.value
                        ):
                            await asyncio.sleep(5)

                        else:
                            # check for spoken words
                            if len(task["words"]) >= 10:
                                transcript = task
                                status = _status
                                break
                            else:
                                settings.LOGGER.error(
                                    f"Transcription {transcript_id} has less than 10 spoken words. "
                                )
                                status = "less_than_10_words"
                                break

        return transcript, status

    async def transcribe_audio(
        self, config: TranscribingConfig, *, file_path: str
    ) -> Tuple[dict, str]:
        upload_response = await self._upload_local_file(file_path)
        _audio_url = upload_response.get("upload_url")
        if not _audio_url:
            raise ValueError("Audio URL not found in upload response")

        transcript_id = await self._submit_audio_file(
            config_dict=config.model_dump(), public_audio_path=_audio_url
        )
        transcript_data, transcript_status = await self._get_transcript_response(
            transcript_id
        )
        return transcript_data, transcript_status


@dataclass
class OpenAiAgent:
    knowledge_patterns: List[KnowledgePattern]
    transcript: str

    def __post_init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    @staticmethod
    async def __get_prompt(pattern: str) -> str:
        prompt_path = f"patterns/create_{pattern}.md"
        async with aiofiles.open(prompt_path, mode="r") as file:
            return await file.read()

    async def _process_pattern(self, pattern: str, model_name: str = "gpt-4o") -> dict:
        prompt = await self.__get_prompt(pattern)
        response = await self.client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": self.transcript},
            ],
        )
        return {
            "pattern": pattern,
            "response": response.choices[0].message.content,
        }

    async def process_all_patterns(self) -> List[dict]:
        tasks = [
            self._process_pattern(pattern.value) for pattern in self.knowledge_patterns
        ]
        return await asyncio.gather(*tasks)


if __name__ == "__main__":

    async def transcribe_audio():
        agent = AssemblyAiAgent()
        transcript_data, transcript_status = await agent.transcribe_audio(
            TranscribingConfig(language_code="en", speaker_labels=False),
            file_path="/Users/satyarthraghuvanshi/Downloads/sample_meeting.m4a",
        )
        print(f"Transcript status: {transcript_status}")
        print(f"Transcript data: {transcript_data}")

    async def notes():
        transcript = """
                Podcasting with a lace restaurant means usually I don't like to have a meeting just like that. Right. So this is all the workshop is fine, but usually when you have a meeting as a team, so you would ideally like to have, what are the things that will be discussed beforehand and not like, you know, go there and have the agenda. So I would like to say like maybe five six pointers, five six question pointers, which you want to cover in that particular meeting for attaining course. Right. So that is the input. And then you kind of speak to the whole meeting. And then you get an audio file, that audio file you would want to just simply upload to this particular, your QT. Okay. And your QT will take it and make a pattern. Okay. So in the pattern I'll give you like, we'll give three options. One is the GitHub issues, one is what is the end point for. Usually when we have a discussion for market history accounting team and for marketing team, it's usually ideas what format you want. Okay, so what format would you ideally want? Okay, so what we will do is like every single team will have one technical guy and you guys should, we are supposed to set up fabric on that machine and give an API. Okay, so that is how I want you to set up that if I possible, you know, that's primary thing. So you can take care of the accounting team. Accounting team. Okay. Already have a app. Were you guys able to, able to open it yesterday? Yeah. Okay. They're able to open it yesterday. So make sure you add that new tab feature saying that meeting, whatever you want to call it. But it has to be done on both the, both these people's machines. Okay. And they should have an option to upload the WAV file or, and then there's a button to read. Process. Process means it will go straight to the request over here and the request will give back a pattern. Okay, so both of you should you create a fast API version. Okay. And we will all, and then you have to send it in a group how to use the pattern. So here's the Wav file. I'm going to send it to the WAV file and it's going to take transcribe and then it should give that output, the transcribed output to the fabric and fabric will give you back the pattern and you just send it back. Can you guys do that? Okay, you should show it on the screen like yesterday. I have a tab, right? Somebody can open the app, please. Any other Lantos? Okay, on the left hand side you have, this is the one meeting. Meeting, what meeting? No, it is going to take the meeting as input and then it's going to give you back a pattern. Meeting. Reader meeting, readers meet something creative pattern in the sense what? I'll show you example. So when we have a meeting, we write the details. Meet repeater saying browse, click on that your how mpg in your trans and mph. Three to connect to texture, thus file. Okay, from that to a set pattern in MD file. Okay, we'll stop till here. If we can continue further, we'll see. Eventually it has to go back and store in a certain already known location. Okay. One in your local, one back in the server. Okay. One fabric on the example one, the pattern. What do you mean by that? See, this is kind of your own way of learning coding. So it's like, no, the technical way is not going to do much of the work. He's going to assist you and you are going to do the majority of the work. Okay, but if you understand, just to understand the concept, will show that thing one just add so it'll do comment, no example link. Okay, maybe there are patterns in the photo. If it helps. In my system I have example I can show you. Look at this gui. What language do you think it was made in if I told you it? All right, so eleven will consider, I want to extract the knowledge. What is it like tell you. Okay, so what I'm going to do is I'm just going to copy here. And I actually have set up an obsidian, so I just want to show that knowledge, wisdom and philosophy. Knowledge, wisdom and philosophy. Yes, yes. So, so I just input that. So in my clipboard I copied, right? So that's what I'm using here. Okay, and pattern, I already have a pattern called as extract wisdom. Okay? So every single time you give any sort of data to this. So it's going to take that and it is going to extract wisdom in the same format. I'll give you two examples and the subject studio better. But is one of an example we need to understand. So we just wrapped it, the whole thing, and it's created in a, it always creates a format that what say, what is the summary, what is an idea, what are the insights, what are the codes, habits? So that is a preset pattern, right? So every single time. So e video code 25, I can give you another video. Also I can give you, forget video, even the audio, whatever we talk, right? So we can give that audio to that and it will transcribe and then it will always give answer in this format. Okay? I'll give you one more example, let me take one, some article, random article, an article about, oh by the way, open air released a new model. Anybody, I thought anybody would say, nobody said nobody cares. Open AI thinking time for some case on this. Same thing again. You know what I did is I took this whole, I think I can do control a, control c. So I can just go here, it's on my clipboard again, I only have one pattern as of now. I can, so there are more patterns. Also this is an extract wisdom pattern. So I could be having a meeting extractor pattern, like for, okay, doom studios pattern, we could have one for GitHub pattern issues pattern. Okay. And then now I just go submit, hopefully. See, it's like even this I got in the same format. So it was a text format, I didn't even read the whole thing. But it always gives me, okay, what is the main point? What is the thing? So you always get the result back in a format, what you want. So where is it useful? In our day to day meetings, usually we always meet and every single time if I ask the transcript, you give it in some other format, some other LC will give some other format, it always changes. So how is it difficult eventually, once you have lots of meetings happening. So you would want to have a certain format all the time. That's what this does. So this is what you will be building now. So instead of it can take anything, it can take a link, it can take a YouTube video or it can take a certain things and then you can select which kind of pattern you want and you will get that. And you also get options where to store it. So this is a full end life cycle, right? So once it's stored back, you can always convert it, tasks or anything, you know. So you will figure out what is the workflow that is you, that will be useful for you on a daily basis. So this is just the first part of the work. Okay, got it. Anybody has any doubt or anybody has any comments, additions. Karthik, I have a question about activity and you can apply day to day activity like where? Where are you going to use it? Okay, all of you tell me one use case. Let's see. So it's even a question for everyone. Yes, yes, yes. What do you guys understand by pattern? What's the pattern? What do you guys understand the pattern? And what kind of pattern would be useful to us specifically? If you can answer that, it will be more beneficial. So what I think pattern is, it's like a format, okay. It is in a way where it can be stored in same particular format. You cannot have an editable form or something. So it is an inbuilt format which thrown out by a particular. What is the use case? Where would you use this? Where is it useful? In your day to day workflow? Where is it useful? For example, APRD project, we want the main story. We just are discussing it and giving the audio file to the app and it will create the main story from which we can extract all the subtasks. And so we will implement that. So this is actually in go. So you guys need to set up one wrapper. There is a sub process. Use the sub process to write a python wrapper on top of the board. No, we don't need to use it, but right now we don't want to complicate also because they want to be able to send a request immediately. All right, guys, let's disperse then. So, yeah. Accounting team Garo Washitana so, Marcella, okay, one, two, three. You said, okay, we can't move this.
                """

        agent = OpenAiAgent(
            knowledge_patterns=[
                KnowledgePattern.SUMMARY,
                KnowledgePattern.IDEA_COMPASS,
                KnowledgePattern.KEYNOTE,
            ],
            transcript=transcript,
        )
        result = await agent.process_all_patterns()
        print(result)
