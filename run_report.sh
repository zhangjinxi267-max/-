#!/bin/bash
set -e

WORKDIR="/workspace"
REPORT_SCRIPT="$WORKDIR/amazon_daily_report.py"
CONFIG_FILE="$WORKDIR/report_config.json"

echo "========================================="
echo "  亚马逊日报生成器启动脚本"
echo "========================================="

if [ ! -f "$REPORT_SCRIPT" ]; then
    echo "✗ 错误: 日报脚本不存在 - $REPORT_SCRIPT"
    exit 1
fi

if [ ! -f "$CONFIG_FILE" ]; then
    echo "✗ 错误: 配置文件不存在 - $CONFIG_FILE"
    exit 1
fi

echo ""
echo "🔄 检查Python环境..."
if command -v python3 &> /dev/null; then
    echo "✓ Python3 已安装"
else
    echo "⚠️ 正在安装Python3..."
    if command -v apt-get &> /dev/null; then
        apt-get update && apt-get install -y python3 python3-pip
    elif command -v yum &> /dev/null; then
        yum install -y python3 python3-pip
    else
        echo "✗ 无法安装Python3，请手动安装"
        exit 1
    fi
    echo "✓ Python3 安装完成"
fi

echo ""
echo "🔄 检查pip依赖..."
if python3 -c "import requests" &> /dev/null; then
    echo "✓ requests 已安装"
else
    echo "⚠️ 正在安装requests..."
    pip3 install requests
    echo "✓ requests 安装完成"
fi

echo ""
echo "🔄 运行日报生成器..."
cd "$WORKDIR"
python3 "$REPORT_SCRIPT"

echo ""
echo "========================================="
echo "  执行完成"
echo "========================================="