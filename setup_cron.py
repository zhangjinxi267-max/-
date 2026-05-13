#!/usr/bin/env python3
"""
定时任务设置脚本
用于设置亚马逊日报的每日推送
"""

import os
import sys
from crontab import CronTab


def setup_daily_cron(hour=9, minute=30):
    """设置每日定时任务"""
    print(f"🚀 正在设置每日 {hour:02d}:{minute:02d} 的定时任务...")
    
    # 获取当前脚本路径
    script_path = os.path.abspath(__file__)
    workspace_dir = os.path.dirname(script_path)
    report_script = os.path.join(workspace_dir, "amazon_daily_report.py")
    log_file = os.path.join(workspace_dir, "daily_report.log")
    
    # 创建CronTab
    cron = CronTab(user=True)
    
    # 移除旧任务（如果存在）
    cron.remove_all(comment='amazon_daily_report')
    
    # 添加新任务
    job = cron.new(
        command=f'cd {workspace_dir} && /usr/bin/python3 {report_script} >> {log_file} 2>&1',
        comment='amazon_daily_report'
    )
    
    # 设置时间
    job.hour.on(hour)
    job.minute.on(minute)
    
    # 保存
    cron.write()
    
    print(f"✅ 定时任务设置成功！")
    print(f"📅 执行时间：每天 {hour:02d}:{minute:02d}")
    print(f"📝 脚本路径：{report_script}")
    print(f"📋 日志文件：{log_file}")
    print(f"\n查看当前任务：crontab -l")
    print(f"查看日志：tail -f {log_file}")


def remove_cron():
    """移除定时任务"""
    cron = CronTab(user=True)
    cron.remove_all(comment='amazon_daily_report')
    cron.write()
    print("✅ 定时任务已移除")


def list_crons():
    """列出所有定时任务"""
    cron = CronTab(user=True)
    print("📋 当前定时任务：")
    for job in cron:
        print(f"  - {job}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # 默认设置9:30
        setup_daily_cron(9, 30)
    elif sys.argv[1] == "remove":
        remove_cron()
    elif sys.argv[1] == "list":
        list_crons()
    else:
        print("用法：")
        print("  python setup_cron.py              # 设置每日9:30的任务")
        print("  python setup_cron.py remove       # 移除任务")
        print("  python setup_cron.py list         # 列出任务")
