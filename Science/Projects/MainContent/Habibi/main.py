import os
import base64
import hazm
from lxml import html
import pandas as pd


DATASET_DIR = "minidataset/"
normalizer = hazm.Normalizer()

def load_pages():
    """
    Loads all html cells from the dataset and return them in a single list
    """
    all_pages = []
    for f in os.scandir(DATASET_DIR):
        pages = pd.read_csv(f.path)
        pages = pages['html'].tolist()
        all_pages += pages
    return all_pages

def b64_to_utf8(base64_page: str):
    """
    Converts a page with base64 encoding to utf-8 
    """
    base64_page += "=" * (len(base64_page) % 4) # fixes the padding issue
    return base64.b64decode(base64_page).decode('utf-8', errors='ignore') # TODO: must fix errors with another approach / wiered output

def get_description(page):
    """
    Returns og:description content if exists and None if not.
    """
    tree = html.fromstring(page) 
    desc = tree.xpath("//meta[@property='og:description']/@content")
    if len(desc) == 0: # Discard pages with no description
        return None
    desc = desc[0].strip()
    if len(desc) == 0: # Discard pages with empty description
        return None
    return desc

def clean_page(page):
    """
    Removes irrelevant parts and finally html tags.
    """
    tree = html.fromstring(page)
    for node in tree.xpath("//script | //head | //nav | //ul | //header | //style | //noscript"):
        node.getparent().remove(node)
    
    return tree.text_content().strip()

def normalize(text):
    return normalizer.normalize(text)


def parse_html(raw_htmls: list):
    """
    Returns a list of tuples of description and clean content of pages.
    """
    desc_content = []
    for page in raw_htmls:
        desc = get_description(page)
        if not desc:
            continue
        clean = normalize(clean_page(page))
        desc_content.append((desc, clean))
    return desc_content
 
if __name__ == '__main__':
    pages = load_pages()
    pages = [b64_to_utf8(p) for p in pages]
    desc_content = parse_html(pages)

    # ---- testing

    print(desc_content[10][0])
    print('----')
    print(desc_content[10][1])
