#pooria_trend_project
#!/usr/bin/env python3
import csv
import sys
import os
from urllib.parse import unquote
from collections import Counter
from hazm import word_tokenize, Normalizer, stopwords_list



csv.field_size_limit(sys.maxsize) 
directory_path = "/home/pooria/zarebin/16_-_توسعه_دهنده_نرم_افزار_-_پایتون_(Python_Developer)_-_ذره_بین/KarAmouzi/" #csvs_directory_address
file_list = os.listdir(directory_path)
words = []
for filename in file_list:
    file_path = os.path.join(directory_path, filename)
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        rows = []
        i = 0
        for row in reader:
            if not row in rows:    
                rows.append(row)
                title = unquote(rows[i][0].split("/")[-1])
                words.extend(title.split("-"))
                i = i + 1



normalizer = Normalizer()
def filter_verbs_prepositions(lst):
    filtered_list = []
    for word in lst:
        normalized_word = normalizer.normalize(word)
        if normalized_word not in stopwords_list() and not normalized_word.isdigit():
            if not (normalized_word == (''or'ها'or'های')):                            
                filtered_list.append(normalized_word)
    return filtered_list



final_words = filter_verbs_prepositions(words)        
hash_list = [tuple(item) for item in final_words]
Count = Counter(hash_list)
ans = Count.most_common(20) 
for item, count in ans :
    out = ''
    for letter in item :
        out = out + letter
    print("trend:",out,"mention:",count)    
