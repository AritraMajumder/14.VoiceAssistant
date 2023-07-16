import datetime
import time
from winotify import Notification,audio 

def check_notification(user_date, user_time):
    target_datetime = datetime.datetime.strptime(user_date + " " + user_time, "%Y-%m-%d %H:%M")
    toast = Notification(app_id="Voice assistant",
                         title="Reminder",
                         msg="This is a reminder",
                         duration="short")
    toast.set_audio(audio.Default, loop=False)
                            
    while True:
        current_datetime = datetime.datetime.now()

        if current_datetime >= target_datetime:
            toast.show()
            break

        # Wait for 1 second before checking again
        time.sleep(1)

# Example usage
date = "2023-07-16"
clk = "13:54"
check_notification(date, clk)
