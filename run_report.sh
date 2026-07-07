#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "  亚马逊日报生成器 - 启动中"
echo "=========================================="
echo ""

echo "[1/3] 检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
    echo "未找到 python3，请先安装 Python 3"
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1)
echo "  ✓ $PYTHON_VERSION"

echo ""
echo "[2/3] 检查依赖..."
python3 -c "
import json, hashlib, hmac, base64, urllib
print('  ✓ 所有核心依赖已就绪（使用 Python 标准库，无需额外安装）')
"

echo ""
echo "[3/3] 运行日报生成器..."
echo "------------------------------------------"
python3 "$SCRIPT_DIR/amazon_daily_report.py"
EXIT_CODE=$?
echo "------------------------------------------"

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ 日报生成完成！"
else
    echo ""
    echo "⚠️  日报生成完成（推送跳过，见上方说明）"
fi

exit $EXIT_CODE
