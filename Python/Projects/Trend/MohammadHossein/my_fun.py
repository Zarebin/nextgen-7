# This function detects the site name from main title and discards it
def site_name_extractor(string):
    if len(string) <= 1:
        return string[0]
    elif len(string[0]) >= len(string[1]):
        return string[0]
    else:
        return string[1]

# This function handles the difference between meaningfull & meaningless words (with less than 3 letters)
def filter_undesired(string):
    if string == None:
        return False
    elif len(string) <= 2:
        return False
    else:
        return True

class Website():

    def __init__(self, url, html):
        self._url = url
        self._html = html
        self._title = None
        self._description = None

    @property 
    def title(self):
        return self._title

    @title.setter
    def title(self, val):
        self._title = val

    @property 
    def description(self):
        return self._description

    @description.setter
    def description(self, val):
        self._description = val

    @property 
    def url(self):
        return self._url

    @url.setter
    def url(self, val):
        self._url = val

    @property 
    def html(self):
        return self._html

    @html.setter
    def html(self, val):
        self._html = val

   
