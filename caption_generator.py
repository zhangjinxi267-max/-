import os
import random
from datetime import datetime

class CaptionGenerator:
    def __init__(self, default_hashtags=None, openai_api_key=None):
        self.default_hashtags = default_hashtags or []
        self.openai_api_key = openai_api_key
        
        self.caption_templates = [
            "今天分享精彩瞬间，希望大家喜欢！✨",
            "新视频上线！欢迎点赞关注～ 🔥",
            "记录美好时光 ✨",
            "享受每一刻 🎬",
            "精彩继续，更多内容敬请期待！💫",
            "今日份快乐已送达 😊",
            "生活就是要记录这些美好瞬间 💕",
            "感谢观看！❤️",
            "分享一下我的日常 📹",
            "周末愉快！🎥"
        ]
        
        self.hashtag_pools = [
            "instagram", "video", "viral", "reels", "fyp", "trending",
            "daily", "life", "moments", "happy", "fun", "vibes",
            "beautiful", "amazing", "awesome", "cool", "instagood",
            "photooftheday", "love", "instadaily", "likeforlikes"
        ]
    
    def generate_caption(self, video_name=None, use_ai=False):
        if use_ai and self.openai_api_key:
            return self._generate_with_ai(video_name)
        
        caption = random.choice(self.caption_templates)
        hashtags = self._generate_hashtags()
        
        return f"{caption}\n\n{hashtags}"
    
    def _generate_hashtags(self):
        tags = self.default_hashtags.copy()
        
        additional_count = min(8, 25 - len(tags))
        if additional_count > 0:
            additional = random.sample(self.hashtag_pools, additional_count)
            tags.extend(additional)
        
        return ' '.join([f'#{tag}' for tag in tags])
    
    def _generate_with_ai(self, video_name):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_api_key)
            
            prompt = f"为一个Instagram视频创作吸引人的文案和相关话题标签。视频名: {video_name or '未命名'}"
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个专业的社交媒体内容创作者，擅长撰写吸引人的Instagram文案。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"AI生成失败，使用默认文案: {e}")
            return self.generate_caption(video_name, use_ai=False)
