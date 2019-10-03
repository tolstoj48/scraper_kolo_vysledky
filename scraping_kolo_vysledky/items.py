# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field
from scrapy.loader.processors import Compose, MapCompose
from w3lib.html import remove_tags


#cisti whitespace
clean_text=Compose(MapCompose(lambda v: v.strip()))

def normalize_space(value):
    return " ".join(value.split())


class ScrapingStodulkyItem(Item):
    souperi=Field()
    vysledek=Field(output_processor=clean_text)

class ScrapingTabulkyTymy(Item):
	poradi_tymu=Field(output_processor=clean_text)
	tym=Field(output_processor=clean_text, input_processor=MapCompose(remove_tags,normalize_space))
	pocet_utkani=Field(output_processor=clean_text)
	pocet_vitezstvi=Field(output_processor=clean_text)
	pocet_remiz=Field(output_processor=clean_text)
	pocet_proher=Field(output_processor=clean_text)
	body=Field(output_processor=clean_text)
	skore=Field(output_processor=clean_text)
	kolo=Field(output_processor=clean_text)






