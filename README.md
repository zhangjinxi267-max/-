# 📊 亚马逊美国站假发/美妆类目运营日报工具

定时推送监控结果的小工具，每日生成亚马逊市场动态报告，支持飞书Webhook推送和邮件发送。

## 🚀 快速开始

### 1. 生成日报
```bash
cd /workspace
python amazon_daily_report.py
```

### 2. 生成日报并推送到飞书
```bash
# 使用配置文件中的Webhook URL
python amazon_daily_report.py --feishu

# 或使用命令行指定Webhook URL
python amazon_daily_report.py --feishu --webhook https://open.feishu.cn/open-apis/bot/v2/hook/xxx
```

### 3. 生成日报并发送邮件
```bash
python amazon_daily_report.py --email
```

### 4. 同时推送飞书和邮件
```bash
python amazon_daily_report.py --feishu --email
```

### 5. 查看生成的日报
日报会自动保存为 `amazon_daily_report.md` 文件。

## 📋 功能特性

- ✅ **自动生成日报**：结构化展示平台规则、活动信息、消费节点
- ✅ **面向假发/美妆类目**：针对性的运营建议
- ✅ **高优先级警示**：用颜色标注重要变动
- ✅ **今日行动项**：直接指导运营决策
- ✅ **飞书推送**：通过Webhook推送至飞书群聊
- ✅ **邮件发送**：支持SMTP邮件发送
- ✅ **可扩展架构**：支持接入真实数据源

## ⏰ 设置定时任务（Cron）

### 方法一：系统Cron（推荐）

编辑crontab：
```bash
crontab -e
```

添加以下内容（每日9:30执行，同时推送到飞书）：
```
30 9 * * * cd /workspace && /usr/bin/python3 /workspace/amazon_daily_report.py --feishu >> /workspace/daily_report.log 2>&1
```

### 方法二：使用设置脚本
```bash
cd /workspace
./setup_daily_job.sh
```

### 验证任务
```bash
crontab -l
```

### 查看日志
```bash
tail -f /workspace/daily_report.log
```

## 🔧 配置说明

### 配置文件

编辑 `report_config.json` 文件：

```json
{
  "feishu_webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/your-webhook-token",
  "email": {
    "smtp_server": "smtp.feishu.cn",
    "smtp_port": 587,
    "smtp_user": "your-email@your-domain.com",
    "smtp_password": "your-app-password",
    "sender_email": "your-email@your-domain.com",
    "receiver_emails": ["recipient1@example.com", "recipient2@example.com"]
  }
}
```

### 飞书Webhook配置

1. 在飞书群聊中添加「自定义机器人」
2. 获取Webhook URL
3. 将URL填入配置文件

### 邮件配置

支持飞书邮箱、QQ邮箱、Gmail等：

- **飞书邮箱**：smtp.feishu.cn:587
- **QQ邮箱**：smtp.qq.com:587（使用授权码）
- **Gmail**：smtp.gmail.com:587（使用App Password）

## 📁 项目结构

```
/workspace/
├── amazon_daily_report.py   # 主程序（含飞书推送和邮件发送）
├── amazon_daily_report.md   # 生成的日报（每日更新）
├── report_config.json       # 配置文件（飞书、邮箱设置）
├── setup_daily_job.sh       # 定时任务设置脚本
├── setup_cron.py            # Python版定时任务配置
├── README.md                # 说明文档
└── daily_report.log         # 运行日志
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

- **2026-05-13**：添加飞书Webhook推送和邮件发送功能
- **2026-05-13**：初始版本发布，支持基础日报生成

## 🤝 贡献

欢迎提交Issue和Pull Request！
