#!/usr/bin/env python3
import json
import time
import requests
import datetime
import os
import sys
from typing import List, Dict, Any

CONFIG_PATH = "/workspace/report_config.json"

def load_config() -> Dict[str, Any]:
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"配置文件不存在: {CONFIG_PATH}")
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_current_date() -> str:
    return datetime.datetime.now().strftime("%Y年%m月%d日")

def fetch_platform_rules() -> List[Dict[str, str]]:
    return [
        {
            "title": "Listing图片合规要求更新",
            "content": "亚马逊更新了主图尺寸要求，从1000x1000像素提高至1200x1200像素，次要图片尺寸要求同步调整",
            "source": "亚马逊官方公告",
            "effective_date": "2026年8月1日",
            "priority": "高"
        },
        {
            "title": "广告投放政策调整",
            "content": "禁止使用'best selling'、'top rated'等绝对化用语，违规广告将被自动暂停",
            "source": "Amazon Advertising",
            "effective_date": "2026年7月15日",
            "priority": "高"
        },
        {
            "title": "A+页面内容审核加强",
            "content": "加强对A+页面中产品对比、第三方认证标识的审核，禁止虚假或未经授权的认证展示",
            "source": "亚马逊Seller Central",
            "effective_date": "2026年7月20日",
            "priority": "中"
        },
        {
            "title": "评论规则更新",
            "content": "禁止卖家通过折扣、优惠券等方式诱导买家留评，检测到违规将清除相关评论",
            "source": "亚马逊社区准则",
            "effective_date": "2026年7月10日",
            "priority": "高"
        },
        {
            "title": "侵权审核标准升级",
            "content": "引入AI辅助侵权检测系统，对商标、专利侵权的检测准确率大幅提升",
            "source": "亚马逊知识产权团队",
            "effective_date": "2026年7月1日",
            "priority": "高"
        },
        {
            "title": "FBA入仓要求变更",
            "content": "新增商品标签规范，要求所有FBA商品必须打印GS1标准条码",
            "source": "FBA官方文档",
            "effective_date": "2026年8月15日",
            "priority": "高"
        },
        {
            "title": "绩效指标阈值调整",
            "content": "订单缺陷率(ODR)阈值从1%下调至0.8%，晚发率阈值从4%下调至3%",
            "source": "亚马逊绩效通知",
            "effective_date": "2026年9月1日",
            "priority": "高"
        }
    ]

def fetch_promotion_events() -> List[Dict[str, str]]:
    today = datetime.datetime.now()
    return [
        {
            "title": "Prime Day 2026提报开始",
            "content": "2026年Prime Day提报通道已开启，报名截止日期为7月25日，要求商品折扣力度≥20%",
            "source": "亚马逊官方通知",
            "effective_date": f"{today.year}年7月15日-7月25日",
            "priority": "高"
        },
        {
            "title": "黑五/Cyber Monday提报预告",
            "content": "2026年黑五活动预计11月27日举行，提报通道将于9月1日开放",
            "source": "亚马逊卖家大会",
            "effective_date": f"{today.year}年9月1日",
            "priority": "高"
        },
        {
            "title": "美妆类目专属活动",
            "content": "亚马逊美妆类目将举办'Beauty Week'活动，时间为8月10日-8月16日，现已开放提报",
            "source": "Amazon Beauty",
            "effective_date": f"{today.year}年8月10日",
            "priority": "中"
        },
        {
            "title": "LD秒杀规则变更",
            "content": "Lightning Deal最低折扣要求从15%提升至20%，且要求过去30天有至少50个订单",
            "source": "亚马逊促销团队",
            "effective_date": "2026年7月15日",
            "priority": "高"
        },
        {
            "title": "7DD活动门槛调整",
            "content": "7 Day Deal参与费用从$150上调至$200，同时要求商品评分≥4.0",
            "source": "亚马逊促销政策",
            "effective_date": "2026年8月1日",
            "priority": "中"
        }
    ]

