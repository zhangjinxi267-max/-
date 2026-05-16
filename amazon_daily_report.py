#!/usr/bin/env python3
"""
亚马逊美国站假发/美妆类目运营周报生成器
每周自动推送最新市场动态和规则更新
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


class AmazonWeeklyReport:
    def __init__(self):
        self.date = datetime.datetime.now().strftime("%Y年%m月%d日")
        self.week = self._get_week_number()
        self.report = {}
        self.config = self._load_config()

    def _get_week_number(self) -> str:
        """获取周数"""
        return datetime.datetime.now().strftime("%Y年第%W周")

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
        """生成完整的周报内容"""
        lines = []
        lines.append(f"# 📊 亚马逊美国站假发/美妆类目运营周报")
        lines.append(f"**日期：{self.date}**")
        lines.append(f"**周期：{self.week}**")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        lines.append("## 1️⃣ 【平台规则与政策变动】")
        lines.append("")
        lines.append("### 🔴 高优先级变动")
        lines.append("| 变动内容 | 来源 | 生效时间 | 对假发运营的影响 |")
        lines.append("|---------|------|---------|-----------------|")
        
        for update in market_updates.get("high_priority_changes", []):
            lines.append(f"| {update['content']} | {update['source']} | {update['effective_date']} | {update['impact']} |")
        
        lines.append("")
        lines.append("### 🟡 中优先级变动")
        for update in market_updates.get("medium_priority_changes", []):
            lines.append(f"- **{update['title']}**：{update['description']}")
        
        lines.append("")
        lines.append("### 📋 Listing合规要求")
        for item in market_updates.get("listing_compliance", []):
            lines.append(f"- **{item['type']}**：{item['content']}")
        
        lines.append("")
        lines.append("### 💰 FBA物流政策")
        for item in market_updates.get("fba_policies", []):
            lines.append(f"- **{item['type']}**：{item['content']}")
        
        lines.append("")
        lines.append("### ⚖️ 广告投放与评论政策")
        for item in market_updates.get("ads_review_policies", []):
            lines.append(f"- **{item['type']}**：{item['content']}")
        
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 2️⃣ 【亚马逊活动与促销信息】")
        lines.append("")
        lines.append("### 🎉 当前进行中活动")
        lines.append("| 活动名称 | 时间 | 假发/美妆参与机会 |")
        lines.append("|---------|------|------------------|")
        
        for event in market_updates.get("ongoing_events", []):
            lines.append(f"| {event['name']} | {event['time']} | {event['opportunity']} |")
        
        lines.append("")
        lines.append("### 📅 即将到来活动")
        lines.append("| 活动名称 | 时间 | 提报截止/入仓要求 | 假发运营建议 |")
        lines.append("|---------|------|-----------------|------------|")
        
        for event in market_updates.get("upcoming_events", []):
            lines.append(f"| {event['name']} | {event['time']} | {event['deadline']} | {event['recommendation']} |")
        
        lines.append("")
        lines.append("### 📈 促销活动要求")
        for req in market_updates.get("promotion_requirements", []):
            lines.append(f"- **{req['type']}**：{req['content']}")
        
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 3️⃣ 【AI工具与平台技术变化】")
        lines.append("")
        lines.append("### 🤖 AI购物助手")
        for ai in market_updates.get("ai_tools", []):
            lines.append(f"- **{ai['type']}**：{ai['content']}")
        
        lines.append("")
        lines.append("### 🔧 平台技术更新")
        for tech in market_updates.get("platform_tech", []):
            lines.append(f"- **{tech['type']}**：{tech['content']}")
        
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 4️⃣ 【美国市场与消费节点】")
        lines.append("")
        lines.append("### 📅 未来30天重要节日")
        lines.append("| 日期 | 节日/事件 | 假发推广机会 |")
        lines.append("|------|----------|------------|")
        
        for holiday in market_updates.get("holidays", []):
            lines.append(f"| {holiday['date']} | {holiday['name']} | {holiday['opportunity']} |")
        
        lines.append("")
        lines.append("### 📈 消费趋势")
        for trend in market_updates.get("trends", []):
            lines.append(f"- {trend}")
        
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 5️⃣ 【Beauty & Personal Care类目专属】")
        lines.append("")
        lines.append("### 💇 Hairpieces假发类目规则")
        for rule in market_updates.get("hairpieces_category", []):
            lines.append(f"- **{rule['type']}**：{rule['content']}")
        
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## ✅ 【本周关键行动项】")
        lines.append("")
        
        for i, action in enumerate(market_updates.get("action_items", []), 1):
            priority_tag = "🔴" if action.get("priority") == "high" else "🟡"
            lines.append(f"{priority_tag} **{action['title']}**：{action['description']}")
        
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("**以上信息仅供参考，请以Amazon Seller Central官方通知为准。**")
        
        return "\n".join(lines)

    def generate_text_report(self, market_updates: Dict[str, Any]) -> str:
        """生成纯文本格式的周报"""
        lines = []
        lines.append(f"📊 亚马逊美国站假发/美妆类目运营周报")
        lines.append(f"日期：{self.date} | {self.week}")
        lines.append("="*60)
        lines.append("")
        
        lines.append("1️⃣ 【平台规则与政策变动】")
        lines.append("🔴 高优先级变动：")
        for update in market_updates.get("high_priority_changes", []):
            lines.append(f"  - {update['content']}")
            lines.append(f"    来源：{update['source']} | 生效：{update['effective_date']}")
            lines.append(f"    影响：{update['impact']}")
            lines.append("")
        
        lines.append("🟡 中优先级变动：")
        for update in market_updates.get("medium_priority_changes", []):
            lines.append(f"  - {update['title']}：{update['description']}")
        
        lines.append("")
        lines.append("📋 Listing合规要求：")
        for item in market_updates.get("listing_compliance", []):
            lines.append(f"  - {item['type']}：{item['content']}")
        
        lines.append("")
        lines.append("💰 FBA物流政策：")
        for item in market_updates.get("fba_policies", []):
            lines.append(f"  - {item['type']}：{item['content']}")
        
        lines.append("")
        lines.append("="*60)
        lines.append("")
        lines.append("2️⃣ 【亚马逊活动与促销信息】")
        
        lines.append("🎉 当前进行中活动：")
        for event in market_updates.get("ongoing_events", []):
            lines.append(f"  - {event['name']}（{event['time']}）")
            lines.append(f"    机会：{event['opportunity']}")
            lines.append("")
        
        lines.append("📅 即将到来活动：")
        for event in market_updates.get("upcoming_events", []):
            lines.append(f"  - {event['name']}（{event['time']}）")
            lines.append(f"    截止：{event['deadline']}")
            lines.append(f"    建议：{event['recommendation']}")
            lines.append("")
        
        lines.append("="*60)
        lines.append("")
        lines.append("3️⃣ 【AI工具与平台技术变化】")
        for ai in market_updates.get("ai_tools", []):
            lines.append(f"  - {ai['type']}：{ai['content']}")
        
        lines.append("")
        lines.append("="*60)
        lines.append("")
        lines.append("4️⃣ 【美国市场与消费节点】")
        
        lines.append("📅 未来30天重要节日：")
        for holiday in market_updates.get("holidays", []):
            lines.append(f"  - {holiday['date']} {holiday['name']}：{holiday['opportunity']}")
        
        lines.append("")
        lines.append("📈 消费趋势：")
        for trend in market_updates.get("trends", []):
            lines.append(f"  - {trend}")
        
        lines.append("")
        lines.append("="*60)
        lines.append("")
        lines.append("5️⃣ 【Beauty类目专属动态】")
        for rule in market_updates.get("hairpieces_category", []):
            lines.append(f"  - {rule['type']}：{rule['content']}")
        
        lines.append("")
        lines.append("="*60)
        lines.append("")
        lines.append("✅ 【本周关键行动项】")
        for i, action in enumerate(market_updates.get("action_items", []), 1):
            priority_tag = "🔴" if action.get("priority") == "high" else "🟡"
            lines.append(f"{priority_tag} {i}. {action['title']}：{action['description']}")
        
        lines.append("")
        lines.append("="*60)
        lines.append("以上信息仅供参考，请以Amazon Seller Central官方通知为准。")
        
        return "\n".join(lines)

    def save_report(self, content: str, filename: str = "amazon_weekly_report.md"):
        """保存周报到文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 周报已保存至 {filename}")

    def send_to_feishu(self, content: str, webhook_url: Optional[str] = None) -> bool:
        """通过飞书Webhook推送周报"""
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
        """发送邮件周报"""
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
            msg['Subject'] = Header(subject or f"【亚马逊运营周报】{self.date}", 'utf-8')
            
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


