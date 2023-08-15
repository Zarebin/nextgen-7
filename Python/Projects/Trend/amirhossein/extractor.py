class Extraxtor:
    def __init__(self, word_count):
        self._last_month_data = None
        self._cur_data = word_count


    def updata_data(self, word_count):
        for word, count in word_count.items():
            if word in self._cur_data:
                self._cur_data[word] += count
            else:
                self._cur_data[word] = count


    def updata_lastmonth(self):
        self._last_month_data = self._cur_data
        self._cur_data = {}


    def compute_ratio(self, word):
        if word in self._last_month_data and word in self._cur_data:
            return self._cur_data[word] / self._last_month_data[word]
        elif not word in self._cur_data:
            return 0
        else:
            return self._cur_data[word] / min(self._last_month_data.values())


    def get_trend(self):
        if self._last_month_data:
            word_ratio = {word: compute_ratio(word) for word in self._cur_data}
            return [word for word in word_ratio if word_ratio[word] == max(word_ratio.values())]
        else:
            return [word for word in self._cur_data if self._cur_data[word] == max(self._cur_data.values())]


