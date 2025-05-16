

'''
Configure the canonical domain and prefix for the article URLS.
This should be removed an placed in each articles meta data.
Each article should have a canonical URL but it should not be
assumed that the canonical URL is the same as the article URL.
'''
DOMAIN = "https:ozprealpha.com/"


'''
Configure the directories for the project.
'''
SITE_MAP = "site-map.json"
CANON = "canonical"
PUBLISH = "publish"
WORKING = "working"
TEMPLATES_DIR = "templates"
STATIC_DIR = "templates/static"


'''
Configure the ports for the development and production servers.
'''
DEBUG = True
CACHE_DELAY = 60 * 60
PROD_PORT = 8080
DEV_PORT = 8765


