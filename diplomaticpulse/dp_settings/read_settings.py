from scrapy.utils.project import get_project_settings


settings = get_project_settings()


def skip_url_extension():
    """ read skipped url extension"""
    return settings["SKIP_URL_EXTENSION"]

def get_languages():
    """ read skipped url extension"""
    return settings["ARTICLES_LANGUAGE"]