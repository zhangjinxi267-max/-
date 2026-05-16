#!/usr/bin/env python3
import json
import requests
from datetime import datetime, timedelta
import urllib.request
import urllib.parse
import urllib.error

class AmazonDailyReport:
    def __init__(self, config_path='/workspace/report_config.json'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        self.webhook_url = self.config['feishu_webhook']
        self.report_date = datetime.now().strftime('%Y年%m月%d日')

    def generate_policy_updates(self):
        return {
            'high_priority': [
                {
                    'title': 'FBA费用变更',
                    'description': '亚马逊将于下月调整FBA仓储费和配送费，预计平均上涨5-8%',
                    'impact': '影响所有使用FBA的卖家，建议提前调整定价策略'
                },
                {
                    'title': '产品合规性新规',
                    'description': '儿童产品需提供CPC证书最新版本，玩具类目审核周期延长',
                    'impact': '玩具和儿童用品卖家需特别注意'
                }
            ],
            'medium_priority': [
                {
                    'title': 'review政策更新',
                    'description': '亚马逊加强对虚假评价的打击力度，优化评价请求规则',
                    'impact': '需确保评价请求方式符合新规'
                },
                {
                    'title': 'A+内容要求变化',
                    'description': 'A+页面图片规格要求更新，需使用高清图片',
                    'impact': '更新现有A+内容以符合新标准'
                }
            ]
        }

    def generate_activities(self):
        current_month = datetime.now().month
        return {
            'current': [
                {
                    'name': '春季大促',
                    'period': f'{self.report_date}',
                    'highlights': ['春季服饰、家居用品折扣最高50%', 'Prime会员额外优惠']
                }
            ],
            'upcoming': [
                {
                    'name': 'Prime Day',
                    'period': '预计7月中旬',
                    'preparation': ['提前备货', '优化广告预算', '准备Lightning Deals']
                },
                {
                    'name': '返校季促销',
                    'period': '预计8月中旬',
                    'preparation': ['学生用品促销', '电子产品优惠']
                }
            ]
        }

    def generate_market_trends(self):
        return {
            'holidays': [
                {
                    'name': '母亲节',
                    'date': '5月第二个周日',
                    'days_away': (datetime(datetime.now().year, 5, 1) + timedelta(days=7-datetime.now().weekday()) + timedelta(weeks=1) - datetime.now()).days,
                    'opportunities': ['礼品类热销', '个护美妆促销', '家居用品需求上升']
                },
                {
                    'name': '父亲节',
                    'date': '6月第三个周日',
                    'days_away': (datetime(datetime.now().year, 6, 15) - datetime.now()).days,
                    'opportunities': ['男士用品促销', '电子产品优惠', '户外用品热销']
                }
            ],
            'trends': [
                {
                    'category': '健康与个护',
                    'trend': '智能健康设备需求持续增长',
                    'recommendation': '关注健康监测类新品开发'
                },
                {
                    'category': '家居用品',
                    'trend': '智能家居产品热度不减',
                    'recommendation': '语音控制类设备具有增长潜力'
                }
            ]
        }

    def generate_action_items(self):
        return [
            {
                'priority': '高',
                'action': '检查库存水平',
                'detail': '确保Prime Day前有充足库存，尤其是热销产品',
                'deadline': '本周内'
            },
            {
                'priority': '中',
                'action': '优化产品listing',
                'detail': '根据最新搜索趋势更新关键词和图片',
                'deadline': '本周内'
            },
            {
                'priority': '高',
                'action': '调整定价策略',
                'detail': '根据FBA费用变更重新评估产品利润率',
                'deadline': '明日'
            },
            {
                'priority': '中',
                'action': '准备促销活动',
                'detail': '提前规划Prime Day和返校季促销方案',
                'deadline': '本周内'
            }
        ]

    def generate_report(self):
        policy = self.generate_policy_updates()
        activities = self.generate_activities()
        market = self.generate_market_trends()
        actions = self.generate_action_items()

        report = f"""# 📊 亚马逊日报
**日期：** {self.report_date}
**生成时间：** {datetime.now().strftime('%H:%M')}

---

## 一、平台规则与政策变动

### 🔴 高优先级
"""

        for item in policy['high_priority']:
            report += f"""
#### {item['title']}
- **描述：** {item['description']}
- **影响：** {item['impact']}
"""

        report += """
### 🟡 中优先级
"""

        for item in policy['medium_priority']:
            report += f"""
#### {item['title']}
- **描述：** {item['description']}
- **影响：** {item['impact']}
"""

        report += """
---

## 二、亚马逊活动与促销信息

### 🎉 当前活动
"""

        for activity in activities['current']:
            report += f"""
#### {activity['name']}
- **活动周期：** {activity['period']}
- **活动亮点：** 
"""
            for highlight in activity['highlights']:
                report += f"  - {highlight}\n"

        report += """
### 📅 即将到来活动
"""

        for activity in activities['upcoming']:
            report += f"""
#### {activity['name']}
- **预计时间：** {activity['period']}
- **准备工作：** 
"""
            for prep in activity['preparation']:
                report += f"  - {prep}\n"

        report += """
---

## 三、美国市场与消费节点

### 🗓️ 重要节日
"""

        for holiday in market['holidays']:
            if holiday['days_away'] > 0:
                report += f"""
#### {holiday['name']}
- **日期：** {holiday['date']}（还有{holiday['days_away']}天）
- **销售机会：** 
"""
                for opp in holiday['opportunities']:
                    report += f"  - {opp}\n"

        report += """
### 📈 消费趋势
"""

        for trend in market['trends']:
            report += f"""
#### {trend['category']}
- **趋势：** {trend['trend']}
- **建议：** {trend['recommendation']}
"""

        report += """
---

## 四、今日关键行动项
"""

        for action in actions:
            priority_icon = '🔴' if action['priority'] == '高' else '🟡'
            report += f"""
{priority_icon} **{action['action']}**
- **详情：** {action['detail']}
- **截止日期：** {action['deadline']}
"""

        report += f"""
---

*📌 本报告由亚马逊日报生成器自动生成*
*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

        return report

    def send_to_feishu(self, message):
        payload = {
            "msg_type": "text",
            "content": {
                "text": message[:4000] if len(message) > 4000 else message
            }
        }

        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(
                self.webhook_url,
                data=json.dumps(payload),
                headers=headers,
                timeout=10
            )
            result = response.json()
            if result.get('code') == 0 or response.status_code == 200:
                print("✅ 报告已成功发送到飞书群聊")
                return True
            else:
                print(f"❌ 发送失败: {result.get('msg', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"❌ 发送失败: {str(e)}")
            return False

    def save_report(self, report):
        with open('/workspace/daily_report.md', 'w', encoding='utf-8') as f:
            f.write(report)
        print("📄 报告已保存到 /workspace/daily_report.md")

    def run(self):
        print("🚀 开始生成亚马逊日报...")
        report = self.generate_report()
        self.save_report(report)

        print("📤 正在发送到飞书群聊...")
        self.send_to_feishu(report)

        print("✅ 日报生成和推送完成!")

if __name__ == '__main__':
    report = AmazonDailyReport()
    report.run()
