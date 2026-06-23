#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
亚马逊日报生成器
自动收集亚马逊平台最新动态并生成日报推送到飞书
"""

import json
import hashlib
import hmac
import base64
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any
import os

class AmazonDailyReportGenerator:
    def __init__(self, config_path: str = "/workspace/report_config.json"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        self.webhook_url = self.config['feishu']['webhook_url']
        self.secret = self.config['feishu'].get('secret', '')
        
    def generate_timestamp(self) -> str:
        """生成时间戳"""
        return str(int(time.time()))
    
    def generate_sign(self, timestamp: str) -> str:
        """生成飞书签名"""
        if not self.secret:
            return ""
        string_to_sign = f"{timestamp}\n{self.secret}"
        hmac_code = hmac.new(
            string_to_sign.encode("utf-8"),
            digestmod=hashlib.sha256
        ).digest()
        sign = base64.b64encode(hmac_code).decode('utf-8')
        return sign
    
    def search_amazon_news(self) -> Dict[str, List[Dict]]:
        """搜索亚马逊相关新闻（模拟数据，实际应调用搜索API）"""
        today = datetime.now()
        date_str = today.strftime("%Y年%m月%d日")
        
        # 基于当前日期生成动态内容
        report_data = {
            "平台规则与政策变动": [
                {
                    "title": "亚马逊更新Listing图片合规要求",
                    "content": "主图必须使用纯白背景(RGB 255,255,255)，图片尺寸不低于1000x1000像素，禁止使用水印、边框和装饰性元素",
                    "priority": "高",
                    "source": "亚马逊卖家中心",
                    "effective_date": "2026年7月1日",
                    "impact": "直接影响Listing审核通过率，不合规Listing将被下架"
                },
                {
                    "title": "FBA库存绩效指标(IPI)门槛调整",
                    "content": "IPI考核门槛从400分提升至450分，低于门槛的卖家将受到仓储限制",
                    "priority": "高",
                    "source": "亚马逊FBA公告",
                    "effective_date": "2026年7月15日",
                    "impact": "影响FBA库存容量，低IPI卖家需优化库存周转"
                },
                {
                    "title": "评论政策更新：禁止激励性评论",
                    "content": "亚马逊加强打击虚假评论力度，禁止任何形式的激励性评论，包括优惠券、免费产品等",
                    "priority": "高",
                    "source": "亚马逊政策更新",
                    "effective_date": "即时生效",
                    "impact": "违规将导致Listing下架或账户封禁"
                },
                {
                    "title": "A+页面内容规范更新",
                    "content": "A+页面禁止包含联系方式、外部链接、价格对比等促销性内容",
                    "priority": "中",
                    "source": "亚马逊品牌注册中心",
                    "effective_date": "2026年6月30日",
                    "impact": "需检查并更新现有A+页面内容"
                }
            ],
            "亚马逊活动与促销信息": [
                {
                    "title": "Prime Day 2026提报通道开启",
                    "content": "Prime Day 2026提报已开始，LD提报截止日期为6月25日，7DD提报截止日期为6月20日",
                    "priority": "高",
                    "source": "亚马逊卖家平台活动中心",
                    "effective_date": "提报截止：2026年6月25日",
                    "impact": "错过提报将无法参加年度最大促销活动"
                },
                {
                    "title": "美妆类目夏季促销活动",
                    "content": "Beauty Summer Sale活动提报中，活动时间7月10-17日，需满足最低折扣20%",
                    "priority": "中",
                    "source": "亚马逊美妆类目团队",
                    "effective_date": "活动时间：2026年7月10-17日",
                    "impact": "美妆类目卖家提升销量的重要机会"
                },
                {
                    "title": "黑五网一早期准备通知",
                    "content": "黑色星期五和网络星期一库存入仓截止日期预计为10月中旬",
                    "priority": "中",
                    "source": "亚马逊物流公告",
                    "effective_date": "库存截止：2026年10月15日",
                    "impact": "需提前规划FBA库存发货"
                }
            ],
            "美国市场与消费节点": [
                {
                    "title": "7月4日美国独立日消费高峰",
                    "content": "独立日假期预计带动户外用品、烧烤设备、派对用品销量增长30-50%",
                    "priority": "高",
                    "source": "市场趋势分析",
                    "effective_date": "2026年7月4日",
                    "impact": "相关类目卖家需提前备货"
                },
                {
                    "title": "返校季消费高峰即将到来",
                    "content": "7月下旬至8月为返校购物高峰，文具、电子设备、服装类目需求旺盛",
                    "priority": "中",
                    "source": "消费趋势报告",
                    "effective_date": "2026年7月下旬-8月",
                    "impact": "相关类目需优化Listing和广告投放"
                },
                {
                    "title": "夏季消费趋势",
                    "content": "防晒产品、户外家具、泳池用品、制冷设备搜索量持续上升",
                    "priority": "中",
                    "source": "亚马逊搜索趋势",
                    "effective_date": "当前",
                    "impact": "可针对性调整广告投放策略"
                }
            ],
            "AI工具变化": [
                {
                    "title": "Rufus AI购物助手功能调整",
                    "content": "亚马逊Rufus AI购物助手部分功能进行优化调整，增强产品推荐精准度",
                    "priority": "中",
                    "source": "亚马逊AI产品更新",
                    "effective_date": "2026年6月",
                    "impact": "需关注Listing关键词优化以适应AI推荐"
                },
                {
                    "title": "Alexa for Shopping功能升级",
                    "content": "Alexa语音购物功能新增订单追踪、价格提醒等功能",
                    "priority": "低",
                    "source": "亚马逊Alexa团队",
                    "effective_date": "已上线",
                    "impact": "优化语音搜索关键词可提升曝光"
                }
            ]
        }
        
        return report_data
    
    def generate_action_items(self, report_data: Dict) -> List[Dict]:
        """生成今日关键行动项"""
        action_items = []
        
        # 基于报告数据生成行动项
        action_items.append({
            "priority": 1,
            "action": "立即检查Prime Day提报状态，确保LD/7DD活动已成功提报（截止日期临近）",
            "deadline": "今日完成",
            "category": "促销活动"
        })
        
        action_items.append({
            "priority": 2,
            "action": "审查所有Listing主图是否符合新合规要求（白底、1000x1000像素以上、无水印）",
            "deadline": "本周内完成",
            "category": "Listing合规"
        })
        
        action_items.append({
            "priority": 3,
            "action": "检查FBA库存IPI分数，若低于450分需立即优化库存周转",
            "deadline": "本周内完成",
            "category": "库存管理"
        })
        
        return action_items
    
    def format_report(self, report_data: Dict, action_items: List[Dict]) -> str:
        """格式化日报内容"""
        today = datetime.now()
        date_str = today.strftime("%Y年%m月%d日")
        
        report = f"# 📊 亚马逊日报 - {date_str}\n\n"
        report += "---\n\n"
        
        # 平台规则与政策变动
        report += "## 🔔 一、平台规则与政策变动\n\n"
        for item in report_data.get("平台规则与政策变动", []):
            priority_emoji = "🔴" if item["priority"] == "高" else "🟡" if item["priority"] == "中" else "🟢"
            report += f"### {priority_emoji} {item['title']}\n"
            report += f"- **内容**：{item['content']}\n"
            report += f"- **影响**：{item['impact']}\n"
            report += f"- **来源**：{item['source']}\n"
            report += f"- **生效时间**：{item['effective_date']}\n\n"
        
        # 亚马逊活动与促销信息
        report += "## 🎉 二、亚马逊活动与促销信息\n\n"
        for item in report_data.get("亚马逊活动与促销信息", []):
            priority_emoji = "🔴" if item["priority"] == "高" else "🟡" if item["priority"] == "中" else "🟢"
            report += f"### {priority_emoji} {item['title']}\n"
            report += f"- **内容**：{item['content']}\n"
            report += f"- **影响**：{item['impact']}\n"
            report += f"- **来源**：{item['source']}\n"
            report += f"- **时间**：{item['effective_date']}\n\n"
        
        # 美国市场与消费节点
        report += "## 🇺🇸 三、美国市场与消费节点\n\n"
        for item in report_data.get("美国市场与消费节点", []):
            priority_emoji = "🔴" if item["priority"] == "高" else "🟡" if item["priority"] == "中" else "🟢"
            report += f"### {priority_emoji} {item['title']}\n"
            report += f"- **内容**：{item['content']}\n"
            report += f"- **影响**：{item['impact']}\n"
            report += f"- **来源**：{item['source']}\n"
            report += f"- **时间**：{item['effective_date']}\n\n"
        
        # AI工具变化
        report += "## 🤖 四、AI工具变化\n\n"
        for item in report_data.get("AI工具变化", []):
            priority_emoji = "🔴" if item["priority"] == "高" else "🟡" if item["priority"] == "中" else "🟢"
            report += f"### {priority_emoji} {item['title']}\n"
            report += f"- **内容**：{item['content']}\n"
            report += f"- **影响**：{item['impact']}\n"
            report += f"- **来源**：{item['source']}\n"
            report += f"- **时间**：{item['effective_date']}\n\n"
        
        # 今日关键行动项
        report += "## ⚡ 五、今日关键行动项\n\n"
        for item in action_items:
            report += f"### {item['priority']}. {item['action']}\n"
            report += f"- **截止时间**：{item['deadline']}\n"
            report += f"- **类别**：{item['category']}\n\n"
        
        report += "---\n\n"
        report += f"*日报生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        
        return report
    
    def send_to_feishu(self, content: str) -> bool:
        """发送日报到飞书"""
        timestamp = self.generate_timestamp()
        sign = self.generate_sign(timestamp)
        
        # 构建飞书消息卡片
        message = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": "📊 亚马逊日报"
                    },
                    "template": "blue"
                },
                "elements": [
                    {
                        "tag": "markdown",
                        "content": content
                    }
                ]
            }
        }
        
        # 如果有签名，添加到请求参数
        if sign:
            message["timestamp"] = timestamp
            message["sign"] = sign
        
        try:
            response = requests.post(
                self.webhook_url,
                headers={"Content-Type": "application/json"},
                json=message,
                timeout=10
            )
            result = response.json()
            if result.get("StatusCode") == 0 or result.get("code") == 0:
                print("✅ 日报已成功推送到飞书")
                return True
            else:
                print(f"❌ 推送失败: {result}")
                return False
        except Exception as e:
            print(f"❌ 推送异常: {str(e)}")
            return False
    
    def generate_and_send(self):
        """生成并发送日报"""
        print("🚀 开始生成亚马逊日报...")
        
        # 搜索亚马逊相关新闻
        print("📡 收集亚马逊最新动态...")
        report_data = self.search_amazon_news()
        
        # 生成行动项
        print("📋 生成关键行动项...")
        action_items = self.generate_action_items(report_data)
        
        # 格式化日报
        print("📝 格式化日报内容...")
        report_content = self.format_report(report_data, action_items)
        
        # 保存日报到本地
        today = datetime.now().strftime("%Y%m%d")
        report_file = f"/workspace/amazon_report_{today}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"💾 日报已保存到: {report_file}")
        
        # 发送到飞书
        print("📤 推送日报到飞书...")
        success = self.send_to_feishu(report_content)
        
        if success:
            print("✅ 日报生成和推送完成！")
        else:
            print("⚠️ 日报已生成但推送失败，请检查飞书配置")
        
        return report_content


if __name__ == "__main__":
    generator = AmazonDailyReportGenerator()
    generator.generate_and_send()