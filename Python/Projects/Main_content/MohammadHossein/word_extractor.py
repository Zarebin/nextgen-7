import numpy as np
import pandas as pd
#import base64
#from bs4 import BeautifulSoup
import re
#from tqdm import tqdm


def word_counter(text):
    """
    Get a text and extract words by their count
    """
    text_processed = pre_process_text(text) # arabic to persian
    words = extract_words(text_processed) # change + to spaces and splite them with spaces 
    words_without_stopwords = words#remove_stopwords(words) # Mahdi Atashi 
    words_df = pd.DataFrame(words_without_stopwords)
    word_counts = words_df.value_counts()
    trends_dict = word_counts.to_dict()
    return trends_dict


def pre_process_text(text): # todo: Arabic to Persian
    pattern = r'-|_|\.|,|<|>|\(|\)|<<|>>|:|\*|\\|\/|\?|\!|؟|\+|\|/|،|\:|»|«|\_' 
    processed_text = re.sub(pattern,' ', text)
    return processed_text



def extract_words(text_processed): # Remove site name - Thanks miss Hedayati 
    text_without_sitename = re.sub(r"خبرگزاری فارس|ایسنا|سایت انتخاب|جهان نیوز|خبر آنلاین|خبرآنلاین|مشرق نیوز|اخبار ایران و جهان|خبرگزاری مهر|خبرگزاری تسنیم|اخبار سیاسی تسنیم|اخبار بین‌الملل تسنیم|اخبار بین الملل تسنیم|اخبار ورزشی تسنیم|اخبار اقتصادی تسنیم|اخبار استانها تسنیم|اخبار فرهنگی تسنیم|اخبار بازار تسنیم|شانا|اخبار اجتماعی تسنیم|ورزش سه|فیلم \+|Tasnim|Mehr News Agency", ' ', text_processed)
    #text_processed.replace(" | سایت انتخاب","").replace(" | خبرگزاری فارس","").replace("ایسنا","")\
          #  .replace("جهان نيوز","").replace("خبرآنلاین","").replace("مشرق نیوز","")\
         #   .replace("خبرگزاری مهر | اخبار ایران و جهان | Mehr News Agency","").replace("شانا ","")\
        #    .replace("اخبار سیاسی تسنیم | Tasnim | خبرگزاری تسنیم | Tasnim ","")\
       #     .replace("اخبار بین الملل تسنیم | Tasnim | خبرگزاری تسنیم | Tasnim ","")\
      #      .replace("اخبار ورزشی تسنیم | Tasnim | خبرگزاری تسنیم | Tasnim ","")\
     #       .replace("اخبار اقتصادی تسنیم | Tasnim | خبرگزاری تسنیم | Tasnim ","")\
    #        .replace("اخبار استانها تسنیم | Tasnim | خبرگزاری تسنیم | Tasnim ","")\
   #         .replace("اخبار فرهنگی تسنیم | Tasnim | خبرگزاری تسنیم | Tasnim ","")\
  #          .replace("اخبار بازار تسنیم | Tasnim | خبرگزاری تسنیم | Tasnim ","")\
 #           .replace("اخبار اجتماعی تسنیم | Tasnim | خبرگزاری تسنیم | Tasnim ","")\
#            .replace("ورزش سه","").replace("فیلم","")
    words_list = list(filter(filter_undesired, re.split(' +', text_without_sitename)))
    return words_list



def filter_undesired(string):
    if string == None or len(string) <= 1:
        return False
    else:
        return True





