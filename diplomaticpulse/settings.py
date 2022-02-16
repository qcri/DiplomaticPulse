# -*- coding: utf-8 -*-

import os

BOT_NAME = "diplomaticpulse"

SPIDER_MODULES = ["diplomaticpulse.spiders"]
NEWSPIDER_MODULE = "diplomaticpulse.spiders"

# To activate an Item Pipeline component we must add its class to the ITEM_PIPELINES setting
# The integer values you assign to classes in this setting determine the order they run in- items go through pipelines from order number low to high.  you can set them  in the 0-1000 range
ITEM_PIPELINES = {
    "diplomaticpulse.pipelines.ElasticSearchPipeline": 800,
    "diplomaticpulse.duplicatepipeline.DuplicatesPipeline": 500,
    "diplomaticpulse.droppipeline.DropItemPipeline": 400,
}

# the SPIDER_CONTRACTS is used for our custom Contracts, it is a dict containing the scrapy contracts enabled in your project, used for testing spiders.
SPIDER_CONTRACTS = {
    "diplomaticpulse.contracts.test_contracts.HasLinkContract": 500,
}

# extension
EXTENSIONS = {
    "scrapy.extensions.closespider.CloseSpider": 400,
}
DOWNLOADER_MIDDLEWARES = {
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    "rotating_proxies.middlewares.BanDetectionMiddleware": 620,
    "scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware": 350,
    "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 810,
}
CLOSESPIDER_ITEMCOUNT = 20
CLOSESPIDER_TIMEOUT = 120
# The maximum depth that will be allowed to crawl for any site. If zero, no limit will be imposed.
DEPTH_LIMIT = 0
# Debug mode conguration
LOG_LEVEL = "INFO"
# Maximum number of concurrent items (per response) to process in parallel in the Item Processor, default is 100
CONCURRENT_ITEMS = 10
# This param is used at an empty ES index
CLOSESPIDER_PAGECOUNT = 50
# The amount of time (in secs) that the downloader should wait before downloading consecutive pages, default is 0
DOWNLOAD_DELAY = 2
# The maximum number of concurrent (ie. simultaneous) requests that will be performed by the Scrapy downloader. (default: 16)
CONCURRENT_REQUESTS = 8
# The maximum number of concurrent (ie. simultaneous) requests that will be performed to any single domain. default is 8
CONCURRENT_REQUESTS_PER_DOMAIN = 8
# The maximum number of concurrent (ie. simultaneous) requests that will be performed to any single IP. If non-zero, the CONCURRENT_REQUESTS_PER_DOMAIN s
# etting is ignored, and this one is used instead. In other words, concurrency limits will be applied per IP, not per domain, default is 0
CONCURRENT_REQUESTS_PER_IP = 16
# Disable cookies (enabled by default)
COOKIES_ENABLED = True
# Enable and configure the AutoThrottle extension (disabled by default) See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0  # Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True
ELASTIC_BUFFER_LENGTH = 50
ELASTIC_TIMEOUT = 60
ELASTIC_UNIQ_KEY = "url"
ELASTIC_TYPE = "_doc"

# Elastic search Configuration#
ELASTIC_HOST = os.environ["ELASTIC_HOST"]
ELASTIC_USERNAME = os.environ["ELASTIC_USERNAME"]
ELASTIC_PASSWORD = os.environ["ELASTIC_PASSWORD"]
ELASTIC_INDEX = os.environ[
    "ELASTIC_INDEX"
]  # os.environ.get('ELASTIC_INDEX', 'dppa.st')
ELASTIC_INDEX_SITECONFIG = os.environ["ELASTIC_INDEX_XPATH"]
ELASTIC_INDEX_COUNTRY = os.environ["ELASTIC_INDEX_COUNTRIES"]

ELASTIC_MAPPINGS = {
    "settings": {
        "index": {
            "number_of_shards": 5,
            "number_of_replicas": 1,
            "refresh_interval": "1s",
            "mapping.total_fields.limit": 90000,
        }
    },
    "mappings": {
        "properties": {
            "posted_date": {
                "type": "date"
                # "format": "YYYY-MM-DD"
            },
            "indexed_date": {"type": "date", "format": "yyyy-MM-dd'T'HH:mm:ss"},
        }
    },
}

# user agent list
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
    "Mozilla/5.0 (Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
]

