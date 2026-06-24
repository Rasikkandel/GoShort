"""
Application-level constants for the URL shortening app.
"""

# Short code generation
SHORT_CODE_LENGTH = 6
SHORT_CODE_CHARSET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
BASE62 = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

# URL constraints
MAX_URL_LENGTH = 2048
MIN_URL_LENGTH = 1

# Click tracking
DEFAULT_CLICK_COUNT = 0
LOW_CLICK_THRESHOLD = 10
MEDIUM_CLICK_THRESHOLD = 100

# Error messages
ERROR_EMPTY_URL = 'Please enter a URL'
ERROR_INVALID_URL = 'Invalid URL format'
ERROR_URL_CREATION = 'Error creating short URL: {}'
ERROR_URL_NOT_FOUND = 'Short URL not found'
ERROR_URL_DELETION = 'Error deleting URL: {}'

# Success messages
SUCCESS_URL_CREATED = 'URL shortened successfully!'
SUCCESS_URL_DELETED = 'Link deleted successfully!'
SUCCESS_CLICK_RESET = 'Click counts reset successfully!'
