import os
import re
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from pydantic import BaseModel, Field
from typing import Optional
from .video_qa import FrameExtractor, FileUploader, AIContentGenerator, get_gemini_response

router = APIRouter()

# Assuming the class definitions for FrameExtractor, FileUploader, and AIContentGenerator are implemented

class VideoQAQueryItem(BaseModel):
    prompt: Optional[str] = Field(default="Describe this video.", title="Prompt for AI to describe the video")
    video_url: Optional[str] = None
    video_file: Optional[UploadFile] = None
    start_time: Optional[int] = None  # No default time, None means not set
    end_time: Optional[int] = None

async def video_qa_parameters(prompt: Optional[str] = Form("Describe this video."), video_url: Optional[str] = Form(None), video_file: Optional[UploadFile] = File(None), start_time: Optional[int] = Form(None), end_time: Optional[int] = Form(None)):
    return {"prompt": prompt, "video_url": video_url, "video_file": video_file, "start_time": start_time, "end_time": end_time}

@router.post("/tools/video_qa")
async def video_qa(item: dict = Depends(video_qa_parameters)):
    try:
        if item["video_url"] is None and item["video_file"] is None:
            raise HTTPException(status_code=400, detail="A video URL or video file is required.")
        
        video_file_path = ""
        response = ""
        
        if item["video_file"]:
            video_file_path = "./content/video/" + os.path.basename(item["video_file"].filename)
            directory = os.path.dirname(video_file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(video_file_path, "wb") as f:
                print(f"Saving video file to {video_file_path}")
                f.write(await item["video_file"].read())

        elif item["video_url"]:
            video_file_path = item["video_url"]
            pattern = r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]+(&\S+)?'
            match = re.match(pattern, item["video_url"])
            if match:
                modeloutput = await get_gemini_response(item["video_url"], item["prompt"])
                response += "Response from youtube extension: " +  modeloutput.text + '\n'
            

        # Setup frame extraction using specified time frames if provided
        extractor = FrameExtractor(video_file_path)
        extractor.extract_frames()

        uploader = FileUploader("./content/frames")
        if item["start_time"] is not None and item["end_time"] is not None:
            uploader.upload_files(upload_range=(item["start_time"], item["end_time"]))
        else:
            uploader.upload_files()  # No specific range provided
        uploader.list_files()

        ai_generator = AIContentGenerator()
        response += "Response2:" + ai_generator.generate_content(item["prompt"], uploader.uploaded_files)
        uploader.cleanup()

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"response": response}