'''
Configure the canonical domain and prefix for the article URLS.
This should be removed an placed in each articles meta data.
Each article should have a canonical URL but it should not be
assumed that the canonical URL is the same as the article URL.
'''

DOMAIN = "https:ozprealpha.com/"
CANON_PREFIX = "archive/"


'''
Configure the directories for the project.
'''

STATIC_DIR = "static"
ASSETS_DIR = "assets"
TEMPLATES_DIR = "templates"
CONTENT_DIR = "content"
CANONICAL_DIR = "canonical"


'''
Configure the ports for the development and production servers.
'''

DEBUG = True
CACHE_DELAY = 60 * 60
PROD_PORT = 8080
DEV_PORT = 8765


