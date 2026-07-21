#!/bin/bash

set -e

echo "========================================"
echo "    亚马逊运营日报生成器 - 启动脚本"
echo "========================================"

WORKSPACE="/workspace"
PYTHON_SCRIPT="$WORKSPACE/amazon_report_generator.py"
CONFIG_FILE="$WORKSPACE/report_config.json"

cd "$WORKSPACE"

echo ""
echo "🔍 检查 Python 环境..."
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
    echo "✅ Python3 已安装"
else
    echo "❌ Python3 未安装，正在安装..."
    if command -v apt-get &>/dev/null; then
        sudo apt-get update && sudo apt-get install -y python3 python3-pip
    elif command -v yum &>/dev/null; then
        sudo yum install -y python3 python3-pip
    else
        echo "❌ 无法安装 Python3，请手动安装"
        exit 1
    fi
    PYTHON_CMD="python3"
fi

echo ""
echo "🔍 检查 requests 库..."
if $PYTHON_CMD -c "import requests" &>/dev/null; then
    echo "✅ requests 库已安装"
else
    echo "📦 正在安装 requests 库..."
    $PYTHON_CMD -m pip install requests
    echo "✅ requests 库安装完成"
fi

echo ""
echo "🔍 检查配置文件..."
if [ -f "$CONFIG_FILE" ]; then
    echo "✅ 配置文件存在"
else
    echo "❌ 配置文件不存在: $CONFIG_FILE"
    echo "请先创建配置文件"
    exit 1
fi

echo ""
echo "🔍 检查脚本文件..."
if [ -f "$PYTHON_SCRIPT" ]; then
    echo "✅ 脚本文件存在"
else
    echo "❌ 脚本文件不存在: $PYTHON_SCRIPT"
    echo "请先创建脚本文件"
    exit 1
fi

echo ""
echo "🚀 运行日报生成器..."
$PYTHON_CMD "$PYTHON_SCRIPT"

echo ""
echo "========================================"
echo "    日报生成任务完成"
echo "========================================"