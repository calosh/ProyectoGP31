from django.test import TestCase

# Create your tests here.



import re


def eliminar_urls(text):
    text = text.replace("https"," https")
    url_patron = re.compile("(?P<url>https?://[^\s]+)")

    text = re.sub(url_patron, '', text)

    return text


url_patron = re.compile("pic.twitter.com/[^0-9a-z]")


text =  re.sub(r'\b(?:(a|e|i|o|u)*(?:ja|je|ji|jo|ju)+j?|(?:j+(a|e|i|o|u)+)+j+)\b','jaja',text, flags=re.I)



print text