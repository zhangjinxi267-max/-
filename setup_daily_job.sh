#!/bin/bash
# 亚马逊日报定时任务设置脚本
# 每日自动生成运营报告

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORT_SCRIPT="$SCRIPT_DIR/amazon_daily_report.py"
LOG_FILE="$SCRIPT_DIR/daily_report.log"

echo "========================================"
echo "  亚马逊日报定时任务设置"
echo "========================================"
echo ""

# 检查Python脚本是否存在
if [ ! -f "$REPORT_SCRIPT" ]; then
    echo "❌ 错误：找不到 $REPORT_SCRIPT"
    exit 1
fi

# 询问用户
echo "请选择操作："
echo "1) 设置每日 9:30 定时任务（推荐）"
echo "2) 自定义时间"
echo "3) 查看当前任务"
echo "4) 移除定时任务"
echo "5) 立即运行一次"
echo ""
read -p "请输入选项 (1-5): " choice

case $choice in
    1)
        CRON_TIME="30 9 * * *"
        echo "⏰ 设置时间：每天 09:30"
        ;;
    2)
        echo "请输入Cron表达式（例如：30 9 * * * 表示每天9:30）"
        read -p "Cron表达式: " CRON_TIME
        ;;
    3)
        echo "📋 当前定时任务："
        crontab -l | grep -v '^#'
        exit 0
        ;;
    4)
        echo "🗑️ 正在移除定时任务..."
        crontab -l | grep -v 'amazon_daily_report' | crontab -
        echo "✅ 定时任务已移除"
        exit 0
        ;;
    5)
        echo "🚀 立即运行日报生成器..."
        cd "$SCRIPT_DIR" && python3 "$REPORT_SCRIPT"
        exit 0
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac

# 添加定时任务（先移除旧的）
echo "📝 更新定时任务..."
crontab -l | grep -v 'amazon_daily_report' > /tmp/crontab.tmp
echo "$CRON_TIME cd $SCRIPT_DIR && /usr/bin/python3 $REPORT_SCRIPT >> $LOG_FILE 2>&1 # amazon_daily_report" >> /tmp/crontab.tmp
crontab /tmp/crontab.tmp
rm /tmp/crontab.tmp

echo ""
echo "========================================"
echo "  ✅ 定时任务设置成功！"
echo "========================================"
echo ""
echo "📅 执行时间：$CRON_TIME"
echo "📝 脚本路径：$REPORT_SCRIPT"
echo "📋 日志文件：$LOG_FILE"
echo ""
echo "常用命令："
echo "  查看任务：crontab -l"
echo "  查看日志：tail -f $LOG_FILE"
echo "  立即运行：cd $SCRIPT_DIR && python3 amazon_daily_report.py"
echo ""