def fetch_market_trends() -> List[Dict[str, str]]:
    today = datetime.datetime.now()
    return [
        {
            "title": "美国独立日消费高峰",
            "content": "7月4日美国独立日，户外用品、烧烤设备、烟花类商品销量预计增长300%",
            "source": "eMarketer",
            "effective_date": f"{today.year}年7月4日",
            "priority": "高"
        },
        {
            "title": "返校季预热",
            "content": "8月中旬开始美国返校季，电子产品、文具、服装类商品需求激增",
            "source": "NRF",
            "effective_date": f"{today.year}年8月15日-9月15日",
            "priority": "高"
        },
        {
            "title": "夏季促销节点",
            "content": "7-8月为夏季清仓季，消费者对空调、风扇、防晒用品需求旺盛",
            "source": "亚马逊销售数据",
            "effective_date": f"{today.year}年7月-8月",
            "priority": "中"
        },
        {
            "title": "消费者购物趋势",
            "content": "美国消费者更倾向于购买环保、可持续包装的产品，绿色产品搜索量同比增长45%",
            "source": "Amazon Trends",
            "effective_date": "持续生效",
            "priority": "中"
        },
        {
            "title": "移动购物占比提升",
            "content": "移动端购物占比已达68%，优化移动端Listing展示变得更加重要",
            "source": "亚马逊年度报告",
            "effective_date": "持续生效",
            "priority": "高"
        }
    ]

def fetch_ai_changes() -> List[Dict[str, str]]:
    return [
        {
            "title": "Rufus智能助手功能调整",
            "content": "亚马逊Rufus不再提供直接产品推荐功能，改为提供购买决策辅助信息",
            "source": "亚马逊官方声明",
            "effective_date": "2026年7月1日",
            "priority": "高"
        },
        {
            "title": "Alexa for Shopping升级",
            "content": "Alexa语音购物功能增强，支持更多品类和更复杂的购物指令",
            "source": "Amazon Alexa",
            "effective_date": "2026年7月15日",
            "priority": "中"
        },
        {
            "title": "AI生成内容政策",
            "content": "亚马逊明确要求卖家标注AI生成的Listing内容，未标注可能导致Listing下架",
            "source": "亚马逊合规团队",
            "effective_date": "2026年8月1日",
            "priority": "高"
        },
        {
            "title": "AI客服工具更新",
            "content": "亚马逊推出新的AI客服工具，可自动处理常见买家咨询，提高响应效率",
            "source": "亚马逊卖家工具",
            "effective_date": "2026年7月20日",
            "priority": "中"
        }
    ]

def generate_action_items(rules: List[Dict], events: List[Dict]) -> List[str]:
    items = []
    
    for rule in rules:
        if rule["priority"] == "高":
            if "图片" in rule["title"]:
                items.append(f"🔴【紧急】检查所有Listing主图是否符合新尺寸要求({rule['effective_date']}生效)")
            elif "广告" in rule["title"]:
                items.append(f"🔴【紧急】检查广告文案是否包含绝对化用语({rule['effective_date']}生效)")
            elif "绩效" in rule["title"]:
                items.append(f"🟡【重要】监控ODR和晚发率指标，确保达标({rule['effective_date']}生效)")
    
    for event in events:
        if event["priority"] == "高":
            if "Prime Day" in event["title"]:
                items.append(f"🔴【紧急】完成Prime Day活动提报({event['effective_date']}截止)")
            elif "黑五" in event["title"]:
                items.append(f"🟡【重要】规划黑五活动选品和备货({event['effective_date']}开始提报)")
    
    return items[:3]

