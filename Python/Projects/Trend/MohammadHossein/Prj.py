import numpy as np
import pandas as pd
import base64
from bs4 import BeautifulSoup
import re
from my_fun import *
from tqdm import tqdm

file1 = pd.read_csv('shana_all.csv')
num_urls = len(file1['url'])
enc = "utf-8"

web_lists = []
for i in range(num_urls):
    web = Website(file1['url'][i], file1['html'][i])
    web_lists.append(web)
    
# Extracting the HTML files with utf-8 encoding
for web in web_lists:
    html = web.html
    plaintext_bytes = base64.b64decode(str(html))
    plaintext_str = plaintext_bytes.decode(enc)
    web.html = plaintext_str

# Extracting the title and description from HTML files

for web in tqdm(web_lists, colour="#008fff", desc ="Progress: "):
    # find title
    soup = BeautifulSoup(web.html, features="html.parser")
    title = soup.title.string
    web.title = title
    #title_list.append(title)

    # find description
    metas = soup.find_all('meta')
    description = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ]
    if description:
        web.description = description[0]
    #description_list.append(description)

# Showing some titles and descriptions
#for i in range(15):

 #   print(title_list[-i])
  #print(description_list[-i])

# Define patterns
pattern_prepositions = r' در | این | برای | را | با | به | از |'
pattern_verbs = r'[ |\.]است[ |\.]| شد[ |ن|ه|\.]| هست[ |م|\.]| میباشد[ |\.]| بود[ |م|ی|ه|\.]| کرد[ |ن|م|ه|\.]| میشود[ |\.]| میکند[ |\.]| رسید[ |ی|م|ه|\.]| خواهد[ |\.]| داد[ |ن|\.]| شود[ |\.]| گفت[\.| ]| باش[ |د|ه|\.]| دارد|'
pattern_verbs_halfspace = r' می\u200cشود| می\u200cگذارد| می\u200cگوید| می\u200cدهد| می\u200cکند| می\u200cشود|'
pattern_conjunctions = r' و | که | تا | بر | هم | یا | آن | اما | باید | های | خود |'
pattern_spaces_etc = r' | می | ها |'
sub_pattern = r' |\.|,|<|>|\(|\)|<<|>>|:|\\|\/|\?|\!|؟|\+|\-|\|/|،|\:|»|«|-|\_|_'
pattern_date = r'[۱,۲][۰-۹]{3}|[1,2][0-9]{3}|^[1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1]\.|-|/|\\[1-9]|0[1-9]|1[0-2]\.|-|/|\\[0-9]{2}|[1,2][0-9]{3}$|^[0-9]{2}|[1,2][0-9]{3}\.|-|/|\\[1-9]|0[1-9]|1[0-2]\.|-|/|\\[1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1]$'
pattern = pattern_prepositions + pattern_verbs + pattern_verbs_halfspace + pattern_conjunctions + pattern_spaces_etc + pattern_date

# We have a problem: some verbs, prepositions, and conjunctions are popular in descriptions but aren't a trend! So we should remove them
title_words_list = []
description_words_list = []
title_date_list = []
description_date_list = []

for web in web_lists:
    title_without_shana = re.split(' - | \_ ' , web.title)
    title_without_shana = site_name_extractor(title_without_shana) + ' '
    title_date_list += re.findall(pattern_date, title_without_shana)
    title_without_shana = re.sub(sub_pattern, '  ', title_without_shana)
    title_words_list = title_words_list + list(filter(filter_undesired, re.split(pattern, title_without_shana)))
    description_without_shana = re.split(' - | \_ ' , str(web.description))
    description_without_shana = site_name_extractor(description_without_shana) + ' ' 
    description_date_list += re.findall(pattern_date, description_without_shana)
    description_without_shana = re.sub(sub_pattern, '  ', description_without_shana)
    description_words_list = description_words_list + list(filter(filter_undesired, re.split(pattern, description_without_shana)))
title_date_list = list(filter(filter_undesired, title_date_list))
description_date_list = list(filter(filter_undesired, description_date_list))
#print(title_words_list)
#print(description_words_list)

# Count trends for titles
title_words_df = pd.DataFrame(title_words_list)
print('Trends in titles:')
print(title_words_df.value_counts().head(60))


# Count trends for descriptions
description_words_df = pd.DataFrame(description_words_list)
print('\nTrends in descriptions:')
print(description_words_df.value_counts().head(60))

# Count trends for title_dates
title_date_df = pd.DataFrame(title_date_list)
print('Dates in titles:')
print(title_date_df.value_counts().head(10))


# Count trends for description_dates
description_date_df = pd.DataFrame(description_date_list)
print('\nDates in descriptions:')
print(description_date_df.value_counts().head(10))



