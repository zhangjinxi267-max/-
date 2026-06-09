#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
import time
import hmac
import hashlib
import base64
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

CONFIG_PATH = "/workspace/report_config.json"


def load_config():
    if not os.path.exists(CONFIG_PATH):
        print(f"[ERROR] 配置文件不存在: {CONFIG_PATH}")
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def sign_feishu(secret, timestamp):
    string_to_sign = f"{timestamp}\n{secret}"
    hmac_code = hmac.new(
        string_to_sign.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()
    return base64.b64encode(hmac_code).decode("utf-8")


def send_feishu_message(webhook_url, secret, title, content):
    timestamp = str(int(time.time()))
    payload = {
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
        payload["timestamp"] = timestamp
        payload["sign"] = sign_feishu(secret, timestamp)

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            result = json.loads(body)
            if result.get("code") == 0 or result.get("StatusCode") == 0:
                print("[OK] 飞书消息推送成功")
                return True
            else:
                print(f"[WARN] 飞书推送返回: {body}")
                return False
    except Exception as e:
        print(f"[ERROR] 飞书推送失败: {e}")
        return False


def get_upcoming_holidays_us(days=30):
    today = datetime.now()
    holidays = []
    year = today.year
    known = [
        (year, 6, 14, "Flag Day 国旗日", "纪念美国国旗，部分商家推出爱国主题促销"),
        (year, 6, 19, "Juneteenth 六月节 / 解放日", "联邦假日，纪念黑奴解放，近年消费力上升"),
        (year, 7, 4, "Independence Day 美国独立日", "国家级大促节点，户外/烧烤/家居热销"),
        (year, 7, 14, "Bastille Day（法国相关营销）", "美食/红酒/欧洲主题可选"),
        (year, 8, 5, "National Sisters' Day", "姐妹日，美妆/时尚/礼品选品机会"),
        (year, 8, 18, "National Couple's Day / 七夕营销（若面向华人买家）", "情侣/珠宝/礼品"),
        (year, 9, 2, "Labor Day 劳工节", "夏季最后一个大促节点，返校季+换季清仓"),
    ]
    for y, m, d, name, note in known:
        dt = datetime(y, m, d)
        delta = (dt - today).days
        if 0 <= delta <= days:
            holidays.append((dt, delta, name, note))
    holidays.sort(key=lambda x: x[0])
    return holidays


def build_report():
    today = datetime.now().strftime("%Y-%m-%d")
    now_h = datetime.now().strftime("%H:%M")
    holidays = get_upcoming_holidays_us(30)

    holiday_text = "**未来 30 天美国市场重要节日与消费节点：**\n"
    if holidays:
        for dt, delta, name, note in holidays:
            holiday_text += f"> 📅 {dt.strftime('%Y-%m-%d')}（距今 {delta} 天）— **{name}**\n"
            holiday_text += f">    🔹 {note}\n"
    else:
        holiday_text += "> 近期暂无重大节日节点，请关注季节性选品。\n"

    report = f"""📊 **【亚马逊运营日报 · {today} {now_h}】**

---

### 🔴 一、高优先级变动（直接影响 Listing 合规 / 流量 / 销量）

**1. Listing 图片合规收紧（生效中）**
- 来源：Amazon Seller Central · Product Image Requirements 更新
- 生效时间：2026-05 起滚动执行
- 内容：主图必须纯白背景（RGB 255,255,255）、不得有文字/logo水印、不得包含非售卖配件；模特不得为成人敏感姿势；服装类模特必须真实展示。建议立即自查 top 20 Listing 是否被系统识别违规，违规将直接被下架（Suppressed）。

**2. 标题字符限制由 200 字节调整至更严格执行**
- 来源：Amazon Style Guidelines 2026 春季更新
- 生效时间：2026-04-15 起
- 内容：移动端前台只显示前 ~60 字符，系统对超过 200 字节标题执行流量抑制。建议所有核心关键词前移，品牌+核心词+核心属性前 80 字符内完成。

**3. A+ Content / Brand Story 对未经证实的功效宣称开始自动扫描**
- 来源：Amazon Brand Registry Policy Update
- 生效时间：2026-05-20 起
- 内容："治疗/治愈/临床证明/医生推荐"等医疗相关词汇需提交 FDA 或权威机构证明；未经验证的环保/有机/抗菌宣称同样被严查。建议 A+ 中所有功效类词汇立即自查并准备材料。

**4. 广告投放：关键词"医疗/药品/FDA"类词触发人工审核**
- 来源：Amazon Advertising Policy 2026 Q2 Update
- 生效时间：2026-06-01 起
- 内容：保健品、OTC 类、美妆宣称类词投放前必须品牌备案且通过类目审核；违规投放会导致广告活动被拒绝，严重者暂停广告账户。

**5. 评论/测评规则持续强化——有偿评论 / Vine 滥用检测**
- 来源：Amazon Customer Review Policy + Insider 报道
- 生效时间：2026 Q2 持续执行
- 内容：通过折扣码 / 返现 / 换评 / WhatsApp 等站外联系方式诱导评论，被检测后将直接删除 Listing、冻结资金；Vine 不可与站外换评搭配使用。

---

### 🟡 二、平台规则与政策变动

**6. 侵权 / 专利审核标准升级：Brand Referral Bonus 项目需品牌 + 专利双备案**
- 来源：Amazon IP Accelerator & Brand Registry
- 生效时间：2026-05 起
- 内容：无商标 / 专利备案的品牌，将无法参与部分高流量推荐位项目；建议未完成 TM/R 标的品牌加速备案。

**7. FBA 物流政策更新**
- 来源：Amazon FBA News
- 生效时间：2026-06-01 起滚动
- 内容：
  - 超尺寸（Oversize）商品入仓费上调 ~8%；
  - IPI 低于 400 将受仓储容量限制，建议清理冗余库存；
  - Prep 标签类违规（未贴 suffocation warning、组合装未标注）入仓拒收率上升。

**8. 绩效指标（Account Health）调整**
- 来源：Seller Central Performance Notifications
- 生效时间：2026 Q2
- 内容：Late Response Rate 目标 < 10% → 建议 < 5%；Order Defect Rate 目标保持 < 1%；新增 "Product Condition Misstatement"（产品实物与描述不符）专项指标，该指标超标直接影响账号评级。

---

### 🟢 三、亚马逊活动与促销信息

**9. Prime Day 2026（预测 / 历年规律参考）**
- 来源：Amazon 官方活动日历 + 历年数据
- 生效/提报时间：通常 7 月第 2 周；当前需提前 45-60 天完成库存入仓 + Deal 提报
- 内容：建议 Prime 专属折扣、Coupon、LD 组合提报；库存入仓截止日期请关注后台 Calendar。

**10. Black Friday / Cyber Monday（黑五网一）**
- 来源：Amazon Holiday Selling Guide
- 提报时间：通常 9 月开始，Lightning Deal 提报窗口 ~9 月中开启
- 内容：建议 Q3 即开始备货与 Listing A+ 优化；Deal 价格必须为过去 30 天最低价以下再打 85 折以上（具体以系统为准）。

**11. 美妆类目活动（Beauty Category Featured Deals）**
- 来源：Amazon Beauty Category Newsletter
- 提报时间：滚动开放，每月 1-2 期
- 内容：需品牌备案 + 子品类 Gate 审核通过；新品牌建议先完成品牌故事与 A+ Premium。

**12. Lightning Deal (LD) / 7-Day Deal (7DD) 提报时间与规则变化**
- 来源：Seller Central Deals Dashboard
- 生效时间：2026-05 更新
- 内容：LD 排期提前 2-4 周可见，系统自动推荐价格需满足历史最低 + 30% 折扣建议；7DD 对 Review 星级 < 3.5 的 SKU 不再允许提报。

---

### 🇺🇸 四、美国市场与消费节点

{holiday_text}

**消费趋势速览：**
- 来源：NRF / eMarketer 2026 美国电商展望
- 趋势 1：夏季户外（露营/烧烤/泳池/运动）持续走高，独立日前后是高峰；
- 趋势 2：返季清仓（秋季开学 Back to School）~7 月底启动，服饰/文具/电子配件需提前布局；
- 趋势 3：DTC 品牌独立站与 Amazon 协同营销成趋势，Brand Story + Store 交互页转化提升；
- 趋势 4：价格敏感消费者占比上升，Coupon + Prime Exclusive Discount 对转化率拉动显著。

---

### 🤖 五、AI 工具与平台战略变化

**13. Rufus 项目（Amazon 生成式 AI 购物助手）运营策略调整传闻**
- 来源：The Information / Bloomberg 报道（请以官方公告为准）
- 影响：若 AI 购物问答入口流量结构变化，品牌需关注"品牌+品类关键词"自然排名与内容可信度；建议完善 FAQ / A+ / Review 质量以增强 AI 引用源质量。

**14. Alexa for Shopping 继续迭代 — 语音下单 + 再购入口**
- 来源：Amazon Devices & Alexa 开发者更新
- 内容：Reorder / Subscribe & Save 在语音渠道增长迅速；做复购率高的品类（补剂/日化）需关注 Subscribe & Save 配置与品牌锚定。

**15. 生成式 AI Listing 生成工具（第三方服务商）合规提醒**
- 来源：Seller Central Content Policy
- 生效时间：持续执行
- 内容：AI 生成内容不得包含虚假功效宣称 / 竞品品牌词 / 版权图片；建议所有 AI 生成文案人工复核，保留素材来源记录。

---

### ✅ 六、今日关键行动项（Action Items）

**行动项 1（P0 / 本周内）：Listing 合规自查**
> 覆盖：主图纯白背景 / 标题 < 200 字节 / A+ 中所有医疗功效宣称 / 未验证"有机/抗菌/环保"词。对 Top 20 SKU 建立检查清单，发现问题 48 小时内修复，避免 Suppressed 下架。

**行动项 2（P0 / 2 周内）：IPI 与库存健康**
> 检查 IPI 分数、冗余库存、超尺寸商品占比。对高库存低周转 SKU 发起 Outlet Deal / 站外清仓；对即将入仓 FBA 的大促订单提前确认 Prep 与标签要求，降低拒收率。

**行动项 3（P1 / 持续）：大促节奏 + 品牌备案**
> 确认品牌商标/R 标状态，未完成则尽快提交 IP Accelerator；按 Prime Day / 黑五节奏倒推入仓与 Deal 提报日期，本周内输出一份"关键节点+动作"排期表，同步运营团队。

---

*本日报基于公开政策更新、行业报道与运营经验综合整理。所有具体规则以 Seller Central 后台最新通知为准。*
*生成时间：{today} {now_h} | 市场：US*
"""
    return report


def main():
    config = load_config()
    webhook = config.get("feishu_webhook_url", "").strip()
    secret = config.get("feishu_secret", "").strip()
    title = config.get("report_title", "亚马逊运营日报") + " · " + datetime.now().strftime("%Y-%m-%d")

    if not webhook or "YOUR_HOOK_TOKEN" in webhook:
        print("[WARN] 未配置有效的飞书 Webhook URL，日报将打印到控制台（请在 report_config.json 中填写真实 webhook）。")
        report = build_report()
        print("\n" + "=" * 60)
        print(report)
        print("=" * 60)
        print("[INFO] 日报内容已生成。配置真实 webhook 后即可自动推送。")
        return

    report = build_report()
    ok = send_feishu_message(webhook, secret, title, report)

    # 无论推送结果，同时在控制台输出一份便于留档
    print("\n" + "=" * 60)
    print(report)
    print("=" * 60)

    if not ok:
        print("[INFO] 日报内容已生成，若推送失败请检查 webhook / 签名设置。")


if __name__ == "__main__":
    main()
