from flask_apscheduler import APScheduler
from db.sync_hrdb_info import update_attendance, sync_data
SCHEDULER_TIMEZONE = 'Asia/Shanghai'
SCHEDULER_API_ENABLED = True
JOBS = [
    {
        'id': 'sync_data',
        'func': 'cron.apscheduler:sync_data',
        'trigger': 'cron',
        'hour': '1-2',
        'minute': '*/30'
    },
    {
        'id': 'update_attendance',
        'func': 'cron.apscheduler:update_attendance',
        'trigger': 'cron',
        'hour': '7-18',
        'minute': '*/5'
    }
]
scheduler = APScheduler()



