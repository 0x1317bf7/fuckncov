import os
import values

from apscheduler.schedulers.background import BlockingScheduler

scheduler = BlockingScheduler()


def exec_task() -> None:
    os.system("python3 fuckncov.py")


def main() -> None:
    values.init()
    exec_task()
    hm = str(values.time).split(":")
    scheduler.add_job(exec_task, 'cron', day_of_week=values.day_of_week, hour=hm[0], minute=hm[1])
    scheduler.start()


if __name__ == "__main__":
    main()
