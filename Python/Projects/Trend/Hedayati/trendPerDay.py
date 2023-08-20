import csv
import base64
import operator
import threading
from bs4 import BeautifulSoup
from htmldate import find_date
from myClasses import DataFile

htmldate1 = dict()
htmldate2 = dict()
htmldate3 = dict()
htmldate4 = dict()
htmldate5 = dict()
htmldate6 = dict()
htmldate7 = dict()
htmldate8 = dict()
htmldate9 = dict()
htmldate10 = dict()
htmldate11 = dict()
htmldate12 = dict()
htmldate13 = dict()
htmldate14 = dict()


def merg():
    htmldate1.update(htmldate2)
    htmldate1.update(htmldate3)
    htmldate1.update(htmldate4)
    htmldate1.update(htmldate5)
    htmldate1.update(htmldate6)
    htmldate1.update(htmldate7)
    htmldate1.update(htmldate8)
    htmldate1.update(htmldate9)
    htmldate1.update(htmldate10)
    htmldate1.update(htmldate11)
    htmldate1.update(htmldate12)
    htmldate1.update(htmldate13)
    htmldate1.update(htmldate14)
    return dict(sorted(htmldate1.items(), key=operator.itemgetter(1)))


def readingdate(datafile,htmldate):
    csv.field_size_limit(100000000)
    file = open(datafile.address)
    data = csv.DictReader(file)
    print("site of :",datafile.name)
    for site in data:
        url = site['url']
        html = site['html']
        # try to decode base64 html
        try:
            html = (base64.urlsafe_b64decode(html)).decode("utf-8")
        except UnicodeDecodeError:
            print("invalid encode!")
        except base64.binascii.Error:
            print("binascii error! (about not encoding with utf-8!)")

        soup = BeautifulSoup(html, 'html.parser')
        date = find_date(html)
        print("date of publish this page --> ", date)
        if html is not None and date is not None:
         htmldate[html]=date
    sorted_htmldate = dict(sorted(htmldate.items(), key=operator.itemgetter(1)))
    print(sorted_htmldate)


t1 = threading.Thread(target=readingdate, args=(DataFile("ana_press", "dataFiles/ana_press_all.csv"),htmldate1,))
t2 = threading.Thread(target=readingdate, args=(DataFile("asriran", "dataFiles/asriran_all.csv"),htmldate2,))
t3 = threading.Thread(target=readingdate, args=(DataFile("entekhab", "dataFiles/entekhab_all.csv"),htmldate3,))
t4 = threading.Thread(target=readingdate, args=(DataFile("farsnews", "dataFiles/farsnews_all.csv"),htmldate4,))
t5 = threading.Thread(target=readingdate, args=(DataFile("iscanews", "dataFiles/iscanews_all.csv"),htmldate5,))
t6 = threading.Thread(target=readingdate, args=(DataFile("isna", "dataFiles/isna_all.csv"),htmldate6,))
t7 = threading.Thread(target=readingdate, args=(DataFile("jahannews", "dataFiles/jahannews_all.csv"),htmldate7,))
t8 = threading.Thread(target=readingdate, args=(DataFile("khabaronline", "dataFiles/khabaronline_all.csv"),htmldate8,))
t9 = threading.Thread(target=readingdate, args=(DataFile("mashreghnews", "dataFiles/mashreghnews_all.csv"),htmldate9,))
t10 = threading.Thread(target=readingdate, args=(DataFile("mehrnews", "dataFiles/mehrnews_all.csv"),htmldate10,))
t11 = threading.Thread(target=readingdate, args=(DataFile("shana", "dataFiles/shana_all.csv"),htmldate11,))
t12 = threading.Thread(target=readingdate, args=(DataFile("tasnimnews", "dataFiles/tasnimnews_all.csv"),htmldate12,))
t13 = threading.Thread(target=readingdate, args=(DataFile("varzesh3", "dataFiles/varzesh3_all.csv"),htmldate13,))
t14 = threading.Thread(target=readingdate, args=(DataFile("yjcnews", "dataFiles/yjcnews_all.csv"),htmldate14,))

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()
t8.start()
t9.start()
t10.start()
t11.start()
t12.start()
t13.start()
t14.start()

t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
t6.join()
t7.join()
t8.join()
t9.join()
t10.join()
t11.join()
t12.join()
t13.join()
t14.join()

sorted_times = merg()


