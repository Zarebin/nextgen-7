from extractor import Extraxtor
import schedule
import time


trend_extractor = Extraxtor({})


def call_update(word_count):
    global trend_extractor
    trend_extractor.updata_data(word_count)


def call_trend():
    global trend_extractor
    trends = trend_extractor.get_trend()
    print(f'trend word are {trends}')


def call_update_month():
    global trend_extractor
    trend_extractor.updata_lastmonth()


schedule.every(17).minutes.do(call_update)

schedule.every(1).days.do(call_trend)

schedule.every(30).days.do(call_update_month)

while True:
    schedule.run_pending()
    time.sleep(1)
