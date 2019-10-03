# -*- coding: utf-8 -*-
import scrapy
from scraping_kolo_vysledky.items import ScrapingStodulkyItem
from scrapy.loader import ItemLoader
import sys
import string


class ScrapeTymSpider(scrapy.Spider):
    name = 'vysledky'
    allowed_domains = ['www.fotbalpraha.cz']
    #vždy se jen přičte o jedno číslo více na konci url - znaci kolo
    start_urls = [  "https://www.fotbalpraha.cz/souteze/zapasy/153-a2b-1-a-trida-skupina-b-muzu?id_season=2019&id_round=8",
                    "https://www.fotbalpraha.cz/souteze/zapasy/154-a3a-1-b-trida-skupina-a-muzu?id_season=2019&id_round=8",
                    "https://www.fotbalpraha.cz/souteze/zapasy/158-a4c-2-trida-skupina-c-muzu?id_season=2019&id_round=6",
                    "https://www.fotbalpraha.cz/souteze/zapasy/162-c2a-1-trida-starsiho-dorostu?id_season=2019&id_round=6",
                    "https://www.fotbalpraha.cz/souteze/zapasy/165-d4a-2-trida-mladsiho-dorostu?id_season=2019&id_round=4",
                    "https://www.fotbalpraha.cz/souteze/zapasy/168-e2b-1-trida-skupina-b-starsich-zaku?id_season=2019&id_round=5",
                    "https://www.fotbalpraha.cz/souteze/zapasy/171-f1a-prebor-mladsich-zaku?id_season=2019&id_round=4",
                    "https://www.fotbalpraha.cz/souteze/zapasy/173-f2b-1-trida-skupina-b-mladsich-zaku?id_season=2019&id_round=4",
                    "https://www.fotbalpraha.cz/souteze/zapasy/174-f3a-2-trida-skupina-a-mladsich-zaku?id_season=2019&id_round=4"
                    ]

    # Muži A - 1.A třída - skupina B, Muži B - 1.B třída - skupina A, Muži C, 2. třída - skupina C, Starší dorost - Přebor Prahy, Starší žáci, 1. třída - skupina B, Mladší žáci A - Pražský přebor, Mladší žáci B - 1. třída - skupina B, Mladší žáci C - 2. třída - skupina A

    def parse(self, response):
            souperi=[]
            konecny=[]
            konecnik={}
            tyms=["Muži A - 1.A třída - skupina B", "Muži B - 1.B třída - skupina A", "Muži C, 2. třída - skupina C", "Starší dorost - 1. třída staršího dorostu ", "Mladší dorost - 2. třída mladšího dorostu","Starší žáci, 1. třída - skupina B", "Mladší žáci A - Pražský přebor", "Mladší žáci B - 1. třída - skupina B", "Mladší žáci C - 2. třída - skupina A"]
            tymy_nazvy_na_webu=["A2B", "A3A", "A4C", "C2A","D4A", "E2B","F1A","F2B","F3A"]
            k=2
            x=0
            soutez=response.xpath('//div[contains(@class, "filter__item")]//h1/text()').extract()[0]
            date=response.xpath('//td[contains(@class, "date")]/text()').extract() 
            soup=response.xpath('//span[contains(@class, "middle")]/text()').extract()
            sledek=response.xpath('//div[contains(@class, "table-responsive")]//td[contains(@class, "score")]//a/text()').extract()
            docas = soutez[0:3]
            if docas in tymy_nazvy_na_webu:
                x = tymy_nazvy_na_webu.index(docas)

            tym_finalni=tyms[x]
            #vytvoreni seznamu souperu po dvojicich
            souperi.append(soup[0]+" - "+soup[1])
            for i in range(1,len(soup)-1):
                if (i*2)<=len(soup)-1:
                    s=soup[i*2]+" - "+soup[i+k]
                    souperi.append(s)
                    s=""
                    k+=1

            #loading do items
            l=ItemLoader(item=ScrapingStodulkyItem(), response=response)
            l.add_value("souperi", souperi)
            l.add_value("vysledek", sledek)

            
            #sceluje soupere a vysledky a ocistuje vysledky od whitespace skrze itemps.py
            for i in range(len(l.get_output_value("souperi"))):
                if i<len(l.get_output_value("souperi"))-1:
                    s=l.get_output_value("souperi")[i]+" "+l.get_output_value("vysledek")[i]+"<br>"
                    konecny.append(s)
                else:
                    s=l.get_output_value("souperi")[i]+" "+l.get_output_value("vysledek")[i]+"<br><br>"
                    konecny.append(s)
            #konecny="\n".join(konecny)
            konecnik["tym"]="<b>"+tym_finalni+"</b><br>"
            konecnik["výsledky_kola"]=konecny
            
            #vystup
            return konecnik
