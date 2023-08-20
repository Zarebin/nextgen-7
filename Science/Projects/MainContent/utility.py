import base64


def b64_to_utf8(base64_page: str) -> str:
    """
    Converts a page with Base64 encoding to UTF-8.

    Args:
        base64_page (str): The Base64 encoded of an HTML page.
        
    Returns:
        string: The UTF-8 encoded of the HTML page.
    """
    return base64.b64decode(base64_page + '==').decode('utf-8', errors='ignore')
    
    
