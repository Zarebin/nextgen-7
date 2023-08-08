import glob
import pandas as pd
import base64
import bs4
import hazm
from pathlib import Path

if __name__ == '__main__':
    csv_base_path = './data/csv_data/bad_files'
    save_dir = './data/csv_data/cleaned_data/'

    normalizer = hazm.Normalizer()

    files = glob.glob(csv_base_path + "/*.csv")
    for file in files:
        print(file)
        df = pd.read_csv(file)
        c = 0
        w = 0
        shit_list = 0

        main_text_list = list()
        og_description_list = list()

        for html in df['html']:
            try:
                base64_str = base64.b64decode(html + '==').decode()
                y = bs4.BeautifulSoup(base64_str, "html.parser")
            except UnicodeDecodeError:
                continue
            try:
                og_des = y.find("meta", property="og:description")['content']
                mio = y.find('body')
                for data in mio(['head', 'header', 'a', 'script', 'li', 'option', 'ul']):
                    data.decompose()
                main_text = ' '.join(mio.stripped_strings)
            except (TypeError, AttributeError):
                shit_list += 1

            if og_des == '':
                w += 1
                continue

            og_des = normalizer.normalize(og_des)
            main_text = normalizer.normalize(main_text)

            if og_des in main_text:
                main_text_list.append(main_text)
                og_description_list.append(og_des)
                c += 1
            else:
                w += 1

        print(c)
        print(w)
        print(shit_list)

        cleaned_data = pd.DataFrame({'main_text': main_text_list, 'og_description': og_description_list})

        name = file.split('/')[-1]
        filepath = Path(save_dir + name)
        cleaned_data.to_csv(filepath, index=False)
        print('done')
        print('----------------------------------------')
