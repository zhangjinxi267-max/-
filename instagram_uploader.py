from instagrapi import Client
import time
from pathlib import Path

class InstagramUploader:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.client = Client()
        self.logged_in = False
    
    def login(self):
        try:
            self.client.login(self.username, self.password)
            self.logged_in = True
            print(f"成功登录 Instagram: {self.username}")
            return True
        except Exception as e:
            print(f"登录失败: {e}")
            return False
    
    def logout(self):
        try:
            if self.logged_in:
                self.client.logout()
                self.logged_in = False
                print("已退出登录")
        except Exception as e:
            print(f"退出登录失败: {e}")
    
    def upload_reel(self, video_path, caption):
        if not self.logged_in:
            if not self.login():
                return False
        
        try:
            video_path = Path(video_path)
            print(f"正在上传视频: {video_path.name}")
            
            media = self.client.clip_upload(
                path=str(video_path),
                caption=caption,
                extra_data={
                    'share_to_feed': True
                }
            )
            
            print(f"上传成功！视频 ID: {media.pk}")
            return True
        except Exception as e:
            print(f"上传失败: {e}")
            return False
    
    def upload_video_post(self, video_path, caption):
        if not self.logged_in:
            if not self.login():
                return False
        
        try:
            video_path = Path(video_path)
            print(f"正在上传视频: {video_path.name}")
            
            media = self.client.video_upload(
                path=str(video_path),
                caption=caption
            )
            
            print(f"上传成功！视频 ID: {media.pk}")
            return True
        except Exception as e:
            print(f"上传失败: {e}")
            return False
