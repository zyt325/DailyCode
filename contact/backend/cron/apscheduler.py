from flask_apscheduler import APScheduler
from db.sync_hrdb_info import update_people, update_attendance
SCHEDULER_TIMEZONE = 'Asia/Shanghai'
SCHEDULER_API_ENABLED = True
JOBS = [
    {
        'id': 'update_people',
        'func': 'cron.apscheduler:update_people',
        'trigger': 'interval',
        'minutes': 8
    },
    {
        'id': 'update_attendance',
        'func': 'cron.apscheduler:update_attendance',
        'trigger': 'interval',
        'minutes': 5
    }
]
scheduler = APScheduler()



