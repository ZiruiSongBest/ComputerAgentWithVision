import os
import shutil
import cv2
import google.generativeai as genai
import dotenv
from typing import List

dotenv.load_dotenv()

# Set up API access
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

class FrameExtractor:
    def __init__(self, video_url, frame_directory="./content/frames", frame_prefix="_frame"):
        self.video_url = video_url
        self.frame_directory = frame_directory
        self.frame_prefix = frame_prefix

    def create_frame_output_dir(self):
        if os.path.exists(self.frame_directory):
            shutil.rmtree(self.frame_directory)
        os.makedirs(self.frame_directory)

    def extract_frames(self):
        print(f"Extracting {self.video_url} at 1 frame per second. This might take a bit...")
        self.create_frame_output_dir()
        vidcap = cv2.VideoCapture(self.video_url)
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        frame_duration = 1 / fps
        output_file_prefix = os.path.basename(self.video_url).replace('.', '_')
        count, frame_count = 0, 0
        while vidcap.isOpened():
            success, frame = vidcap.read()
            if not success:
                break
            if int(count / fps) == frame_count:
                min = frame_count // 60
                sec = frame_count % 60
                time_string = f"{min:02d}:{sec:02d}"
                image_name = f"{output_file_prefix}{self.frame_prefix}{time_string}.jpg"
                output_filename = os.path.join(self.frame_directory, image_name)
                cv2.imwrite(output_filename, frame)
                frame_count += 1
            count += 1
        vidcap.release()
        print(f"Completed video frame extraction. Extracted: {frame_count} frames")

class File:
    def __init__(self, file_path: str, display_name: str = None):
        self.file_path = file_path
        if display_name:
            self.display_name = display_name
        self.timestamp = File.get_timestamp(file_path)

    def set_file_response(self, response):
        self.response = response

    @staticmethod
    def get_timestamp(filename, frame_prefix="_frame"):
        """Extracts the frame count (as an integer) from a filename with the format
        'output_file_prefix_frame00:00.jpg'.
        """
        parts = filename.split(frame_prefix)
        if len(parts) != 2:
            return None  # Indicates the filename might be incorrectly formatted
        return parts[1].split('.')[0]

class FileUploader:
    def __init__(self, frame_directory):
        self.frame_directory = frame_directory
        self.uploaded_files = []

    def upload_files(self, upload_range=None):
        files = sorted(os.listdir(self.frame_directory))
        files_to_upload = [File(file_path=os.path.join(self.frame_directory, file)) for file in files]
        for file in files_to_upload if upload_range==None else files_to_upload[upload_range[0]:upload_range[1]]:
            print(f'Uploading: {file.file_path}...')
            response = genai.upload_file(path=file.file_path)
            file.set_file_response(response)
            self.uploaded_files.append(file)
        print(f"Uploaded: {len(self.uploaded_files)} files")

    def list_files(self):
        for n, f in zip(range(len(self.uploaded_files)), genai.list_files()):
            print(f.uri)

    def cleanup(self):
        for file in self.uploaded_files:
            genai.delete_file(file.name)
            print(f'Deleted {file.display_name}.')
        print(f"Completed deleting files.\n\nDeleted: {len(uploaded_files)} files")
    
    def delete_all(self):
        uploaded_files = []
        for f in genai.list_files():
            print(f.uri)
            uploaded_files.append(f)
        
        for file in uploaded_files:
            genai.delete_file(file.name)
            print(f'Deleted {file.display_name}.')
        print(f"Completed deleting files!\n\nDeleted: {len(uploaded_files)} files")
    

class AIContentGenerator:
    def __init__(self, model_name="models/gemini-1.5-pro-latest"):
        self.model = genai.GenerativeModel(model_name=model_name)

    def generate_content(self, prompt, files: List[File]):
        request = [prompt]
        for file in files:
            request.append(file.timestamp)
            request.append(file.response)
        response = self.model.generate_content(request, request_options={"timeout": 600})
        return response.text

if __name__ == "__main__":
    
    # video_file_name = "https://download.blender.org/peach/bigbuckbunny_movies/BigBuckBunny_320x180.mp4"
    video_file_name = "/Users/dylan/Downloads/BigBuckBunny_320x180.mp4"
    extractor = FrameExtractor(video_file_name)
    extractor.extract_frames()
    
    uploader = FileUploader("./content/frames")
    uploader.upload_files(upload_range=(45, 50))  # Uploads 10 seconds slice
    uploader.list_files()
    
    # Create the AI content generator and make a request
    ai_generator = AIContentGenerator()
    prompt = "Describe this video."
    response = ai_generator.generate_content(prompt, uploader.uploaded_files)
    print("AI Response:", response)

    uploader.cleanup()
    # uploader.delete_all()
    pass
 