import os
import random
from pathlib import Path

class VideoSelector:
    def __init__(self, video_folder, uploaded_log):
        self.video_folder = Path(video_folder)
        self.uploaded_log = Path(uploaded_log)
        self.supported_formats = ['.mp4', '.mov', '.avi', '.mkv']
        
        if not self.video_folder.exists():
            raise FileNotFoundError(f"视频文件夹不存在: {self.video_folder}")
        
        self.uploaded_log.parent.mkdir(parents=True, exist_ok=True)
        if not self.uploaded_log.exists():
            self.uploaded_log.touch()
    
    def get_uploaded_videos(self):
        with open(self.uploaded_log, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f if line.strip())
    
    def mark_as_uploaded(self, video_path):
        with open(self.uploaded_log, 'a', encoding='utf-8') as f:
            f.write(f"{video_path}\n")
    
    def get_available_videos(self):
        uploaded = self.get_uploaded_videos()
        available = []
        
        for file in self.video_folder.iterdir():
            if file.is_file() and file.suffix.lower() in self.supported_formats:
                if str(file) not in uploaded:
                    available.append(file)
        
        return available
    
    def select_random_video(self):
        available = self.get_available_videos()
        if not available:
            return None
        return random.choice(available)
    
    def select_next_video(self):
        available = self.get_available_videos()
        if not available:
            return None
        available.sort(key=lambda x: x.stat().st_mtime)
        return available[0]
