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
        self.uploaded_files: List[File] = []
        self.current_files: List[File] = []

    def upload_files(self, upload_range=None):
        files = sorted(os.listdir(self.frame_directory))
        files_to_upload = [File(file_path=os.path.join(self.frame_directory, file), display_name=file) for file in files]
        uploaded_file_names = [file.display_name for file in self.uploaded_files]
        for file in files_to_upload if upload_range==None else files_to_upload[upload_range[0]:upload_range[1]]:
            print(f'Uploading: {file.file_path}...')
            response = genai.upload_file(path=file.file_path)
            print(response.name)
            response = genai.get_file(response.name)
            print(response)
            break
            if file.display_name not in uploaded_file_names:
                response = genai.upload_file(path=file.file_path)
                print(response)
                file.set_file_response(response)
                self.uploaded_files.append(file)
                self.current_files.append(file)
            else:
                for uploaded_file in self.uploaded_files:
                    if uploaded_file.display_name == file.display_name:
                        self.current_files.append(uploaded_file)
                        break
        print(f"Uploaded: {len(self.current_files)} files")

    def list_files(self):
        for n, f in zip(range(len(self.current_files)), genai.list_files()):
            print(f.uri)

    def cleanup(self):
        for file in self.current_files:
            genai.delete_file(file.name)
            print(f'Deleted {file.display_name}.')
        print(f"Completed deleting files.\n\nDeleted: {len(self.current_files)} files")
    
    def list_all_files(self):
        self.uploaded_files = []
        for f in genai.list_files():
            print(f.display_name, f.uri)
            self.uploaded_files.append(f)
        return self.uploaded_files
    
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
    video_file_name = "/Users/dylan/Desktop/1Res/osc/ComputerAgentWithVisionDev/content/video/Path of Ascension - Pelagos vs Kalisthene - Trial of Humility.mp4"
    test_name = 'Path of Ascension - Pelagos vs Kalisthene - Trial of Humility_mp4_frame01:17.jpg'
    # extractor = FrameExtractor(video_file_name)
    # extractor.extract_frames()
    
    uploader = FileUploader("./content/frames")
    # uploader.list_all_files()
    
    # for file in uploader.uploaded_files:
    #     file.timestamp = File.get_timestamp(file.display_name)
    #     print(file.timestamp)
    uploader.upload_files()
    
    # files = sorted(files, key=lambda x: x.display_name)
    
    # for file in uploader.current_files:
        # print(file.display_name, file.uri)
    
    # print(genai.get_file(test_name))
    
    # Create the AI content generator and make a request
    # ai_generator = AIContentGenerator()
    # prompt = "Describe this video."
    # response = ai_generator.generate_content(prompt, uploader.current_files)
    # print("AI Response:", response)

    # uploader.cleanup()
    # uploader.delete_all()
    # pass
 