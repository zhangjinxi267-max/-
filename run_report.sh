#!/bin/bash

set -e

echo "=========================================="
echo "  亚马逊日报生成器"
echo "  开始执行日期: $(date '+%Y年%m月%d日 %H:%M:%S')"
echo "=========================================="
echo ""

cd /workspace

echo "📦 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，正在安装..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y python3 python3-pip
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3 python3-pip
    else
        echo "❌ 无法自动安装Python3，请手动安装"
        exit 1
    fi
fi

echo "✅ Python3 版本: $(python3 --version)"

echo ""
echo "📦 检查依赖..."
if ! python3 -c "import requests" &> /dev/null; then
    echo "📦 安装 requests 库..."
    pip3 install requests --quiet
    echo "✅ requests 安装完成"
else
    echo "✅ requests 库已安装"
fi

echo ""
echo "🔍 验证配置文件..."
if [ ! -f "/workspace/report_config.json" ]; then
    echo "❌ 配置文件不存在: /workspace/report_config.json"
    exit 1
fi

echo "✅ 配置文件验证通过"

echo ""
echo "🔍 验证日报生成器脚本..."
if [ ! -f "/workspace/amazon_report_generator.py" ]; then
    echo "❌ 日报生成器脚本不存在: /workspace/amazon_report_generator.py"
    exit 1
fi

echo "✅ 日报生成器脚本验证通过"

echo ""
echo "=========================================="
echo "  开始生成亚马逊日报"
echo "=========================================="
echo ""

python3 /workspace/amazon_report_generator.py

echo ""
echo "=========================================="
echo "  执行完成时间: $(date '+%Y年%m月%d日 %H:%M:%S')"
echo "=========================================="
