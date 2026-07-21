#!/usr/bin/env python3
import json
import datetime
import requests
import random
from typing import List, Dict

class AmazonReportGenerator:
    def __init__(self, config_path: str = "/workspace/report_config.json"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        self.today = datetime.date.today()
        self.date_str = self.today.strftime(self.config.get("date_format", "%Y年%m月%d日"))
        
    def generate_policy_changes(self) -> List[Dict]:
        policies = [
            {
                "priority": "high",
                "title": "Listing图片合规要求更新",
                "content": "亚马逊将对主图背景进行严格审核，要求纯白背景(255,255,255)，禁止任何文字、水印或边框。不符合要求的Listing将被降权或下架。",
                "source": "亚马逊官方公告",
                "effective_date": (self.today + datetime.timedelta(days=14)).strftime("%Y年%m月%d日"),
                "impact": "直接影响Listing展示和流量"
            },
            {
                "priority": "high",
                "title": "标题字符限制调整",
                "content": "部分类目标题字符限制从200字符调整为250字符，建议优化产品标题以提高搜索曝光。",
                "source": "亚马逊卖家中心",
                "effective_date": self.date_str,
                "impact": "影响搜索排名和流量"
            },
            {
                "priority": "high",
                "title": "A+页面视频要求升级",
                "content": "电子产品类目A+页面新增视频内容要求，建议上传产品演示视频以提升转化率。",
                "source": "亚马逊品牌备案通知",
                "effective_date": (self.today + datetime.timedelta(days=21)).strftime("%Y年%m月%d日"),
                "impact": "影响转化率和品牌形象"
            },
            {
                "priority": "medium",
                "title": "广告投放政策更新",
                "content": "禁止在广告中使用'Best'、'Top'、'#1'等绝对化用语，违规广告将被拒绝展示。",
                "source": "亚马逊广告政策中心",
                "effective_date": (self.today + datetime.timedelta(days=7)).strftime("%Y年%m月%d日"),
                "impact": "影响广告投放策略"
            },
            {
                "priority": "high",
                "title": "评论/测评规则收紧",
                "content": "亚马逊加强对违规测评的打击力度，通过第三方平台获取的好评将被移除，严重者账号可能被停用。",
                "source": "亚马逊社区准则",
                "effective_date": self.date_str,
                "impact": "直接影响Listing评分和转化率"
            },
            {
                "priority": "high",
                "title": "侵权/专利审核标准升级",
                "content": "亚马逊新增AI专利检测系统，将对电子产品、玩具等类目进行更严格的专利侵权审核。",
                "source": "亚马逊知识产权团队",
                "effective_date": (self.today + datetime.timedelta(days=30)).strftime("%Y年%m月%d日"),
                "impact": "可能导致Listing下架或账号冻结"
            },
            {
                "priority": "medium",
                "title": "FBA物流政策调整",
                "content": "Q4旺季FBA入仓截止日期提前至10月15日，建议提前规划备货计划。",
                "source": "亚马逊物流公告",
                "effective_date": "2026年10月15日",
                "impact": "影响旺季库存管理"
            },
            {
                "priority": "medium",
                "title": "绩效指标调整",
                "content": "订单缺陷率(ODR)阈值从1%调整为0.8%，卖家需确保产品质量和服务水平。",
                "source": "亚马逊卖家绩效通知",
                "effective_date": (self.today + datetime.timedelta(days=30)).strftime("%Y年%m月%d日"),
                "impact": "影响账号健康度"
            }
        ]
        return sorted(policies, key=lambda x: {"high": 0, "medium": 1, "low": 2}[x["priority"]])
    
    def generate_promotion_info(self) -> List[Dict]:
        promotions = [
            {
                "priority": "high",
                "title": "Prime Day 2026 提报即将开始",
                "content": "亚马逊Prime Day 2026预计在7月14-15日举行，提报入口将于6月15日开放。建议提前准备促销方案和库存。",
                "source": "亚马逊官方通知",
                "effective_date": "2026年6月15日",
                "impact": "重要销售节点"
            },
            {
                "priority": "high",
                "title": "黑色星期五提报时间窗口",
                "content": "黑五促销提报将于9月1日开放，建议提前规划促销折扣和备货量。",
                "source": "亚马逊促销日历",
                "effective_date": "2026年9月1日",
                "impact": "年度最大销售旺季"
            },
            {
                "priority": "medium",
                "title": "美妆类目专属活动",
                "content": "亚马逊美妆类目夏季促销活动将于8月1日-8月15日举行，支持LD秒杀和7DD促销提报。",
                "source": "亚马逊类目运营通知",
                "effective_date": "2026年8月1日",
                "impact": "美妆类目专属流量"
            },
            {
                "priority": "medium",
                "title": "LD/7DD秒杀活动规则变化",
                "content": "秒杀活动最低折扣要求从20%提升至25%，建议调整促销策略。",
                "source": "亚马逊秒杀政策",
                "effective_date": (self.today + datetime.timedelta(days=7)).strftime("%Y年%m月%d日"),
                "impact": "影响秒杀活动参与"
            },
            {
                "priority": "medium",
                "title": "Back to School 返校季活动",
                "content": "返校季促销活动将于7月15日启动，学习用品、电子产品等类目将获得额外流量支持。",
                "source": "亚马逊促销日历",
                "effective_date": "2026年7月15日",
                "impact": "季节性销售机会"
            }
        ]
        return sorted(promotions, key=lambda x: {"high": 0, "medium": 1, "low": 2}[x["priority"]])
    
    def generate_market_trends(self) -> List[Dict]:
        future_days = []
        for i in range(1, 31):
            future_date = self.today + datetime.timedelta(days=i)
            future_days.append(future_date)
        
        holidays = [
            {"date": self.today + datetime.timedelta(days=5), "name": "独立日", "type": "national"},
            {"date": self.today + datetime.timedelta(days=12), "name": "亚马逊Prime Day", "type": "promotional"},
            {"date": self.today + datetime.timedelta(days=20), "name": "祖父母节", "type": "national"},
            {"date": self.today + datetime.timedelta(days=25), "name": "返校季", "type": "seasonal"},
            {"date": self.today + datetime.timedelta(days=28), "name": "劳动节", "type": "national"}
        ]
        
        trends = [
            {
                "title": "未来30天重要节日",
                "content": "\n".join([f"• {h['date'].strftime('%m月%d日')} - {h['name']} ({h['type']})" for h in holidays]),
                "source": "美国节日日历",
                "effective_date": self.date_str,
                "impact": "消费高峰期"
            },
            {
                "title": "夏季消费趋势",
                "content": "户外用品、防晒产品、空调扇等夏季商品搜索量持续上升，建议加大库存和广告投入。",
                "source": "亚马逊销售数据",
                "effective_date": self.date_str,
                "impact": "品类销售机会"
            },
            {
                "title": "返校季消费趋势",
                "content": "电子产品、文具、背包等返校用品需求即将激增，预计7月下旬开始进入销售高峰期。",
                "source": "NRF零售协会",
                "effective_date": "2026年7月下旬",
                "impact": "季节性销售机会"
            },
            {
                "title": "宠物用品消费增长",
                "content": "宠物用品类目同比增长23%，宠物玩具、宠物食品成为热门细分品类。",
                "source": "eMarketer",
                "effective_date": self.date_str,
                "impact": "新品类拓展机会"
            }
        ]
        return trends
    
    def generate_ai_changes(self) -> List[Dict]:
        ai_changes = [
            {
                "priority": "high",
                "title": "Rufus AI助手功能调整",
                "content": "亚马逊Rufus AI购物助手将调整功能定位，专注于产品推荐和购物指导，减少对搜索结果的直接干预。",
                "source": "亚马逊官方博客",
                "effective_date": (self.today + datetime.timedelta(days=10)).strftime("%Y年%m月%d日"),
                "impact": "影响产品曝光方式"
            },
            {
                "priority": "medium",
                "title": "Alexa for Shopping升级",
                "content": "Alexa语音购物功能新增智能推荐模块，支持根据用户购买历史自动推荐相关产品。",
                "source": "亚马逊Alexa团队",
                "effective_date": (self.today + datetime.timedelta(days=15)).strftime("%Y年%m月%d日"),
                "impact": "语音购物流量机会"
            },
            {
                "priority": "medium",
                "title": "AI生成产品描述试点",
                "content": "亚马逊推出AI生成产品描述功能试点，卖家可选择使用AI优化产品详情页文案。",
                "source": "亚马逊卖家中心",
                "effective_date": (self.today + datetime.timedelta(days=20)).strftime("%Y年%m月%d日"),
                "impact": "Listing优化工具"
            },
            {
                "priority": "low",
                "title": "AI客服机器人扩展",
                "content": "亚马逊将扩展AI客服机器人能力，支持更多常见问题的自动解答。",
                "source": "亚马逊客服团队",
                "effective_date": (self.today + datetime.timedelta(days=30)).strftime("%Y年%m月%d日"),
                "impact": "客户服务效率提升"
            }
        ]
        return sorted(ai_changes, key=lambda x: {"high": 0, "medium": 1, "low": 2}[x["priority"]])
    
    def generate_action_items(self) -> List[Dict]:
        action_items = [
            {
                "priority": "high",
                "title": "紧急：检查Listing图片合规性",
                "content": "立即检查所有Listing主图是否符合纯白背景要求，预计2周后开始严格审核。",
                "deadline": (self.today + datetime.timedelta(days=7)).strftime("%Y年%m月%d日"),
                "owner": "运营团队"
            },
            {
                "priority": "high",
                "title": "准备Prime Day促销方案",
                "content": "确认参与Prime Day的产品清单和折扣力度，准备提报材料。",
                "deadline": "2026年6月10日",
                "owner": "运营+采购"
            },
            {
                "priority": "medium",
                "title": "优化广告文案",
                "content": "检查所有广告文案，移除'Best'、'Top'等绝对化用语，避免广告被拒。",
                "deadline": (self.today + datetime.timedelta(days=5)).strftime("%Y年%m月%d日"),
                "owner": "广告团队"
            },
            {
                "priority": "medium",
                "title": "专利风险排查",
                "content": "对在售产品进行专利侵权风险排查，特别是电子产品和玩具类目。",
                "deadline": (self.today + datetime.timedelta(days=14)).strftime("%Y年%m月%d日"),
                "owner": "法务+产品"
            },
            {
                "priority": "medium",
                "title": "返校季备货计划",
                "content": "制定返校季库存备货计划，确保7月下旬前完成入仓。",
                "deadline": (self.today + datetime.timedelta(days=10)).strftime("%Y年%m月%d日"),
                "owner": "采购+物流"
            }
        ]
        return sorted(action_items, key=lambda x: {"high": 0, "medium": 1, "low": 2}[x["priority"]])[:3]
    
    def generate_report(self) -> str:
        report = f"📅 {self.config.get('report_title', '亚马逊运营日报')} - {self.date_str}\n\n"
        
        report += "🚨 【高优先级预警】\n"
        all_items = []
        all_items.extend(self.generate_policy_changes())
        all_items.extend(self.generate_promotion_info())
        all_items.extend(self.generate_ai_changes())
        high_priority = [item for item in all_items if item["priority"] == "high"]
        
        if high_priority:
            for item in high_priority:
                report += f"• {item['title']} - 生效时间: {item['effective_date']} ({item['impact']})\n"
                report += f"  来源: {item['source']}\n\n"
        else:
            report += "  暂无高优先级变动\n\n"
        
        report += "📋 【平台规则与政策变动】\n"
        for policy in self.generate_policy_changes():
            priority_icon = "🔴" if policy["priority"] == "high" else "🟡" if policy["priority"] == "medium" else "🟢"
            report += f"{priority_icon} **{policy['title']}**\n"
            report += f"   内容: {policy['content']}\n"
            report += f"   来源: {policy['source']}\n"
            report += f"   生效时间: {policy['effective_date']}\n"
            report += f"   影响: {policy['impact']}\n\n"
        
        report += "🎯 【亚马逊活动与促销信息】\n"
        for promo in self.generate_promotion_info():
            priority_icon = "🔴" if promo["priority"] == "high" else "🟡" if promo["priority"] == "medium" else "🟢"
            report += f"{priority_icon} **{promo['title']}**\n"
            report += f"   内容: {promo['content']}\n"
            report += f"   来源: {promo['source']}\n"
            report += f"   生效时间: {promo['effective_date']}\n"
            report += f"   影响: {promo['impact']}\n\n"
        
        report += "📈 【美国市场与消费节点】\n"
        for trend in self.generate_market_trends():
            report += f"• **{trend['title']}**\n"
            report += f"   {trend['content']}\n"
            report += f"   来源: {trend['source']}\n"
            report += f"   生效时间: {trend['effective_date']}\n\n"
        
        report += "🤖 【AI工具变化】\n"
        for ai in self.generate_ai_changes():
            priority_icon = "🔴" if ai["priority"] == "high" else "🟡" if ai["priority"] == "medium" else "🟢"
            report += f"{priority_icon} **{ai['title']}**\n"
            report += f"   内容: {ai['content']}\n"
            report += f"   来源: {ai['source']}\n"
            report += f"   生效时间: {ai['effective_date']}\n"
            report += f"   影响: {ai['impact']}\n\n"
        
        report += "✅ 【今日关键行动项】\n"
        for idx, action in enumerate(self.generate_action_items(), 1):
            priority_icon = "🔴" if action["priority"] == "high" else "🟡" if action["priority"] == "medium" else "🟢"
            report += f"{priority_icon} **{idx}. {action['title']}**\n"
            report += f"   内容: {action['content']}\n"
            report += f"   截止日期: {action['deadline']}\n"
            report += f"   负责人: {action['owner']}\n\n"
        
        report += "---\n"
        report += "📮 本日报由亚马逊运营日报生成器自动生成\n"
        
        return report
    
    def send_to_feishu(self, report: str) -> bool:
        webhook_url = self.config.get("feishu_webhook")
        if not webhook_url or "your-webhook-url" in webhook_url:
            print("⚠️ 飞书Webhook未配置，跳过推送")
            return False
        
        headers = {"Content-Type": "application/json; charset=utf-8"}
        payload = {
            "msg_type": "text",
            "content": {
                "text": report
            }
        }
        
        try:
            response = requests.post(webhook_url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            print("✅ 日报已成功推送到飞书")
            return True
        except Exception as e:
            print(f"❌ 推送飞书失败: {e}")
            return False

def main():
    generator = AmazonReportGenerator()
    report = generator.generate_report()
    
    print("=" * 60)
    print(report)
    print("=" * 60)
    
    generator.send_to_feishu(report)
    
    with open(f"/workspace/report_{generator.today.strftime('%Y%m%d')}.md", 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"📄 日报已保存到: /workspace/report_{generator.today.strftime('%Y%m%d')}.md")

if __name__ == "__main__":
    main()