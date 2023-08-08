class DataFile:
    name = None
    address = None

    def __init__(self,name,address):
        self.name=name
        self.address=address


class Cleaner:

    def cleanWord(str):
        return str.replace("/", "").replace("\\", "").replace("|","").replace("\u200c"," ")\
            .replace("،","").replace("«", "").replace("»","").replace("(","").replace(")","")\
            .replace("?","").replace("!","")

    def removeWord(word):
        result = word
        if len(word) == 0 or len(word) == 1 or len(word) == 2 or word == "شده" \
                or word == "خواهد" or word == "همه" or word == "برای" or word == "است" or word == "می‌شود"\
                or word == "باشد" or word == "کرد" or word == "می کند" or word == "های" or word == "نیست" \
                or word == "بود" or word == "دارد" or word == "شدند" or word == "'(عکس)" or word == "(فیلم)"\
                or word == "(+عکس)" or word == "شود" or word == "این" or word == "اگر" or word == "کنند"\
                or word == "اما" or word == "درباره" or word == "باید" or word == "است" or word == "نمی"\
                or word == "ندارد" or word == "باشد" or word == "دیگر":
            result = None
        return result


class Counter:

    def count(str,trends):

        str = str.replace(" | سایت انتخاب","").replace(" | خبرگزاری فارس","").replace(" - ایسنا","")\
            .replace(" - جهان نيوز","").replace(" - خبرآنلاین","").replace(" - مشرق نیوز","")\
            .replace(" - خبرگزاری مهر | اخبار ایران و جهان | Mehr News Agency","").replace(" - شانا","")\
            .replace("- اخبار سیاسی تسنیم | Tasnim | خبرگزاری تسنیم | Tasnim ","")\
            .replace("- اخبار بین الملل تسنیم | Tasnim | خبرگزاری تسنیم | Tasnim ","")\
            .replace("- اخبار ورزشی تسنیم | Tasnim | خبرگزاری تسنیم | Tasnim ","")\
            .replace("- اخبار اقتصادی تسنیم | Tasnim | خبرگزاری تسنیم | Tasnim ","")\
            .replace("- اخبار استانها تسنیم | Tasnim | خبرگزاری تسنیم | Tasnim ","")\
            .replace("- اخبار فرهنگی تسنیم | Tasnim | خبرگزاری تسنیم | Tasnim ","")\
            .replace("- اخبار بازار تسنیم | Tasnim | خبرگزاری تسنیم | Tasnim ","")\
            .replace("- اخبار اجتماعی تسنیم | Tasnim | خبرگزاری تسنیم | Tasnim ","")\
            .replace(" - ورزش سه","").replace("+ فیلم","")

        if str is not None:
         print("counting words of this title --> ",str)

        counts = dict()
        words = str.split()

        for word in words:
            word = Cleaner.removeWord(word)
            if word is None:
                continue

            word = Cleaner.cleanWord(word)
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
            if word in trends:
                trends[word] += 1
            else:
                trends[word] = 1

        return counts