# languages
ARTICLES_LANGUAGE = {
    "aa": "Afar",
    "ab": "Abkhazian",
    "af": "Afrikaans",
    "ak": "Akan",
    "sq": "Albanian",
    "am": "Amharic",
    "ar": "Arabic",
    "an": "Aragonese",
    "hy": "Armenian",
    "as": "Assamese",
    "av": "Avaric",
    "ae": "Avestan",
    "ay": "Aymara",
    "az": "Azerbaijani",
    "ba": "Bashkir",
    "bm": "Bambara",
    "eu": "Basque",
    "be": "Belarusian",
    "bn": "Bengali",
    "bh": "Bihari languages",
    "bi": "Bislama",
    "bs": "Bosnian",
    "br": "Breton",
    "bg": "Bulgarian",
    "my": "Burmese",
    "ca": "Catalan; Valencian",
    "cs": "Czech",
    "ch": "Chamorro",
    "ce": "Chechen",
    "cu": "Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic",
    "cv": "Chuvash",
    "kw": "Cornish",
    "co": "Corsican",
    "cr": "Cree",
    "da": "Danish",
    "dv": "Divehi; Dhivehi;Maldivian",
    "dz": "Dzongkha",
    "el": "Greek: Modern 1453-",
    "en": "English",
    "eo": "Esperanto",
    "et": "Estonian",
    "ee": "Ewe",
    "fo": "Faroese",
    "fa": "Persian",
    "fj": "Fijian",
    "fi": "Finnish",
    "fr": "French",
    "fy": "Western Frisian",
    "ff": "Fulah",
    "Ga": "Georgian",
    "de": "German",
    "gd": "Gaelic; Scottish Gaelic",
    "ga": "Irish",
    "gl": "Galician",
    "gv": "Manx",
    "el": "Greek: Modern 1453-",
    "gn": "Guarani",
    "gu": "Gujarati",
    "ht": "Haitian; Haitian Creole",
    "ha": "Hausa",
    "he": "Hebrew",
    "hz": "Herero",
    "hi": "Hindi",
    "ho": "Hiri Motu",
    "hr": "Croatian",
    "hu": "Hungarian",
    "hy": "Armenian",
    "ig": "Igbo",
    "is": "Icelandic",
    "io": "Ido",
    "ii": "Sichuan Yi; Nuosu",
    "iu": "Inuktitut",
    "ie": "Interlingue; Occidental",
    "ia": "InterlinguaInternational Auxiliary Language Association",
    "id": "Indonesian",
    "ik": "Inupiaq",
    "is": "Icelandic",
    "it": "Italian",
    "jv": "Javanese",
    "ja": "Japanese",
    "kl": "Kalaallisut; Greenlandic",
    "kn": "Kannada",
    "ks": "Kashmiri",
    "ka": "Georgian",
    "kr": "Kanuri",
    "kk": "Kazakh",
    "km": "Central Khmer",
    "ki": "Kikuyu; Gikuyu",
    "rw": "Kinyarwanda",
    "ky": "Kirghiz; Kyrgyz",
    "kv": "Komi",
    "kg": "Kongo",
    "ko": "Korean",
    "kj": "Kuanyama; Kwanyama",
    "ku": "Kurdish",
    "lo": "Lao",
    "la": "Latin",
    "lv": "Latvian",
    "li": "Limburgan; Limburger;Limburgish",
    "ln": "Lingala",
    "lt": "Lithuanian",
    "lb": "Luxembourgish; Letzeburgesch",
    "lu": "Luba-Katanga",
    "lg": "Ganda",
    "mk": "Macedonian",
    "mh": "Marshallese",
    "ml": "Malayalam",
    "mi": "Maori",
    "mr": "Marathi",
    "ms": "Malay",
    "Mi": "Micmac",
    "mk": "Macedonian",
    "mg": "Malagasy",
    "mt": "Maltese",
    "mn": "Mongolian",
    "my": "Burmese",
    "na": "Nauru",
    "nv": "Navajo; Navaho",
    "nr": "Ndebele: South; South Ndebele",
    "nd": "Ndebele: North; North Ndebele",
    "ng": "Ndonga",
    "ne": "Nepali",
    "nl": "Dutch; Flemish",
    "nn": "Norwegian Nynorsk; Nynorsk: Norwegian",
    "nb": "Bokmål: Norwegian; Norwegian Bokmål",
    "no": "Norwegian",
    "oc": "Occitanpost 1500",
    "oj": "Ojibwa",
    "or": "Oriya",
    "om": "Oromo",
    "os": "Ossetian; Ossetic",
    "pa": "Panjabi; Punjabi",
    "pi": "Pali",
    "pl": "Polish",
    "pt": "Portuguese",
    "ps": "Pushto; Pashto",
    "qu": "Quechua",
    "rm": "Romansh",
    "ro": "Romanian; Moldavian;Moldovan",
    "rn": "Rundi",
    "ru": "Russian",
    "sg": "Sango",
    "sa": "Sanskrit",
    "si": "Sinhala;Sinhalese",
    "sk": "Slovak",
    "sl": "Slovenian",
    "se": "Northern Sami",
    "sm": "Samoan",
    "sn": "Shona",
    "sd": "Sindhi",
    "so": "Somali",
    "st": "Sotho: Southern",
    "es": "Spanish; Castilian",
    "sq": "Albanian",
    "sc": "Sardinian",
    "sr": "Serbian",
    "ss": "Swati",
    "su": "Sundanese",
    "sw": "Swahili",
    "sv": "Swedish",
    "ty": "Tahitian",
    "ta": "Tamil",
    "html": "Tatar",
    "te": "Telugu",
    "tg": "Tajik",
    "tl": "Tagalog",
    "th": "Thai",
    "bo": "Tibetan",
    "ti": "Tigrinya",
    "to": "Tonga Tonga Islands",
    "tn": "Tswana",
    "ts": "Tsonga",
    "tk": "Turkmen",
    "tr": "Turkish",
    "tw": "Twi",
    "ug": "Uighur; Uyghur",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "uz": "Uzbek",
    "ve": "Venda",
    "vi": "Vietnamese",
    "vo": "Volapük",
    "cy": "Welsh",
    "wa": "Walloon",
    "wo": "Wolof",
    "xh": "Xhosa",
    "yi": "Yiddish",
    "yo": "Yoruba",
    "za": "Zhuang; Chuang",
    "zh": "Chinese",
    "zu": "Zulu",
}

