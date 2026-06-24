"""
Utility functions for the URL shortening app.
"""

import random
import string
from .constants import SHORT_CODE_LENGTH, SHORT_CODE_CHARSET, BASE62


def base62_encode(num):
    """
    Convert a number to base62.
    
    Args:
        num (int): Number to encode
        
    Returns:
        str: Base62 encoded string
    """
    if num == 0:
        return BASE62[0]
    
    result = []
    while num > 0:
        remainder = num % 62
        result.append(BASE62[remainder])
        num //= 62
    
    return ''.join(reversed(result))


def base62_decode(encoded):
    """
    Decode a base62 string to a number.
    
    Args:
        encoded (str): Base62 encoded string
        
    Returns:
        int: Decoded number
    """
    result = 0
    for char in encoded:
        result = result * 62 + BASE62.index(char)
    return result


def generate_short_code(length=None):
    """
    Generate a random short code.
    
    Args:
        length (int): Length of the short code. Defaults to SHORT_CODE_LENGTH constant
        
    Returns:
        str: Random short code
    """
    if length is None:
        length = SHORT_CODE_LENGTH
    return ''.join(random.choices(SHORT_CODE_CHARSET, k=length))


def is_valid_url(url):
    """
    Validate if a string is a valid URL.
    
    Args:
        url (str): URL string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not url or not isinstance(url, str):
        return False
    
    # Basic URL validation
    url = url.strip()
    if len(url) < 4 or len(url) > 2048:
        return False
    
    # Check for valid URL patterns
    valid_schemes = ('http://', 'https://', 'ftp://', 'ftps://')
    return any(url.lower().startswith(scheme) for scheme in valid_schemes)


def truncate_string(text, length=50):
    """
    Truncate a string to a specified length and add ellipsis.
    
    Args:
        text (str): Text to truncate
        length (int): Maximum length. Defaults to 50
        
    Returns:
        str: Truncated text with ellipsis if needed
    """
    if len(text) <= length:
        return text
    return text[:length] + '...'


def get_click_status(clicks):
    """
    Get the status indicator based on click count.
    
    Args:
        clicks (int): Number of clicks
        
    Returns:
        tuple: (status_name, status_class, status_icon)
    """
    from .constants import LOW_CLICK_THRESHOLD, MEDIUM_CLICK_THRESHOLD
    
    if clicks == 0:
        return ('No Activity', 'secondary', 'fa-circle-notch')
    elif clicks < LOW_CLICK_THRESHOLD:
        return ('Active', 'warning', 'fa-arrow-trend-up')
    elif clicks < MEDIUM_CLICK_THRESHOLD:
        return ('Popular', 'info', 'fa-chart-line')
    else:
        return ('Very Popular', 'success', 'fa-star')
