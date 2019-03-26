import schedule
import time
import threading
from datetime import datetime

from restaurants.models import UserNotification
from .db import get_users_to_notify
from util import ru_month, msg
from restaurants import Materik


class ScheduleMenu(object):
    def __init__(self, dispatcher, interval=1):
        self.interval = interval
        self.dispatcher = dispatcher

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def notify(self):
        users_to_notify = get_users_to_notify()
        for user in users_to_notify:
            curr_hour, curr_min = datetime.now().hour, datetime.now().minute
            hour, minute = user["time"].split(":")
            if int(hour) == int(curr_hour + 3) and int(minute) == int(curr_min):
                weekdays = (6, 7)
                today = datetime.now()
                if today.isoweekday() in weekdays:
                    return

                day, month, menu = Materik.fetch_menu()
                if day is not None and month is not None:
                    today = f"{int(day)}е {ru_month[int(month)]}"
                    business_lunch_menu = f"{msg['menu_for']} {today}\n{menu}"
                    self.dispatcher.process_update(UserNotification(chat_id=user["chat_id"], msg=business_lunch_menu))

    def run(self):
        schedule.every(1).minutes.do(self.notify)
        while True:
            schedule.run_pending()
            time.sleep(self.interval)
