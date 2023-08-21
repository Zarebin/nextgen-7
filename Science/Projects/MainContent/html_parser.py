from lxml import html
from node import Node

class Parser():
    """
    To use this parser, create an object with the html_text (utf-8) and then call 'og_desc' method to get og description 
    or call 'leaves' with a list of tags (for example ['p', 'div']) to get a list of nodes of those tags that are in the bottom of the tree.
    Each element in this list is a Node object so you can use the methods in this class for each of these elements and generate features.
    """
    # TODO: fix the docstring

    def __init__(self, html_text: str) -> None:
        self._html = html_text
        self._root = html.fromstring(html_text)
        self._og_desc = self._find_og_desc(self._root)
        # TODO: we can use _clean_html here. 

    def og_desc(self) -> str:
        """
        Returns:
            str: The text of the og:description
        """
        return self._og_desc

    def root(self) -> Node:
        """
        Returns:
            Node: The root of the HTML page. Normally it will represent to the <html>.
        """
        return Node(self._root)

    def title(self) -> str:
        """
        Returns:
            str: Text of the page title.
        """
        return self._root.find('.//title').text

    def leaves(self, tags_list: list) -> list:
        """        
        Args:
            tags_list (str): List of tags to find in the leaves or near them.

        Returns:
            list[Node]: List of the lowest Nodes according to the tag_list in the HTML tree.
        """
        # TODO: impeove
        def check_list(n):
            if n.tag in tags_list:
                return n
            elif n.getparent().tag not in ['body', 'head']:
                return check_list(n.getparent())
            else:
                return None

        leaves_list = []
        for node in self._root.iter('*'):
            if len(node) == 0:
                node = check_list(node)
                if node is not None and node not in leaves_list:
                    leaves_list.append(node)
        
        return [Node(l) for l in leaves_list]

    def _clean_html(self) -> None:
        """
        Removes Irrelevant Parts, removes only tags where we need the text and removes tags with no text.

        Args:
            root (html.HtmlElement): The root of the HTML page.

        Returns:
            html.HtmlElement: The root of a clean HTML page.
        """

        # Remove Irrelevant Parts
        for node in self._root.xpath("//script | //noscript | //head | //header | //footer | //ul | //li | //ol | //nav | //style | //figure | //img | //form | //comment()"):
            node.getparent().remove(node)

        # Remove Irrelevant Tags
        for node in self._root.xpath("//a | //b | //i | //em | //strong"):
            node.drop_tag()

        # Remove Empty Tags
        # TODO: needs improvement. Tags with empty spaces are remaining.
        def recursive_empty(node):
            keep = node.text != None
            for c in node.getchildren():
                if recursive_empty(c):
                    keep = True
            
            if not keep:
                node.getparent().remove(node)
            return keep
        
        recursive_empty(self._root)

    @staticmethod
    def _find_og_desc(root: html.HtmlElement) -> str:
        """
        Extracts the og:description of the HTML page.

        Args:
            page (HtmlElement): The HTML page root.
            
        Returns:
            str: description content if exists.
            none: if there is no og:desctiption.
        """
        desc = root.xpath("//meta[@property='og:description']/@content")

        if len(desc) and len(desc[0].strip()):
            return desc[0].strip()
        else:
            return None
        
