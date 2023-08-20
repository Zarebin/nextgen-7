from lxml import html


class Node():
    def __init__(self, html_element: html.HtmlElement) -> None:
        self._node = html_element

    def tag(self) -> str:
        """
        Returns:
            str: The html tag of the node.
        """
        return self._node.tag

    def classes(self) -> list[str]:
        """
        Returns:
            list[str]: A list of classes of the node.
        """
        return list(self._node.classes)

    def path(self) -> list[str]:
        """
        Returns:
            list[str]: A list showing the path of the node. Starts with the parent and ends with the root.
        """
        ancestors = list(self._node.iterancestors())
        return [n.tag for n in ancestors]

    def children(self) -> list['Node']:
        """
        Returns:
            list: A list of children nodes of the node. Empty list if there is no children.
        """
        children = self._node.getchildren()
        children = [Node(c) for c in children]
        return children

    def parent(self) -> 'Node':
        """
        Returns:
            Node: The node's parent.
            None: If there is no parents.
        """
        return self._node.getparent()

    def text_length(self) -> int:
        """
        Returns:
            int: The length of the node's text
        """
        text = self._node.text_content()
        return len(text)
    
    def word_count(self) -> int:
        """
        Returns:
            int: The word count of the node's text
        """
        text = self._node.text_content()
        word_list = text.split() # TODO: use a better approach
        return len(word_list)
    
    def depth(self) -> int:
        """
        Returns:
            int: The depth of the node in the html tree.
        """
        return len(list(self._node.iterancestors()))