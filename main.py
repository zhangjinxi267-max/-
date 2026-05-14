#!/usr/bin/env python3
import os
import time
import schedule
from dotenv import load_dotenv
from video_selector import VideoSelector
from caption_generator import CaptionGenerator
from instagram_uploader import InstagramUploader
from datetime import datetime

def load_config():
    load_dotenv()
    
    return {
        'username': os.getenv('INSTAGRAM_USERNAME'),
        'password': os.getenv('INSTAGRAM_PASSWORD'),
        'video_folder': os.getenv('VIDEO_FOLDER'),
        'upload_time': os.getenv('UPLOAD_TIME', '12:00'),
        'default_hashtags': os.getenv('DEFAULT_HASHTAGS', 'instagram,video,viral,reels').split(','),
        'uploaded_log': os.getenv('UPLOADED_LOG', 'uploaded_videos.txt'),
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'upload_as_reel': os.getenv('UPLOAD_AS_REEL', 'true').lower() == 'true'
    }

def upload_video():
    config = load_config()
    
    print(f"{'='*50}")
    print(f"开始执行上传任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")
    
    if not config['username'] or not config['password']:
        print("错误: 请先在 .env 文件中配置 Instagram 账号信息")
        return False
    
    if not config['video_folder']:
        print("错误: 请先在 .env 文件中配置视频文件夹路径")
        return False
    
    try:
        selector = VideoSelector(config['video_folder'], config['uploaded_log'])
    except Exception as e:
        print(f"初始化视频选择器失败: {e}")
        return False
    
    video = selector.select_random_video()
    if not video:
        print("没有可用的视频可以上传")
        return False
    
    print(f"选中视频: {video.name}")
    
    caption_gen = CaptionGenerator(config['default_hashtags'], config['openai_api_key'])
    caption = caption_gen.generate_caption(video.stem, use_ai=bool(config['openai_api_key']))
    
    print(f"\n生成的文案:\n{caption}\n")
    
    uploader = InstagramUploader(config['username'], config['password'])
    
    try:
        if config['upload_as_reel']:
            success = uploader.upload_reel(video, caption)
        else:
            success = uploader.upload_video_post(video, caption)
        
        if success:
            selector.mark_as_uploaded(str(video))
            print(f"✅ 任务完成！")
        else:
            print(f"❌ 上传失败")
        
        return success
    finally:
        uploader.logout()

def main():
    config = load_config()
    
    print(f"{'='*50}")
    print(f"Instagram 视频自动上传程序已启动")
    print(f"上传时间: 每天 {config['upload_time']}")
    print(f"视频文件夹: {config['video_folder']}")
    print(f"{'='*50}\n")
    
    schedule.every().day.at(config['upload_time']).do(upload_video)
    
    print("按 Ctrl+C 退出程序\n")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n程序已停止")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Instagram 视频自动上传程序')
    parser.add_argument('--now', action='store_true', help='立即执行一次上传，而不是等待定时任务')
    args = parser.parse_args()
    
    if args.now:
        upload_video()
    else:
        main()
