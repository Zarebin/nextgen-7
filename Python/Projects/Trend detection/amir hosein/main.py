from extractor import Extractor
import schedule
import time
# from ... import word_counter

trend_extractor = Extractor(word_counter())


def call_update_cur(word_count):
    global trend_extractor
    trend_extractor.update_cur(word_counter())


def call_trend():
    global trend_extractor
    trends = trend_extractor.get_trend()
    print(f'trend word are {trends}')


def call_update_avg():
    global trend_extractor
    trend_extractor.updata_avg()


schedule.every(5).minutes.do(call_update_cur)

schedule.every(30).minutes.do(call_trend)

schedule.every(17).minutes.do(call_update_avg)

while True:
    schedule.run_pending()
    time.sleep(1)