reg_exp_1 = (
    r"(?:\d{1,2} (?:january|february|march|april|may|june|july|august|september|october|november|december) \d{2,4})|(?:\d{1,2} "
    r"(?:jan|feb|march|april|may|june|july|august|sept|oct|nov|dec) \d{2,4})|(?:(?:january|february|march|april|may|june|july|"
    r"august|september|october|november|december)[,]? \d{1,2} \d{2,4})|"
    r"(?:(?:jan|feb|march|april|may|june|july|august|sept|oct|nov|dec)[,]? \d{1,2} \d{2,4})"
)

reg_exp_1 = (
    "[0-9]{2}/[0-9]{2}/[0-9]{4}|[0-9]{2}.[0-9]{2}.[0-9]{4}|[0-9]{2}/[0-9]{2}/[0-9]{2}|[0-9]{1}/[0-9]{2}/[0-9]{2}|[0-9]{2}-[0-9]{2}-"
    "[0-9]{2}|[0-9]{4}.[0-9]{1}.[0-9]{1}|[0-9]{2}.[0-9]{1}.[0-9]{4}|[0-9]{4}.[0-9]{1}.[0-9]{1}|[0-9]{4}.[0-9]{2}.[0-9]{2}|[0-9]{1}."
    "[0-9]{1}.[0-9]{4}|[0-9]{1}.[0-9]{2}.[0-9]{4}|[0-9]{2}.[0-9]{2}.[0-9]{2}|[0-9]{2}.[0-9]{1}.[0-9]{2}|"
    r"(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2},"
    r" \d{4}|(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday), \d{1,2}th (?:January|February|March|April|May|"
    r"June|July|August|September|October|November|December) "
    r"\d{4}|(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday), \d{1,2}. (?:January|February|March|April|May|"
    r"June|July|August|September|October|November|December) \d{4}|\d{1,2} "
    r"(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}|(?:Jan|Feb|Mar|"
    r"April|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2}, \d{4}|\d{1,2}th "
    r"(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}|(?:January|"
    r"February|March|April|May|June|July|August|September|October|November|December) \d{1,2} \d{4}"
)
