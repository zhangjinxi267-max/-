# Instagram 视频自动上传工具

一个自动化程序，可以每天从你的电脑文件夹中随机选择视频文件，自动生成文案和话题标签，然后上传到 Instagram。

## 功能特点

- 📹 从指定文件夹自动选择视频文件
- ✍️ 自动生成吸引人的文案和话题标签
- 🤖 支持 AI 智能生成文案（可选，使用 OpenAI）
- ⏰ 定时任务，每天在指定时间自动上传
- 📝 记录已上传的视频，避免重复上传
- 🎬 支持上传为 Reels 或普通视频帖子

## 安装步骤

1. 克隆或下载此项目到你的电脑

2. 安装 Python 3.7+（如果还没有安装）

3. 安装依赖包：

```bash
pip install -r requirements.txt
```

4. 复制配置文件：

```bash
cp .env.example .env
```

5. 编辑 `.env` 文件，配置你的信息

## 配置说明

编辑 `.env` 文件，设置以下参数：

| 参数 | 说明 |
|------|------|
| `INSTAGRAM_USERNAME` | 你的 Instagram 用户名 |
| `INSTAGRAM_PASSWORD` | 你的 Instagram 密码 |
| `VIDEO_FOLDER` | 存放视频文件的文件夹路径 |
| `UPLOAD_TIME` | 每天上传时间（24小时制，例如：`12:00` |
| `DEFAULT_HASHTAGS` | 默认话题标签，用逗号分隔 |
| `UPLOADED_LOG` | 已上传视频记录文件（默认：uploaded_videos.txt） |
| `OPENAI_API_KEY` | OpenAI API Key（可选，用于 AI 生成文案） |
| `UPLOAD_AS_REEL` | 是否上传为 Reels（默认：true） |

## 使用方法

### 立即执行一次上传

如果你想立即测试上传功能：

```bash
python main.py --now
```

### 启动定时任务

让程序在后台运行，每天在指定时间自动上传：

```bash
python main.py
```

程序会一直运行，直到你按 `Ctrl+C` 停止。

## 视频格式要求

Instagram 对视频有一些限制，建议：
- 格式：MP4 或 MOV
- 时长：3 秒 - 60 秒
- 分辨率：1080x1920 (9:16) 最佳
- 大小：不超过 100MB

## 项目结构

```
/workspace/
├── main.py              # 主程序
├── video_selector.py    # 视频选择模块
├── caption_generator.py # 文案生成模块
├── instagram_uploader.py # Instagram 上传模块
├── requirements.txt    # 依赖列表
├── .env.example    # 配置示例文件
├── .gitignore       # Git 忽略文件
└── README.md         # 使用说明
```

## 注意事项

⚠️ 重要提醒：
1. 首次使用建议先用 `--now` 参数测试
2. Instagram 账号可能有上传频率限制，建议合理设置合适的上传频率
3. 确保你的视频符合 Instagram 的内容政策
4. 保护好你的 .env 文件，不要分享给他人
5. 程序会在已上传视频记录在文件中，删除该文件可以重置上传历史

## 常见问题

**Q: 如何重置已上传视频记录？**
A: 删除 `uploaded_videos.txt` 文件即可。

**Q: 可以同时支持多个视频文件夹吗？**
A: 当前版本只支持单个文件夹，你可以把多个文件夹的视频集中到一个文件夹中。

**Q: 程序会删除已上传的视频文件吗？**
A: 不会，程序只会记录哪些视频已上传，不会删除原文件。

**Q: 如何修改上传顺序？**
A: 当前是随机选择，你可以修改 video_selector.py 中的逻辑来改变选择策略。
