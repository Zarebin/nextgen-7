import base64
import bs4
import hazm


def isBase64(s):
    try:
        return base64.b64encode(base64.b64decode(s)) == s
    except Exception:
        return False


def get_normalized_main_text(html_data_string):
    main_text = get_main_text(html_data_string)
    normalizer = hazm.Normalizer()
    return normalizer.normalize(main_text)


def get_main_text(html_data_string):
    html_string = None
    bs4_obj = None
    if isBase64(html_data_string):
        html_string = base64.b64decode(html_data_string)
        bs4_obj = bs4.BeautifulSoup(html_string, 'html.parser')
    else:
        bs4_obj = bs4.BeautifulSoup(html_data_string, 'html.parser')

    # remove unwanted tags
    mio = bs4_obj.find('body')
    for data in mio(['head', 'header', 'a', 'script', 'li', 'option', 'ul']):
        data.decompose()
    main_text = ' '.join(mio.stripped_strings)

    return main_text
