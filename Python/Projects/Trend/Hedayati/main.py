import csv
import base64
import operator
from htmldate import find_date
from myClasses import DataFile
from myClasses import Counter
from bs4 import BeautifulSoup

csv.field_size_limit(100000000)
# key,value for (word,count)
trends = dict()

all_files = [DataFile("ana_press", "dataFiles/ana_press_all.csv"), DataFile("asriran", "dataFiles/asriran_all.csv"),
             DataFile("entekhab", "dataFiles/entekhab_all.csv"), DataFile("farsnews", "dataFiles/farsnews_all.csv"),
             DataFile("iscanews", "dataFiles/iscanews_all.csv"), DataFile("isna", "dataFiles/isna_all.csv"),
             DataFile("jahannews", "dataFiles/jahannews_all.csv"),
             DataFile("khabaronline", "dataFiles/khabaronline_all.csv"),
             DataFile("mashreghnews", "dataFiles/mashreghnews_all.csv"),
             DataFile("mehrnews", "dataFiles/mehrnews_all.csv"),
             DataFile("shana", "dataFiles/shana_all.csv"), DataFile("tasnimnews", "dataFiles/tasnimnews_all.csv"),
             DataFile("varzesh3", "dataFiles/varzesh3_all.csv"), DataFile("yjcnews", "dataFiles/yjcnews_all.csv")]

for datafile in all_files:
    file = open(datafile.address)
    data = csv.DictReader(file)
    url_counter = 1
    for site in data:
        print("url number of ",url_counter, ":")
        print(site['url'])
        html = site['html']

        # try to decode base64 html
        try:
            html = (base64.urlsafe_b64decode(html)).decode("utf-8")
        except UnicodeDecodeError:
            print("invalid encode!")
        except base64.binascii.Error:
            print("binascii error! (about not encoding with utf-8!)")

        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title
        date = find_date(html)
        print("date of publish this page --> ", date)

        if title is not None:
            count = Counter.count(title.string, trends)
            print(count)
            print("trend until now : ")
            sorted_trends = dict(sorted(trends.items(), key=operator.itemgetter(1)))
            print(sorted_trends)
        else:
            print("no title!")

        url_counter = url_counter + 1
        print(" ")
        print(" ")

    file.close()
