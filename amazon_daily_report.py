#!/usr/bin/env python3
import json
import os
import sys
import hashlib
import hmac
import base64
import time
from datetime import datetime, timedelta
from urllib import request, parse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "report_config.json")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def gen_sign(timestamp, secret):
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    hmac_code = hmac.new(
        string_to_sign.encode("utf-8"),
        digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(hmac_code).decode('utf-8')

def send_feishu_webhook(webhook_url, secret, title, content):
    timestamp = str(int(time.time()))
    body = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": title
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
    if secret:
        sign = gen_sign(timestamp, secret)
        body["timestamp"] = timestamp
        body["sign"] = sign

    data = json.dumps(body).encode("utf-8")
    req = request.Request(
        webhook_url,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    try:
        with request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result
    except Exception as e:
        return {"error": str(e)}

def build_report():
    today = datetime.now().strftime("%Y年%m月%d日")

    high_priority_items = [
        {
            "title": "评论操纵零容忍政策持续升级，账号级封禁风险加剧",
            "desc": "亚马逊2025-2026年持续强化评论操纵打击力度，采用AI算法识别评分激增、重复评论者、协同模式等异常行为，实行\"两次违规即出局\"政策，即使是合规卖家也可能在大范围检测中被审查。",
            "source": "eCommerce Evolution Podcast / Amazon Anti-Manipulation Policy",
            "effective_time": "持续生效中（2025年起强化执行）"
        },
        {
            "title": "FBA配送费2026年1月15日起调整，叠加4月17日3.5%燃料附加费",
            "desc": "2026年1月15日起标准尺寸商品配送费平均每件增加$0.08；4月17日起美国及加拿大FBA配送费加收3.5%燃料和物流相关附加费。低价商品（<$10）小号标准尺寸每件增加$0.12，高价商品（>$50）增加$0.31。",
            "source": "Amazon Seller Central - 2026年美国FBA配送费用变更",
            "effective_time": "2026年1月15日（费率调整）/ 2026年4月17日（附加费）"
        },
        {
            "title": "变体评论共享政策收紧，差异变体不再共享评论",
            "desc": "2026年2月12日至5月31日期间，亚马逊逐步停止差异显著的产品变体之间的评论共享，关闭变体滥用漏洞。卖家需确保变体系列内产品真正相似（尺寸/颜色/款式），否则评论将被拆分。",
            "source": "Amazon Seller Central / EpiphanyInfotech 分析",
            "effective_time": "2026年2月12日 - 5月31日（分阶段实施）"
        }
    ]

    platform_policies = [
        {
            "title": "Listing图片合规标准更新（2026年）",
            "desc": "主图要求：纯白背景（RGB 255,255,255）、产品占比85-100%、最长边至少1000像素（建议1600+）以启用缩放功能、禁止文字/图形/Logo/水印/促销信息、必须展示完整产品。主图质量直接影响转化率和搜索排名。",
            "source": "Amazon Seller Forums - Product Photography Standards 2026",
            "effective_time": "持续生效（2026年重申强化）"
        },
        {
            "title": "产品标题新规：200字符上限、禁止重复关键词",
            "desc": "大多数品类标题不得超过200字符（含空格）；禁止特殊字符 !, $, ?, _, {, }, ^, ¬, ¦（品牌名除外）；同一单词不得出现超过两次（介词、冠词、连词除外）。品牌所有者有14天处理建议，之后亚马逊将自动修改。",
            "source": "Amazon Seller Central - New product title requirements",
            "effective_time": "2025年1月21日起生效"
        },
        {
            "title": "多品类合规政策更新：便携式电源、供水商品、膳食补充剂",
            "desc": "亚马逊要求卖家必须与第三方检测认证(TIC)服务商合作，对收到通知的ASIN进行商品检测。便携式电源需符合BS/EN/IEC62368-1和BS/EN/IEC62133-2标准及UN38.3；供水商品需符合无铅要求（涉水表面铅含量加权平均≤0.25%）和ANSI认证。",
            "source": "亚马逊全球开店 - 多品类合规政策更新",
            "effective_time": "2026年1月起分批实施"
        },
        {
            "title": "广告审核政策：提前7天提交素材，预审核机制可用",
            "desc": "Sponsored Brands和Sponsored Display广告发布前须经审核。建议至少提前7天提交；支持批量预审核创意资产，审核通过后存入素材库供后续使用。广告内容要求：准确反映商品详情页、使用站点主要语言、无误导性声明、禁止竞品对比和制造紧迫感。",
            "source": "Amazon Ads - Sponsored Brands moderation guide",
            "effective_time": "持续生效"
        },
        {
            "title": "英国CMA与亚马逊达成虚假评论治理承诺",
            "desc": "亚马逊承诺建立更严格的虚假评论和目录滥用检测与移除流程；违规卖家可能被封禁，违规评论者账号将被禁言并删除所有历史评论。消费者和商家均可便捷举报。依据DMCC法案2024，CMA可直接处以罚款。",
            "source": "Lewis Silkin - Amazon gives undertakings to CMA",
            "effective_time": "2025年6月起执行"
        },
        {
            "title": "FBA低库存水平费用改按FNSKU收取，食品类豁免",
            "desc": "低库存水平费用将按FNSKU（而非父ASIN）收取，有助于确保畅销变体有充足库存。食品类商品现已获得豁免。周转慢的商品可免除低库存费，但配送承诺可能较慢或全国供货能力有限。",
            "source": "Amazon Seller Central - 2026年美国销售佣金和FBA费用变更一览",
            "effective_time": "2026年1月15日起生效"
        },
        {
            "title": "超大型处理费：最长边超96英寸加收附加费",
            "desc": "自2026年1月15日起，对最长边超过96英寸或长度加周长超过130英寸的加大型产品（重量不超过150磅）收取超大型附加费。",
            "source": "Amazon Seller Central - 2026 FBA fee changes",
            "effective_time": "2026年1月15日起生效"
        }
    ]

    promotions = [
        {
            "title": "Prime Day 2026已结束：6月23-26日，为期4天",
            "desc": "2026年Prime Day于6月23日至26日举行，Prime会员专享，覆盖35+品类数百万优惠。活动期间每日有新优惠，部分时段每5分钟更新一次。Alexa for Shopping提供优惠提醒和自动购买功能。",
            "source": "Amazon About - Prime Day 2026",
            "effective_time": "2026年6月23日 - 6月26日（已结束，复盘参考）"
        },
        {
            "title": "Prime Day秒杀提报已截止：6月9日关闭排期",
            "desc": "Prime-Exclusive Best Deal和Lightning Deal提报于3月24日开启，4月30日前提交可享每个Deal $50早鸟优惠。6月9日关闭排期。Prime专享折扣在活动结束前6小时均可提交。FBA入仓截止：5月27日（最少拆分）/6月5日（亚马逊优化拆分）。",
            "source": "Amazon Seller Central - Prime Day readiness playbook",
            "effective_time": "2026年6月9日（排期截止，已结束）"
        },
        {
            "title": "黑五网一2026预告：通常11月末开启，提前规划Q4库存",
            "desc": "参考2025年黑五周期：11月20日黑五周开始，持续至12月1日（含网一）。2026年感恩节为11月26日，预计黑五周将于11月中下旬启动。数百万优惠覆盖家居、电子、美妆、服饰等品类，最高可达50%折扣。",
            "source": "Amazon Press - Black Friday 2025 announcement（参考）",
            "effective_time": "2026年11月（预计，以官方公告为准）"
        },
        {
            "title": "美妆类目活动：夏季美妆节（已结束）/ 假日美妆季（Q4）",
            "desc": "2026年夏季美妆节于4月底至5月10日（母亲节）举行，为期两周，覆盖10,000+优惠，低至5折。48小时闪购轮换：彩妆、香水、健康保健、男士护理、护肤、护发、个护。Q4假日美妆季通常在10月底至11月初举行。",
            "source": "Amazon About - Summer Beauty Event 2026",
            "effective_time": "2026年4月27日 - 5月10日（已结束）/ Q4假日季（待官宣）"
        },
        {
            "title": "Lightning Deal / 7-Day Deal 常规规则要点",
            "desc": "LD：折扣≥15%，展示约4-6小时，仅FBA/Easy-Ship Prime商品 eligible，需提前3+周提报，同一ASIN不能同时参加多个Deal。7DD：折扣≥10%，展示7天（周一至周日）。黄金购物车所有者才有申报资格。主图必须合规。",
            "source": "Amazon Seller University - 促销工具及使用方法",
            "effective_time": "持续生效"
        },
        {
            "title": "春季大促参考：3月中下旬，欧洲站已公布2026春季档",
            "desc": "2026年欧洲站春季大促3月10-16日（10站同步），秒杀提报截止3月6日，Z划算截止3月9日，FBA入仓截止2月27日。美国站Big Spring Sale 2026于3月25-31日举行，覆盖35+品类，美妆最高30%折扣。",
            "source": "Amazon About - Big Spring Sale 2026 / 亚马逊全球开店",
            "effective_time": "2026年3月（已结束，供2027参考）"
        }
    ]

    us_market = [
        {
            "title": "独立日（7月4日）：夏季消费高峰节点",
            "desc": "美国独立日是夏季重要消费节点，户外用品、烧烤设备、节日装饰、爱国主题商品、泳装、防晒霜需求旺盛。7月4日前后周末通常有大型促销活动，零售商普遍推出家居、服饰、电子产品折扣。",
            "source": "Retail Holiday Calendar / 美国零售日历",
            "effective_time": "2026年7月4日（刚过，复盘Q3策略）"
        },
        {
            "title": "返校季（Back to School）：7月中 - 9月",
            "desc": "美国返校季是每年第三大购物季，2025年市场规模约370亿美元。主力品类：文具、笔记本电脑、平板、背包、学生服装、宿舍用品。Apple教育优惠、Amazon返校季专场是重要流量入口。7月中旬至8月为高峰期。",
            "source": "iSale / igni7e - 米国EC販促カレンダー",
            "effective_time": "2026年7月中旬 - 9月上旬（进行中）"
        },
        {
            "title": "劳动节（Labor Day）：9月第一个周一",
            "desc": "劳动节标志着夏季结束，是重要的清仓和促销节点，通常有大型周末促销。床垫、家具、家电折扣力度大，夏装季末清仓。2026年为9月7日，预计9月5-7日为促销高峰。",
            "source": "DontPayFull - 2026 Shopping Calendar",
            "effective_time": "2026年9月7日（即将到来）"
        },
        {
            "title": "8月消费节点：国际猫日/国际狗日/免税周末",
            "desc": "8月8日国际猫日、8月26日国际狗日：宠物食品、玩具、美容用品有主题促销。部分州8月有免税周末（如Iowa 8月7-8日服装鞋类$100以下免税），适合分州定向营销。",
            "source": "DontPayFull - 2026 Shopping Calendar / Shopify Retail Calendar",
            "effective_time": "2026年8月"
        },
        {
            "title": "消费趋势：AI购物助手影响购买决策，属性完整度决定曝光",
            "desc": "Alexa for Shopping（原Rufus）嵌入搜索栏，影响数百万购物者的购买路径。AI助手优先推荐属性完整、用例覆盖全面、语义化A+内容丰富的产品。AI购物旅程中完成购买的可能性比普通浏览高60%。",
            "source": "Teikametrics - Alexa for Shopping Catalog Impact",
            "effective_time": "2026年5月起持续深化"
        }
    ]

    ai_tools = [
        {
            "title": "Rufus正式升级为Alexa for Shopping，统一AI购物入口",
            "desc": "2026年5月13日，亚马逊将Rufus聊天机器人升级为Alexa for Shopping，整合Rufus商品知识与Alexa+个性化能力，嵌入亚马逊搜索栏、Shopping App和Echo Show设备。支持价格提醒、商品对比、定期购买设置、库存通知，甚至跨网站代买(Buy for Me)。",
            "source": "Amazon About - Alexa for Shopping / CNET Japan / 雪球",
            "effective_time": "2026年5月13日起全面上线"
        },
        {
            "title": "AI购物助手影响Listing排名逻辑：三大关键信号",
            "desc": "Alexa for Shopping通过三个信号决定产品是否被推荐：1）用例覆盖度——描述产品用途而非仅名称，优化可提升38%答案位可见度；2）属性深度——每一项结构化属性都是AI可回答的问题，平均品牌仅填了12项中的4项；3）语义化A+内容——纯图片模块AI无法读取，对比表/FAQ/属性标注直接供给模型。",
            "source": "Teikametrics - Alexa for Shopping Catalog Impact（2400+品牌审计数据）",
            "effective_time": "2026年5月起生效"
        },
        {
            "title": "亚马逊AI战略：Agentic AI + Bedrock多模型路由",
            "desc": "Alexa for Shopping基于Amazon Bedrock构建，使用Anthropic Claude Sonnet、Amazon Nova和自定义模型的实时路由架构，针对不同查询类型优化能力、延迟和答案质量。月度用户同比增长140%，互动量增长210%。2025年Rufus带动了约120亿美元增量年化销售额。",
            "source": "AWS Blog - How Rufus scales with Amazon Bedrock / Teikametrics",
            "effective_time": "持续迭代中"
        },
        {
            "title": "Help Me Decide等新AI购物功能上线",
            "desc": "亚马逊推出\"Help Me Decide\"功能，帮助消费者快速选择合适产品。Lens视觉搜索新增Lens Live滑动商品匹配功能。\"Hear the Highlights\"提供AI生成的音频对话，基于商品详情、评论和网络见解。",
            "source": "Amazon About - Help Me Decide / Amazon Shopping AI Features",
            "effective_time": "2025年底至2026年陆续上线"
        }
    ]

    action_items = [
        "立即审计所有变体Listing，确保变体间产品真正相似（仅尺寸/颜色/款式差异），在5月31日变体评论共享政策完全落地前清理不合规变体，避免评论被拆分导致权重下降。",
        "备战返校季（7月中-9月）：优化相关品类Listing的属性完整度（目标12/12项），补充语义化A+内容（对比表、FAQ模块），提升Alexa for Shopping推荐概率，抢占AI购物入口流量。",
        "复盘Q3物流成本：按新FBA费率（1月15日调整+4月17日3.5%附加费）重新核算各ASIN利润，对低价/大尺寸商品评估定价策略或SIPP认证机会，降低超大型处理费影响。"
    ]

    lines = []
    lines.append(f"**📅 生成时间：{today}**")
    lines.append("---")

    lines.append("## ⚠️ 高优先级变动（直接影响Listing合规/流量/销量）")
    for i, item in enumerate(high_priority_items, 1):
        lines.append(f"\n**{i}. {item['title']}**")
        lines.append(f"- {item['desc']}")
        lines.append(f"- 📌 来源：{item['source']}")
        lines.append(f"- ⏰ 生效时间：{item['effective_time']}")

    lines.append("\n---")
    lines.append("## 📋 一、平台规则与政策变动")
    for i, item in enumerate(platform_policies, 1):
        lines.append(f"\n**{i}. {item['title']}**")
        lines.append(f"- {item['desc']}")
        lines.append(f"- 📌 来源：{item['source']}")
        lines.append(f"- ⏰ 生效时间：{item['effective_time']}")

    lines.append("\n---")
    lines.append("## 🎁 二、亚马逊活动与促销信息")
    for i, item in enumerate(promotions, 1):
        lines.append(f"\n**{i}. {item['title']}**")
        lines.append(f"- {item['desc']}")
        lines.append(f"- 📌 来源：{item['source']}")
        lines.append(f"- ⏰ 生效时间：{item['effective_time']}")

    lines.append("\n---")
    lines.append("## 🇺🇸 三、美国市场与消费节点")
    for i, item in enumerate(us_market, 1):
        lines.append(f"\n**{i}. {item['title']}**")
        lines.append(f"- {item['desc']}")
        lines.append(f"- 📌 来源：{item['source']}")
        lines.append(f"- ⏰ 时间：{item['effective_time']}")

    lines.append("\n---")
    lines.append("## 🤖 四、AI工具变化")
    for i, item in enumerate(ai_tools, 1):
        lines.append(f"\n**{i}. {item['title']}**")
        lines.append(f"- {item['desc']}")
        lines.append(f"- 📌 来源：{item['source']}")
        lines.append(f"- ⏰ 时间：{item['effective_time']}")

    lines.append("\n---")
    lines.append("## ✅ 五、今日关键行动项")
    for i, item in enumerate(action_items, 1):
        lines.append(f"\n**{i}. {item}**")

    lines.append("\n---")
    lines.append(f"> 📊 本报告共覆盖 {len(high_priority_items) + len(platform_policies) + len(promotions) + len(us_market) + len(ai_tools)} 条信息，{len(action_items)} 条行动建议")

    return "\n".join(lines)

def main():
    config = load_config()
    webhook_url = config.get("feishu_webhook_url", "")
    secret = config.get("feishu_secret", "")
    title = config.get("report_title", "亚马逊卖家日报")

    today = datetime.now().strftime("%Y年%m月%d日")
    full_title = f"{title} - {today}"

    print(f"正在生成 {full_title} ...")
    content = build_report()
    print("报告生成完成。")

    if not webhook_url or "YOUR_WEBHOOK_TOKEN_HERE" in webhook_url:
        print("⚠️  警告：未配置有效的飞书Webhook URL，报告仅在本地输出。")
        print("=" * 60)
        print(content)
        print("=" * 60)
        print("\n请在 /workspace/report_config.json 中配置有效的 webhook_url 后重试。")
        return 1

    print(f"正在推送到飞书群聊 ...")
    result = send_feishu_webhook(webhook_url, secret, full_title, content)

    if result.get("code") == 0 or result.get("StatusCode") == 0:
        print("✅ 推送成功！")
        report_file = os.path.join(SCRIPT_DIR, f"daily_report_{datetime.now().strftime('%Y%m%d')}.md")
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(f"# {full_title}\n\n")
            f.write(content)
        print(f"📄 报告已保存至: {report_file}")
        return 0
    else:
        print(f"❌ 推送失败: {result}")
        print("报告内容预览：")
        print(content[:500] + "..." if len(content) > 500 else content)
        return 1

if __name__ == "__main__":
    sys.exit(main())
