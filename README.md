# 📊 亚马逊美国站假发/美妆类目运营日报工具

定时推送监控结果的小工具，每日生成亚马逊市场动态报告。

## 🚀 快速开始

### 1. 生成日报
```bash
cd /workspace
python amazon_daily_report.py
```

### 2. 查看生成的日报
日报会自动保存为 `amazon_daily_report.md` 文件。

## 📋 功能特性

- ✅ **自动生成日报**：结构化展示平台规则、活动信息、消费节点
- ✅ **面向假发/美妆类目**：针对性的运营建议
- ✅ **高优先级警示**：用颜色标注重要变动
- ✅ **今日行动项**：直接指导运营决策
- ✅ **可扩展架构**：支持接入真实数据源

## ⏰ 设置定时任务（Cron）

### 方法一：系统Cron（推荐）

编辑crontab：
```bash
crontab -e
```

添加以下内容（每日9:30执行）：
```
30 9 * * * cd /workspace && /usr/bin/python3 /workspace/amazon_daily_report.py >> /workspace/daily_report.log 2>&1
```

### 验证任务
```bash
crontab -l
```

### 查看日志
```bash
tail -f /workspace/daily_report.log
```

## 📁 项目结构

```
/workspace/
├── amazon_daily_report.py   # 主程序
├── amazon_daily_report.md   # 生成的日报（每日更新）
├── README.md                # 说明文档
└── daily_report.log         # 运行日志
```

## 🔧 自定义配置

### 1. 修改推送时间
在Cron配置中调整时间：
- `30 9 * * *` = 每天9:30
- `0 8 * * 1-5` = 工作日8:00

### 2. 修改数据源
编辑 `get_sample_market_updates()` 函数，接入：
- 网络爬虫
- Amazon Seller API
- RSS订阅源
- 自定义数据源

### 3. 接入飞书机器人推送
可扩展代码，通过飞书Webhook API将日报推送到群聊：
```python
import requests

def send_to_feishu(content: str, webhook_url: str):
    data = {"msg_type": "text", "content": {"text": content}}
    requests.post(webhook_url, json=data)
```

## 📊 日报模块说明

1. **平台规则与政策变动**：最新合规要求、费用调整
2. **亚马逊活动与促销信息**：大促时间、提报截止
3. **美国市场与消费节点**：节日机会、消费趋势
4. **今日关键行动项**：可执行的运营建议

## 💡 使用建议

1. **每天早上9:30**查看今日行动项
2. **重点关注高优先级**（红色）变动
3. **提前7天**开始筹备大型活动
4. **保存历史日报**，便于追踪政策演变

## 📝 更新日志

- **2026-05-13**：初始版本发布，支持基础日报生成

## 🤝 贡献

欢迎提交Issue和Pull Request！
