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
            "feishu_webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/a4fd940c-2d0f-430b-9a40-613457f14c67",
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

    def generate_simple_report(self, market_updates: Dict[str, Any]) -> str:
        """生成简洁版日报"""
        text = f"📊 亚马逊日报 | {self.date}\n\n"
        
        # 平台规则变动
        if market_updates.get("high_priority_changes"):
            text += "【平台动态】\n"
            for update in market_updates["high_priority_changes"][:3]:
                text += f"• {update['content']}\n"
                text += f"  影响：{update['impact']}\n\n"
        
        # 活动信息
        if market_updates.get("upcoming_events"):
            text += "【活动提醒】\n"
            for event in market_updates["upcoming_events"][:2]:
                text += f"• {event['name']}：{event['deadline']}\n"
        
        # 行动项
        if market_updates.get("action_items"):
            text += "\n【今日行动】\n"
            for i, action in enumerate(market_updates["action_items"][:3], 1):
                text += f"{i}. {action['title']}\n"
        
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
            print("❌ 飞书Webhook URL未配置")
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
            print("❌ 邮件配置不完整")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = Header(sender_email, 'utf-8')
            msg['To'] = Header(",".join(receiver_emails), 'utf-8')
            msg['Subject'] = Header(subject or f"【亚马逊日报】{self.date}", 'utf-8')
            
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
    """获取示例市场更新数据"""
    return {
        "high_priority_changes": [
            {
                "content": "亚马逊关停Rufus AI，推出Alexa for Shopping",
                "source": "亚马逊官方公告",
                "effective_date": "2026年5月13日",
                "impact": "搜索结果顶部将出现AI生成内容，可能影响自然点击率。需优化Listing和A+内容"
            },
            {
                "content": "FBA履约费与商品价格挂钩",
                "source": "FBA Fee 2026",
                "effective_date": "已生效",
                "impact": "$30-50客单价区间履约费上涨6-8%"
            },
            {
                "content": "价格规则调整",
                "source": "5月新规",
                "effective_date": "2026年5月18日",
                "impact": "检查90天内价格历史，避免影响促销效果"
            }
        ],
        "medium_priority_changes": [
            {
                "title": "FBA移除费实时扣费",
                "description": "合理规划库存移除节奏"
            },
            {
                "title": "Placement费用上涨",
                "description": "建议拆分发货到多仓库"
            }
        ],
        "ongoing_events": [
            {
                "name": "Pet Days宠物日",
                "time": "5月11-15日",
                "opportunity": "5天延长活动，面向所有消费者"
            }
        ],
        "upcoming_events": [
            {
                "name": "Memorial Day大促",
                "time": "5月15-25日",
                "deadline": "现已开启",
                "recommendation": "布局夏季发型主题假发"
            },
            {
                "name": "Prime Day 2026",
                "time": "6月",
                "deadline": "5月26日提报截止",
                "recommendation": "提前备货，优化Listing"
            }
        ],
        "holidays": [
            {"date": "5月18日", "name": "价格规则调整", "opportunity": "检查Listing价格历史"},
            {"date": "5月26日", "name": "Prime Day提报截止", "opportunity": "完成提报"},
            {"date": "6月1日", "name": "国际儿童节", "opportunity": "儿童假发、cosplay"},
            {"date": "6月21日", "name": "父亲节", "opportunity": "男士造型假发"}
        ],
        "trends": [
            "夏季户外主题假发需求上升",
            "Prime Day备战需立即行动",
            "宠物经济持续增长"
        ],
        "action_items": [
            {
                "title": "检查价格历史",
                "description": "确保90天内低价天数<45天"
            },
            {
                "title": "完成Prime Day提报",
                "description": "5月26日截止"
            },
            {
                "title": "调整FBA发货",
                "description": "分仓策略，避免Placement费用"
            }
        ]
    }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='亚马逊运营日报生成器')
    parser.add_argument('--feishu', action='store_true', help='发送到飞书')
    parser.add_argument('--email', action='store_true', help='发送邮件')
    parser.add_argument('--webhook', type=str, help='飞书Webhook URL')
    args = parser.parse_args()
    
    print("🚀 正在生成亚马逊市场运营日报...")
    
    report_generator = AmazonDailyReport()
    market_updates = get_sample_market_updates()
    
    # 生成简洁版日报
    report_content = report_generator.generate_simple_report(market_updates)
    
    # 输出日报
    print("\n" + "="*60)
    print(report_content)
    print("="*60)
    
    # 保存文件
    report_generator.save_report(report_content)
    
    # 发送到飞书
    if args.feishu:
        report_generator.send_to_feishu(report_content, args.webhook)
    
    # 发送邮件
    if args.email:
        report_generator.send_email(report_content)
    
    print("\n✅ 日报生成完成！")
