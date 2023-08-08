'''
> Line 51: change open(... mode='w' ...) to mode='a' .
'''

import base64
import csv
from html.parser import HTMLParser

CSV_address = 'shana_all.csv'
Title, Date = '', ''
titleIsFound, dateIsFound = False, False
titleIsReady = False
Trends_file_address = 'Trends.csv'
Titles, Dates = [], []


class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        # print("Start tag:", tag)
        global Title, Date
        global titleIsFound, dateIsFound, titleIsReady
        if tag == 'title':
            titleIsReady = True
        elif tag == 'meta':
            dateLineIsFound = False
            for attr in attrs:
                if 'date' in attr[1]:
                    dateLineIsFound = True
                    continue
                if dateLineIsFound and attr[0] == 'content':
                    Date = attr[1]
                    dateIsFound, dateLineIsFound = True, False

    def handle_data(self, data):
        # print("Data     :", data)
        global Title, Date
        global titleIsFound, titleIsReady, dateIsFound
        if titleIsReady:
            Title = data
            titleIsReady = False
            titleIsFound = True


def decode_base64(my_b64_string):
    my_b64_bytes = my_b64_string.encode("UTF-8")
    decoded_bytes = base64.b64decode(my_b64_bytes)
    decoded_string = decoded_bytes.decode("UTF-8", errors='ignore')
    return decoded_string


def myMain():
    global Title, Date
    global titleIsFound, dateIsFound
    global Titles, Dates
    with open(file=CSV_address, mode='r', encoding='UTF-8', newline='') as CSV_file \
            , open(file=Trends_file_address, mode='w', encoding='UTF-8', newline='') as Trends_file:
        # , open(file='row2_value2.html', mode='w', encoding='UTF-8', newline='') as row2_value2_file:
        CSV_file_reader = csv.reader(CSV_file)
        row_BASE64 = ''
        rowNumber = 0  # start value : 0
        next(CSV_file_reader)  # skip the first line
        for row in CSV_file_reader:
            rowNumber += 1
            if row:
                row_BASE64 = row[1]
                row_HTML = decode_base64(row_BASE64)
                row_Lines = row_HTML.splitlines()
                # row2_value2_file.writelines(row_HTML)
                '''##########################################################'''
                myParser = MyHTMLParser()
                for line in row_Lines:
                    myParser.feed(line)
                    if titleIsFound and dateIsFound:
                        titleIsFound, dateIsFound = False, False
                        myParser.close()
                        # ver-1.0 output >>>
                        '''
                        print('>>>>>  News Number:', rowNumber, '  <<<<<')
                        print(Title)
                        print(Date)
                        print("\n")
                        # '''
                        # ver-2.0 output >>>
                        Trends_file_writer = csv.writer(Trends_file)
                        Trends_file_writer.writerow([Title, Date])
                        Titles.append(Title)
                        Dates.append(Date)
                        break


myMain()
