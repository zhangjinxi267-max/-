#!/bin/bash

# 亚马逊日报生成器运行脚本
# 自动安装依赖并运行日报生成器

set -e

echo "=========================================="
echo "  亚马逊日报生成器"
echo "=========================================="
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，正在安装..."
    apt-get update && apt-get install -y python3 python3-pip
fi

echo "✅ Python3 已安装: $(python3 --version)"
echo ""

# 安装依赖
echo "📦 安装依赖包..."
pip3 install requests -q

echo "✅ 依赖安装完成"
echo ""

# 检查配置文件
if [ ! -f "/workspace/report_config.json" ]; then
    echo "❌ 配置文件不存在: /workspace/report_config.json"
    echo "请先创建配置文件"
    exit 1
fi

echo "✅ 配置文件已找到"
echo ""

# 运行日报生成器
echo "🚀 启动日报生成器..."
echo "=========================================="
echo ""

python3 /workspace/amazon_daily_report.py

echo ""
echo "=========================================="
echo "  日报生成完成"
echo "=========================================="