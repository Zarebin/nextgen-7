harfeEzafeHa = 'به با از تا بر اندر در پی بهر سوی چون برای جز بدون'.split()
harfeRabtHa = 'و یا اگر چنانچه اما ولی'.split()
feaelHa = 'است گفت شد'.split()
stopWords = set(harfeEzafeHa + harfeRabtHa + feaelHa)


def remove_stopwords(inputList: list):
    return [word for word in inputList if word not in stopWords]
