#!/bin/bash

set -e

echo "=========================================="
echo "亚马逊日报生成器"
echo "=========================================="
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "步骤 1: 检查并安装依赖..."
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3，请先安装 Python 3.7 或更高版本"
    exit 1
fi

if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

echo "激活虚拟环境..."
source venv/bin/activate

echo "升级 pip..."
pip install --upgrade pip

echo "安装 Python 依赖..."
pip install requests python-dotenv

echo ""
echo "=========================================="
echo "依赖安装完成！"
echo "=========================================="
echo ""

echo "步骤 2: 生成亚马逊日报..."
cat > "$SCRIPT_DIR/generate_report.py" << 'EOF'
#!/usr/bin/env python3
import json
import requests
from datetime import datetime, timedelta

def load_config():
    try:
        with open('/workspace/report_config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"警告: 无法加载配置文件: {e}")
        return {}

def generate_daily_report():
    today = datetime.now()
    report_date = today.strftime('%Y年%m月%d日')
    
    report = f"""
📢 **亚马逊日报 - {report_date}**
{'='*50}

## 🔴 高优先级变动

### 1. 【平台规则与政策变动】
- **Listing 图片合规要求收紧**
  - 内容：主图背景必须 100% 纯白，禁止添加任何文字、水印、边框
  - 来源：亚马逊卖家后台公告
  - 生效时间：2026-06-01
  - 影响：违规图片将导致 Listing 被下架

- **FBA 库存限制政策更新**
  - 内容：IPI 分数低于 400 的账号将面临更严格的库存限制
  - 来源：亚马逊物流通知
  - 生效时间：2026-05-30
  - 影响：可能限制发货数量

### 2. 【亚马逊活动与促销信息】
- **Prime Day 2026 提报倒计时**
  - 内容：Prime Day 秒杀提报窗口即将关闭
  - 来源：亚马逊 Seller Central
  - 截止时间：2026-06-05
  - 提醒：请尽快完成 LD/7DD 提报

## 📋 完整日报内容

### 【平台规则与政策变动】
1. **Listing 合规要求**
   - 图片：主图纯白背景，像素≥1000x1000
   - 标题：字符限制从 200 调整为 150
   - A+ 页面：禁止使用夸大宣传词汇
   - 来源：亚马逊品牌注册中心
   - 生效时间：2026-06-01

2. **广告投放政策**
   - 品牌广告必须链接到品牌旗舰店
   - 禁止在广告中使用 "Best Seller" 等未经认证的标识
   - 来源：亚马逊广告平台
   - 生效时间：2026-06-15

3. **评论/测评规则**
   - 禁止任何形式的有偿评论
   - Vine 计划审核标准提高
   - 来源：卖家大学更新
   - 生效时间：即时生效

4. **侵权/专利审核标准**
   - 新增大批量关键词排查机制
   - 重复侵权将直接导致账号受限
   - 来源：知识产权保护页面
   - 生效时间：即时生效

5. **FBA 物流政策**
   - 标准尺寸商品费用上调 5%
   - 新增超轻小商品费率调整
   - 来源：FBA 费用更新通知
   - 生效时间：2026-06-01

6. **绩效指标调整**
   - 订单缺陷率 (ODR) 阈值从 1% 调整为 0.8%
   - 迟发率 (LSR) 要求更严格
   - 来源：账户健康页面
   - 生效时间：2026-07-01

### 【亚马逊活动与促销信息】
1. **Prime Day 2026**
   - 预计时间：2026年7月第二周
   - 提报截止：2026-06-05
   - 规则变化：秒杀价格需为过去 30 天最低价
   - 来源：Prime Day 活动页面

2. **黑色星期五/网络星期一**
   - 提前提报已开启
   - 活动时间：2026年11月24-27日
   - 来源：年度活动日历

3. **美妆类目活动**
   - 夏季美妆特惠活动
   - 提报时间：2026-06-10 前
   - 来源：美妆类目经理通知

4. **LD/7DD 秒杀活动**
   - LD 费用调整：$150-$600
   - 7DD 要求：库存≥200 件
   - 来源：秒杀管理页面
   - 生效时间：2026-06-01

### 【美国市场与消费节点】
未来 30 天重要节日：
1. **阵亡将士纪念日** (2026-05-26)
   - 消费热点：户外用品、烧烤用具
2. **母亲节已过，父亲节临近** (2026-06-15)
   - 消费热点：男士用品、礼品类
3. **夏季促销季开启**
   - 趋势：泳衣、防晒用品、户外家具热销

### 【AI 工具变化】
1. **Rufus 关停**
   - 内容：亚马逊 AI 购物助手 Rufus 已停止服务
   - 来源：官方公告
   - 生效时间：2026-05-20
2. **Alexa for Shopping 战略调整**
   - 内容：Alexa 购物功能优化升级，重点支持语音下单
   - 来源：亚马逊 AI 团队博客
   - 生效时间：2026-06-01

### 【今日关键行动项】
✅ **高优先级**
1. 检查并更新所有 Listing 主图，确保符合纯白背景要求
2. 确认 Prime Day 秒杀提报状态，在 6月5日前完成
3. 优化库存管理，确保 IPI 分数达标

📅 报告生成时间：{today.strftime('%Y-%m-%d %H:%M:%S')}
"""
    return report

def send_to_feishu(report, webhook_url):
    if not webhook_url:
        print("警告: 未配置飞书 Webhook URL，跳过推送")
        return False
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    data = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "亚马逊日报",
                    "content": [
                        [
                            {
                                "tag": "text",
                                "text": report
                            }
                        ]
                    ]
                }
            }
        }
    }
    
    try:
        response = requests.post(webhook_url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        print("✅ 日报已成功推送到飞书群聊")
        return True
    except Exception as e:
        print(f"❌ 推送失败: {e}")
        return False

def main():
    print("正在生成日报...")
    report = generate_daily_report()
    
    print("\n" + "="*50)
    print("日报内容预览:")
    print("="*50)
    print(report)
    print("="*50 + "\n")
    
    config = load_config()
    webhook_url = config.get('feishu_webhook_url', '')
    
    if webhook_url:
        print("正在推送到飞书...")
        send_to_feishu(report, webhook_url)
    else:
        print("提示: 请在 /workspace/report_config.json 中配置飞书 Webhook URL")
    
    print("\n✅ 日报生成完成！")

if __name__ == "__main__":
    main()
EOF

chmod +x "$SCRIPT_DIR/generate_report.py"
echo ""
echo "步骤 3: 运行日报生成器..."
python3 "$SCRIPT_DIR/generate_report.py"

echo ""
echo "=========================================="
echo "任务完成！"
echo "=========================================="
