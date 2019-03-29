import schedule
import time
import threading
from datetime import datetime

from restaurants.models import UserNotification
from .db import get_users_to_notify
from util import ru_month, msg, restaurants
from restaurants import Materik


class ScheduleMenu(object):
    def __init__(self, dispatcher, interval=1):
        self.interval = interval
        self.dispatcher = dispatcher

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def notify(self):
        """
        Check if a user should be notified
        :return:
        """
        users_to_notify = get_users_to_notify()
        for user in users_to_notify:
            curr_hour, curr_min = datetime.now().hour, datetime.now().minute
            hour, minute = user["time"].split(":")
            if int(hour) == int(curr_hour + 3) and int(minute) == int(curr_min):
                weekdays = (6, 7)
                today = datetime.now()
                if today.isoweekday() in weekdays:
                    return

                if user["restaurant"] == restaurants["MATERIK"]:
                    day, month, menu = Materik.fetch_menu()
                    if day is not None and month is not None:
                        today = f"{int(day)}е {ru_month[int(month)]}"
                        business_lunch_menu = f"{msg['menu_for']} {today}\n{menu}"
                        self.dispatcher.process_update(
                            UserNotification(
                                chat_id=user["chat_id"],
                                msg=business_lunch_menu,
                                restaurant="materik",
                            )
                        )

                if user["restaurant"] == restaurants["VANGOG"]:
                    self.dispatcher.process_update(
                        UserNotification(
                            chat_id=user["chat_id"],
                            msg="меню ресторана вангог",
                            restaurant="vangog",
                        )
                    )

                if user["restaurant"] == restaurants["PIZZARONI"]:
                    self.dispatcher.process_update(
                        UserNotification(
                            chat_id=user["chat_id"],
                            msg="меню ресторана пиццарони",
                            restaurant="pizzaroni",
                        )
                    )

    def run(self):
        """ Running schedule """
        schedule.every(1).minutes.do(self.notify)
        while True:
            schedule.run_pending()
            time.sleep(self.interval)
