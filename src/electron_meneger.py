import subprocess
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import os
import stat



def create_electron():
    elec = subprocess.Popen('tonation.exe')
    setup_scheduler(elec)


def check_for_electron_close(elec):
    poll = elec.poll()
    if poll is None:
        print(elec.communicate())
        os._exit(1)

def setup_scheduler(elec):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=lambda: check_for_electron_close(elec), trigger="date")
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())