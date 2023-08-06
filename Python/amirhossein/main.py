from rss import fetch_data, update_data
import schedule
import time


schedule.every(5).seconds.do(update_data)

fetch_data()

while True:
    schedule.run_pending()
    time.sleep(1)
    
