#!/usr/bin/env python3
"""
亚马逊美国站假发/美妆类目运营日报生成器
每日自动推送最新市场动态和规则更新
支持飞书Webhook推送和邮件发送
"""

import json
import datetime
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import Dict, List, Any, Optional


class AmazonDailyReport:
    def __init__(self):
        self.date = datetime.datetime.now().strftime("%Y年%m月%d日")
        self.report = {}
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        config_path = '/workspace/report_config.json'
        default_config = {
            "feishu_webhook_url": "",
            "email": {
                "smtp_server": "smtp.example.com",
                "smtp_port": 587,
                "smtp_user": "",
                "smtp_password": "",
                "sender_email": "",
                "receiver_emails": []
            }
        }
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            return default_config

    def generate_report(self, market_updates: Dict[str, Any]) -> str:
        """生成完整的日报内容"""
        markdown = f"""# 📊 亚马逊美国站假发/美妆类目运营日报
**日期：{self.date}**

---

## 1️⃣ 【平台规则与政策变动】

### 🔴 高优先级变动
| 变动内容 | 来源 | 生效时间 | 对假发运营的影响 |
|---------|------|---------|-----------------|
"""
        
        for update in market_updates.get("high_priority_changes", []):
            markdown += f"| {update['content']} | {update['source']} | {update['effective_date']} | {update['impact']} |\n"
        
        markdown += "\n### 🟡 中优先级变动\n"
        for update in market_updates.get("medium_priority_changes", []):
            markdown += f"- **{update['title']}**：{update['description']}\n"
        
        markdown += "\n---\n\n## 2️⃣ 【亚马逊活动与促销信息】\n\n### 🎉 当前进行中活动\n| 活动名称 | 时间 | 假发/美妆参与机会 |\n|---------|------|------------------|\n"
        
        for event in market_updates.get("ongoing_events", []):
            markdown += f"| {event['name']} | {event['time']} | {event['opportunity']} |\n"
        
        markdown += "\n### 📅 即将到来活动\n| 活动名称 | 时间 | 提报截止/入仓要求 | 假发运营建议 |\n|---------|------|-----------------|------------|\n"
        
        for event in market_updates.get("upcoming_events", []):
            markdown += f"| {event['name']} | {event['time']} | {event['deadline']} | {event['recommendation']} |\n"
        
        markdown += "\n---\n\n## 3️⃣ 【美国市场与消费节点】\n\n### 📅 未来30天重要节日\n| 日期 | 节日/事件 | 假发推广机会 |\n|------|----------|------------|\n"
        
        for holiday in market_updates.get("holidays", []):
            markdown += f"| {holiday['date']} | {holiday['name']} | {holiday['opportunity']} |\n"
        
        markdown += "\n### 📈 消费趋势\n"
        for trend in market_updates.get("trends", []):
            markdown += f"- {trend}\n"
        
        markdown += "\n---\n\n## ✅ 【今日关键行动项】\n\n"
        for i, action in enumerate(market_updates.get("action_items", []), 1):
            markdown += f"{i}. **{action['title']}**：{action['description']}\n"
        
        markdown += "\n---\n\n**以上信息仅供参考，请以Amazon Seller Central官方通知为准。**"
        
        return markdown

    def generate_text_report(self, market_updates: Dict[str, Any]) -> str:
        """生成纯文本格式的日报（用于邮件和飞书推送）"""
        text = f"📊 亚马逊美国站假发/美妆类目运营日报\n"
        text += f"日期：{self.date}\n"
        text += "="*50 + "\n\n"
        
        text += "1️⃣ 【平台规则与政策变动】\n"
        text += "🔴 高优先级变动：\n"
        for update in market_updates.get("high_priority_changes", []):
            text += f"  - {update['content']}\n"
            text += f"    来源：{update['source']} | 生效时间：{update['effective_date']}\n"
            text += f"    影响：{update['impact']}\n"
        
        text += "\n🟡 中优先级变动：\n"
        for update in market_updates.get("medium_priority_changes", []):
            text += f"  - {update['title']}：{update['description']}\n"
        
        text += "\n" + "="*50 + "\n\n"
        text += "2️⃣ 【亚马逊活动与促销信息】\n"
        
        text += "🎉 当前进行中活动：\n"
        for event in market_updates.get("ongoing_events", []):
            text += f"  - {event['name']}（{event['time']}）\n"
            text += f"    参与机会：{event['opportunity']}\n"
        
        text += "\n📅 即将到来活动：\n"
        for event in market_updates.get("upcoming_events", []):
            text += f"  - {event['name']}（{event['time']}）\n"
            text += f"    截止/入仓：{event['deadline']}\n"
            text += f"    运营建议：{event['recommendation']}\n"
        
        text += "\n" + "="*50 + "\n\n"
        text += "3️⃣ 【美国市场与消费节点】\n"
        
        text += "📅 未来30天重要节日：\n"
        for holiday in market_updates.get("holidays", []):
            text += f"  - {holiday['date']} {holiday['name']}：{holiday['opportunity']}\n"
        
        text += "\n📈 消费趋势：\n"
        for trend in market_updates.get("trends", []):
            text += f"  - {trend}\n"
        
        text += "\n" + "="*50 + "\n\n"
        text += "✅ 【今日关键行动项】\n"
        for i, action in enumerate(market_updates.get("action_items", []), 1):
            text += f"{i}. {action['title']}：{action['description']}\n"
        
        text += "\n" + "="*50 + "\n"
        text += "以上信息仅供参考，请以Amazon Seller Central官方通知为准。"
        
        return text

    def save_report(self, content: str, filename: str = "amazon_daily_report.md"):
        """保存日报到文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 日报已保存至 {filename}")

    def send_to_feishu(self, content: str, webhook_url: Optional[str] = None) -> bool:
        """通过飞书Webhook推送日报"""
        url = webhook_url or self.config.get("feishu_webhook_url", "")
        
        if not url:
            print("❌ 飞书Webhook URL未配置，请在report_config.json中设置")
            return False
        
        try:
            data = {
                "msg_type": "text",
                "content": {
                    "text": content
                }
            }
            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status()
            print("✅ 飞书消息推送成功！")
            return True
        except Exception as e:
            print(f"❌ 飞书消息推送失败：{str(e)}")
            return False

    def send_email(self, content: str, subject: Optional[str] = None) -> bool:
        """发送邮件日报"""
        email_config = self.config.get("email", {})
        
        smtp_server = email_config.get("smtp_server", "")
        smtp_port = email_config.get("smtp_port", 587)
        smtp_user = email_config.get("smtp_user", "")
        smtp_password = email_config.get("smtp_password", "")
        sender_email = email_config.get("sender_email", "")
        receiver_emails = email_config.get("receiver_emails", [])
        
        if not all([smtp_server, smtp_user, smtp_password, sender_email, receiver_emails]):
            print("❌ 邮件配置不完整，请在report_config.json中设置")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = Header(sender_email, 'utf-8')
            msg['To'] = Header(",".join(receiver_emails), 'utf-8')
            msg['Subject'] = Header(subject or f"【亚马逊运营日报】{self.date}", 'utf-8')
            
            msg.attach(MIMEText(content, 'plain', 'utf-8'))
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(sender_email, receiver_emails, msg.as_string())
            
            print("✅ 邮件发送成功！")
            return True
        except Exception as e:
            print(f"❌ 邮件发送失败：{str(e)}")
            return False


def get_sample_market_updates() -> Dict[str, Any]:
    """获取示例市场更新数据（实际使用时可替换为网络爬取或API调用）"""
    return {
        "high_priority_changes": [
            {
                "content": "FBA履约费用与商品价格挂钩",
                "source": "Amazon FBA Fee Changes 2026",
                "effective_date": "2026年1月15日已生效",
                "impact": "假发类目平均客单价$30-50区间，履约费上涨6-8%，成本压力增大。建议优化定价策略"
            },
            {
                "content": "Buy with Prime及多渠道履约附加费扩展",
                "source": "5月新规",
                "effective_date": "2026年5月2日",
                "impact": "增加3.5%附加费，平均每件商品约增加$0.17。叠加超龄库存费后，综合成本可能上涨10%-15%"
            },
            {
                "content": "价格抓取规则收紧",
                "source": "5月新规",
                "effective_date": "2026年5月18日",
                "impact": "List Price与Typical Price计算方式调整，需注意价格历史记录，避免影响活动效果"
            }
        ],
        "medium_priority_changes": [
            {
                "title": "FBA移除费实时扣费",
                "description": "美国站已于2月15日实施，建议合理规划移除节奏，避免短期费用激增"
            },
            {
                "title": "Placement费用上涨",
                "description": "单点入仓费用上涨6-179%，建议拆分发货到多个仓库"
            }
        ],
        "ongoing_events": [
            {
                "name": "Amazon Pet Days宠物日",
                "time": "5月11-15日",
                "opportunity": "首次延长至5天，面向所有消费者开放。可布局宠物造型假发、宠物美容护理周边"
            }
        ],
        "upcoming_events": [
            {
                "name": "Memorial Day阵亡将士纪念日大促",
                "time": "5月15-25日",
                "deadline": "现已开启",
                "recommendation": "最高55%折扣，布局夏季发型、泳池/户外主题假发"
            },
            {
                "name": "Prime Day 2026",
                "time": "6月（具体日期待公布）",
                "deadline": "5月26日Best Deal/秒杀提报截止；单点入仓5月27日前",
                "recommendation": "重中之重！提前备货，优化Listing，准备Prime Day专属套装"
            }
        ],
        "holidays": [
            {"date": "5月18日", "name": "价格规则调整日", "opportunity": "检查所有Listing价格历史"},
            {"date": "5月26日", "name": "Prime Day提报截止日", "opportunity": "务必按时提报"},
            {"date": "6月1日", "name": "国际儿童节", "opportunity": "儿童假发、cosplay造型"},
            {"date": "6月21日", "name": "父亲节", "opportunity": "男士商务/休闲造型"}
        ],
        "trends": [
            "夏季消费转向户外：泳池派对、海滩度假主题假发需求上升",
            "Prime Day前置到6月：备战周期缩短，节奏加快，需立即行动",
            "宠物经济持续增长：Amazon Pet Days延长至5天，宠物周边值得布局"
        ],
        "action_items": [
            {
                "title": "立即检查Listing价格历史",
                "description": "确保过去90天低价天数不超过45天，避免影响Prime Day促销效果"
            },
            {
                "title": "确认Prime Day提报计划",
                "description": "5月26日截止，务必本周内完成提报"
            },
            {
                "title": "调整FBA发货计划",
                "description": "采用分仓策略，避免高额Placement费用；确保货物在5月27日前入仓"
            }
        ]
    }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='亚马逊运营日报生成器')
    parser.add_argument('--feishu', action='store_true', help='发送到飞书')
    parser.add_argument('--email', action='store_true', help='发送邮件')
    parser.add_argument('--webhook', type=str, help='飞书Webhook URL（优先使用命令行参数）')
    args = parser.parse_args()
    
    print("🚀 正在生成亚马逊市场运营日报...")
    
    report_generator = AmazonDailyReport()
    market_updates = get_sample_market_updates()
    
    # 生成Markdown格式（保存文件）
    markdown_content = report_generator.generate_report(market_updates)
    report_generator.save_report(markdown_content)
    
    # 生成文本格式（用于推送）
    text_content = report_generator.generate_text_report(market_updates)
    
    # 输出日报内容
    print("\n" + "="*60)
    print(text_content)
    print("="*60)
    
    # 发送到飞书
    if args.feishu:
        report_generator.send_to_feishu(text_content, args.webhook)
    
    # 发送邮件
    if args.email:
        report_generator.send_email(text_content)
    
    print("\n✅ 日报生成完成！")
