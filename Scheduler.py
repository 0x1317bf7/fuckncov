from datetime import datetime, timedelta

import apscheduler.job
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.start()


def release():
    scheduler.shutdown(wait=False)


def add_delay_task(function, delay: int) -> apscheduler.job.Job:
    date = datetime.now() + timedelta(seconds=delay)
    print("set delay task : " + str(date))
    job = scheduler.add_job(function, 'date', run_date=date)
    return job


def add_schedule_task(function, day_of_week, hour, minute) -> apscheduler.job.Job:
    job = scheduler.add_job(function, 'cron', day_of_week=day_of_week, hour=hour, minute=minute)
    return job


def remove_task(job: apscheduler.job.Job):
    if scheduler.get_job(job.id) is not None:
        scheduler.remove_job(job.id)
