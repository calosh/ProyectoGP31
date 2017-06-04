import re


def eliminar_urls(text):
    text = text.replace("https"," https")
    text = text.replace("pic.twitter.com", " https://pic.twitter.com")
    url_patron = re.compile("(?P<url>https?://[^\s]+)")
    text = re.sub(url_patron, '', text)

    return text