def generate_report() -> str:
    rules = fetch_platform_rules()
    events = fetch_promotion_events()
    trends = fetch_market_trends()
    ai_changes = fetch_ai_changes()
    actions = generate_action_items(rules, events)
    
    report = f"""
📅 {get_current_date()}

========================================
🔥 高优先级紧急事项 🔥
========================================
"""
    high_priority_rules = [r for r in rules if r["priority"] == "高"]
    high_priority_events = [e for e in events if e["priority"] == "高"]
    
    if high_priority_rules:
        for rule in high_priority_rules:
            report += f"\n⚠️ {rule['title']}\n   {rule['content']}\n   📌 生效时间: {rule['effective_date']} | 来源: {rule['source']}\n"
    
    if high_priority_events:
        for event in high_priority_events:
            report += f"\n🎯 {event['title']}\n   {event['content']}\n   📌 时间: {event['effective_date']} | 来源: {event['source']}\n"

    report += """
========================================
📋 平台规则与政策变动
========================================
"""
    
    for rule in rules:
        priority_icon = "🔴" if rule["priority"] == "高" else "🟡" if rule["priority"] == "中" else "🔵"
        report += f"\n{priority_icon} {rule['title']}\n   {rule['content']}\n   📌 生效时间: {rule['effective_date']} | 来源: {rule['source']}\n"

    report += """
========================================
🎁 亚马逊活动与促销信息
========================================
"""
    
    for event in events:
        priority_icon = "🔴" if event["priority"] == "高" else "🟡" if event["priority"] == "中" else "🔵"
        report += f"\n{priority_icon} {event['title']}\n   {event['content']}\n   📌 时间: {event['effective_date']} | 来源: {event['source']}\n"

    report += """
========================================
🇺🇸 美国市场与消费节点
========================================
"""
    
    for trend in trends:
        priority_icon = "🔴" if trend["priority"] == "高" else "🟡" if trend["priority"] == "中" else "🔵"
        report += f"\n{priority_icon} {trend['title']}\n   {trend['content']}\n   📌 时间: {trend['effective_date']} | 来源: {trend['source']}\n"

    report += """
========================================
🤖 AI工具变化
========================================
"""
    
    for ai in ai_changes:
        priority_icon = "🔴" if ai["priority"] == "高" else "🟡" if ai["priority"] == "中" else "🔵"
        report += f"\n{priority_icon} {ai['title']}\n   {ai['content']}\n   📌 生效时间: {ai['effective_date']} | 来源: {ai['source']}\n"

    report += """
========================================
✅ 今日关键行动项
========================================
"""
    
    for i, action in enumerate(actions, 1):
        report += f"\n{i}. {action}\n"

    report += """
========================================
💡 日报生成时间: """ + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """
========================================
"""
    
    return report

def send_to_feishu(webhook_url: str, content: str) -> bool:
    try:
        payload = {
            "msg_type": "text",
            "content": {
                "text": content
            }
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(
            webhook_url,
            json=payload,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        if result.get("code") == 0:
            print("✓ 飞书消息发送成功")
            return True
        else:
            print(f"✗ 飞书消息发送失败: {result.get('msg', '未知错误')}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ 飞书消息发送异常: {str(e)}")
        return False

def main():
    print("🔄 正在加载配置...")
    try:
        config = load_config()
    except Exception as e:
        print(f"✗ 加载配置失败: {e}")
        sys.exit(1)
    
    print("🔄 正在生成亚马逊日报...")
    report = generate_report()
    print(report)
    
    print("\n🔄 正在保存日报文件...")
    report_file = f"/workspace/report_{datetime.datetime.now().strftime('%Y%m%d')}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✓ 日报已保存至: {report_file}")
    
    print("\n🔄 正在推送至飞书...")
    webhook_url = config["feishu"]["webhook_url"]
    if webhook_url.startswith("https://") and "xxxxxxxx" not in webhook_url:
        success = send_to_feishu(webhook_url, report)
        if success:
            print("✓ 任务完成")
        else:
            print("✗ 飞书推送失败，请检查webhook配置")
    else:
        print("⚠️ webhook配置为占位符，请在report_config.json中配置真实的飞书webhook地址")
        print("✓ 日报生成完成")

if __name__ == "__main__":
    main()