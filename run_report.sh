#!/bin/bash
# 亚马逊日报生成器启动脚本
# 自动安装依赖并运行日报生成和推送

set -e

echo "🚀 启动亚马逊日报生成器..."

# 安装依赖
pip install requests -q

# 运行日报生成
cd /workspace
python3 amazon_daily_report.py --feishu

echo "✅ 日报推送完成！"
