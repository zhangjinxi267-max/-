#!/usr/bin/env bash
# =============================================================================
# 亚马逊日报生成器 - run_report.sh
# 功能：自动安装依赖、运行日报生成器、通过飞书机器人推送日报
# 用法：bash /workspace/run_report.sh
# =============================================================================

set -euo pipefail

WORKSPACE="/workspace"
CONFIG_FILE="${WORKSPACE}/report_config.json"
REPORT_SCRIPT="${WORKSPACE}/amazon_daily_report.py"
LOG_FILE="${WORKSPACE}/report_run.log"

cd "${WORKSPACE}"

echo "================================================================="
echo "  亚马逊运营日报生成器 - 启动"
echo "  时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "================================================================="

# -------- 1. 检查 Python 环境 --------
echo ""
echo "[1/3] 检查 Python 环境..."
if ! command -v python3 >/dev/null 2>&1; then
    echo "[ERROR] 未检测到 python3，请先安装 Python 3。"
    exit 1
fi
PY_VERSION=$(python3 --version | awk '{print $2}')
echo "[OK] Python 版本: ${PY_VERSION}"

# 标准库已足够，无需 pip 安装；这里保留依赖检查作为占位
echo "[INFO] 日报生成器仅使用 Python 标准库（urllib / json / hmac / hashlib / datetime），无需额外依赖。"

# -------- 2. 检查配置文件与脚本 --------
echo ""
echo "[2/3] 检查脚本与配置..."
if [ ! -f "${CONFIG_FILE}" ]; then
    echo "[ERROR] 配置文件不存在: ${CONFIG_FILE}"
    exit 1
fi
if [ ! -f "${REPORT_SCRIPT}" ]; then
    echo "[ERROR] 日报生成脚本不存在: ${REPORT_SCRIPT}"
    exit 1
fi

# 读取 webhook 配置（仅用于提示）
WEBHOOK=$(python3 -c "
import json, sys
try:
    with open('${CONFIG_FILE}') as f:
        cfg = json.load(f)
    print(cfg.get('feishu_webhook_url', ''))
except Exception:
    print('')
" 2>/dev/null || true)

if [ -z "${WEBHOOK}" ] || echo "${WEBHOOK}" | grep -q "YOUR_HOOK_TOKEN"; then
    echo "[WARN] 未配置有效的飞书 Webhook URL，日报将在控制台打印，不会推送。"
    echo "       请编辑 ${CONFIG_FILE}，填入真实 webhook 地址。"
else
    echo "[OK] 已检测到飞书 Webhook 配置。"
fi

# -------- 3. 运行日报生成器 --------
echo ""
echo "[3/3] 运行亚马逊日报生成器..."
echo "-----------------------------------------------------------------"

set +e
python3 "${REPORT_SCRIPT}" 2>&1 | tee "${LOG_FILE}"
EXIT_CODE=${PIPESTATUS[0]}
set -e

echo "-----------------------------------------------------------------"
echo ""
if [ "${EXIT_CODE}" -eq 0 ]; then
    echo "[OK] 日报生成完成。日志: ${LOG_FILE}"
else
    echo "[ERROR] 日报生成失败 (exit=${EXIT_CODE})，请查看日志: ${LOG_FILE}"
    exit "${EXIT_CODE}"
fi

echo ""
echo "完成时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "================================================================="