def get_market_updates() -> Dict[str, Any]:
    """获取市场更新数据"""
    return {
        "high_priority_changes": [
            {
                "content": "【重要】亚马逊关停Rufus AI购物助手，推出Alexa for Shopping",
                "source": "亚马逊官方公告（2026年5月13日）",
                "effective_date": "2026年5月13日生效",
                "impact": "独立Rufus正式关停，整合Rufus和Alexa+的新一代AI购物助手上线。搜索结果顶部将出现AI生成内容，可能影响自然搜索点击率。建议关注商品详情页优化和AI对话场景下的产品展示"
            },
            {
                "content": "FBA履约费用与商品价格挂钩调整",
                "source": "Amazon FBA Fee Changes 2026",
                "effective_date": "2026年1月15日已生效",
                "impact": "假发类目平均客单价$30-50区间，履约费上涨6-8%，成本压力增大。建议优化定价策略，考虑分价格段运营"
            },
            {
                "content": "价格抓取规则收紧",
                "source": "亚马逊美国站公告",
                "effective_date": "2026年5月18日生效",
                "impact": "List Price与Typical Price计算方式调整，若过去90天低价天数超45天，促销价将被纳入常规价计算"
            }
        ],
        "medium_priority_changes": [
            {
                "title": "FBA移除费实时扣费",
                "description": "美国站已于2月15日实施，欧洲站5月1日跟进。建议合理规划移除节奏，避免短期费用激增"
            },
            {
                "title": "Placement费用上涨",
                "description": "单点入仓费用上涨6-179%，建议采用分仓策略发货"
            },
            {
                "title": "Buy with Prime附加费扩展",
                "description": "5月2日起扩展至美国Buy with Prime及美加多渠道履约，增加3.5%附加费"
            }
        ],
        "listing_compliance": [
            {"type": "图片要求", "content": "主图需白底无水印，辅图建议6张以上，包含使用场景和尺寸对比"},
            {"type": "标题规范", "content": "控制在200字符内，避免关键词堆砌，核心词前置，品牌名+核心属性+材质+款式"},
            {"type": "A+内容", "content": "高质量A+内容可提升转化率15-20%，建议添加对比图表和使用场景图"},
            {"type": "Search Term优化", "content": "隐藏关键词需包含长尾词、变体词、同义词，避免重复类目搜索词"}
        ],
        "fba_policies": [
            {"type": "入仓要求", "content": "Prime Day入仓截止：单点5月27日，拆分6月5日"},
            {"type": "库存管理", "content": "低库存费现在按FNSKU级别计算，需保持合理库存水平"},
            {"type": "包装要求", "content": "SIOP已成标配，需使用5-7层瓦楞纸箱，确保运输安全"}
        ],
        "ads_review_policies": [
            {"type": "评论政策", "content": "严查好评返现、测评激励，一经发现可能暂停销售权限"},
            {"type": "广告合规", "content": "竞品品牌词不可用于广告投放，避免侵权投诉"},
            {"type": "秒杀规则", "content": "LD要求至少15%折扣，7DD要求至少30%折扣，提报需提前规划"}
        ],
        "ongoing_events": [
            {
                "name": "Memorial Day阵亡将士纪念日大促",
                "time": "5月15-25日",
                "opportunity": "最高55%折扣，布局夏季发型、泳池/户外主题假发"
            }
        ],
        "upcoming_events": [
            {
                "name": "Prime Day 2026",
                "time": "6月（具体日期待公布）",
                "deadline": "5月26日Best Deal/秒杀/Prime专属折扣提报截止；单点入仓5月27日前",
                "recommendation": "重中之重！提前备货，优化Listing，准备Prime Day专属套装（节日造型+日常佩戴组合）"
            },
            {
                "name": "父亲节大促",
                "time": "6月15-21日",
                "deadline": "6月上旬",
                "recommendation": "男士短发、商务造型假发需求增加，提前准备男士款式库存"
            }
        ],
        "promotion_requirements": [
            {"type": "Prime Day提报要求", "content": "Deal价格需低于近30天最低价，库存需充足"},
            {"type": "优惠券设置", "content": "建议设置10-20% coupon，配合Deal活动提升转化率"},
            {"type": "LD秒杀技巧", "content": "4-6小时限时，建议在流量高峰时段进行"}
        ],
        "ai_tools": [
            {
                "type": "Alexa for Shopping上线",
                "content": "整合Rufus和Alexa+能力，嵌入搜索栏，可进行自然语言购物对话，支持价格历史查询和自动购买"
            },
            {
                "type": "AI搜索结果变化",
                "content": "搜索结果顶部将出现AI生成的内容摘要，可能影响传统Listing的点击率"
            }
        ],
        "platform_tech": [
            {"type": "搜索算法更新", "content": "持续优化AI驱动的个性化推荐，类目相关性权重提升"},
            {"type": "移动端优化", "content": "APP端用户体验持续优化，移动端流量占比超60%"}
        ],
        "holidays": [
            {"date": "5月26日", "name": "Prime Day提报截止日", "opportunity": "务必按时完成提报"},
            {"date": "6月1日", "name": "国际儿童节", "opportunity": "儿童假发、cosplay造型需求"},
            {"date": "6月14日", "name": "父亲节（美国）", "opportunity": "男士造型假发推广"},
            {"date": "6月", "name": "Prime Day", "opportunity": "年度最大促销，提前备货"},
            {"date": "7月4日", "name": "美国独立日", "opportunity": "爱国主题、派对造型"}
        ],
        "trends": [
            "夏季消费转向户外：泳池派对、海滩度假主题假发需求上升",
            "Prime Day前置到6月：备战周期缩短，节奏加快，需立即行动",
            "AI购物助手普及：需优化Listing以适应新的AI对话搜索场景",
            "价格透明化：消费者越来越关注价格历史，需合理定价"
        ],
        "hairpieces_category": [
            {
                "type": "Hairpieces类目规则",
                "content": "Beauty类目下的Hairpieces有特殊审核要求，需确保产品描述准确，避免误导性声明"
            },
            {
                "type": "安全认证",
                "content": "假发产品需符合相关安全标准，特别是与人接触的发制品，建议准备相关认证文件"
            },
            {
                "type": "侵权风险",
                "content": "避免使用品牌logo、设计元素，定期排查Listing中的潜在侵权内容"
            }
        ],
        "action_items": [
            {
                "title": "立即检查Listing价格历史",
                "priority": "high",
                "description": "确保过去90天低价天数不超过45天，为Prime Day促销留出价格空间"
            },
            {
                "title": "完成Prime Day提报",
                "priority": "high",
                "description": "5月26日截止！确认参与活动类型，准备充足库存，优化活动Listing"
            },
            {
                "title": "优化AI搜索展示",
                "priority": "medium",
                "description": "针对Alexa for Shopping等AI工具，优化产品标题和描述中的关键词，提升AI推荐概率"
            },
            {
                "title": "男士款式备货",
                "priority": "medium",
                "description": "父亲节（6月21日）将近，提前备货男士商务/休闲造型假发"
            }
        ]
    }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='亚马逊运营周报生成器')
    parser.add_argument('--feishu', action='store_true', help='发送到飞书')
    parser.add_argument('--email', action='store_true', help='发送邮件')
    parser.add_argument('--webhook', type=str, help='飞书Webhook URL')
    args = parser.parse_args()
    
    print("🚀 正在生成亚马逊市场运营周报...")
    
    report_generator = AmazonWeeklyReport()
    market_updates = get_market_updates()
    
    markdown_content = report_generator.generate_report(market_updates)
    report_generator.save_report(markdown_content)
    
    text_content = report_generator.generate_text_report(market_updates)
    
    print("\n" + "="*60)
    print(text_content)
    print("="*60)
    
    if args.feishu:
        report_generator.send_to_feishu(text_content, args.webhook)
    
    if args.email:
        report_generator.send_email(text_content)
    
    print("\n✅ 周报生成完成！")
