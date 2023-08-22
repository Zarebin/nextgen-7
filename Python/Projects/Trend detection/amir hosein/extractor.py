class Extractor:
    def __init__(self, word_count):
        self.update_step = 1
        self.avg_freq = {}
        self.cur_freq = word_count


    def update_cur(self, word_count):
        for word, count in word_count.items():
            if word in self.cur_freq:
                self.cur_freq[word] += count
            else:
                self.cur_freq[word] = count


    def update_avg(self):
        if self.update_step > 1:
            for word, count in self.cur_freq.items():
                if word in self.avg_freq:
                    self.avg_freq[word] = (count + (self.update_step - 1) * self.avg_freq[word]) / (self.update_step)
                else:
                    self.avg_freq[word] = count / self.update_step

        else:
            self.avg_freq = self.cur_freq.copy()

        self.cur_freq = {}
        self.update_step += 1

    def compute_ratio(self, word):
        if word in self.avg_freq and word in self.cur_freq:
            return self.cur_freq[word] / self.avg_freq[word]
        elif not word in self.cur_freq:
            return 0
        else:
            return self.cur_freq[word] / min(self.avg_freq.values())


    def get_trend(self):
        if self.avg_freq:
            word_ratio = {word: self.compute_ratio(word) for word in self.cur_freq}
            return [word for word in word_ratio if word_ratio[word] == max(word_ratio.values())]
        else:
            return [word for word in self.cur_freq if self.cur_freq[word] == max(self.cur_freq.values())]


