# -*- coding: utf-8 -*-
import csv

#prepise mezivysledek scrapovani tak, ze kazdy vysledek je na jednom radku
final=[]
with open('vysledky_soutezi.csv', newline='') as icsvfile, open('vysledky_soutezi_konecne_otec.csv', 'w') as ocsvfile:
	reader = csv.reader(icsvfile)
	writer = csv.writer(ocsvfile, lineterminator='\n\n', delimiter=" ")
	icsvfile.readline() 
	for row in reader:
		if row[0][:3] == "<b>":
			listik = [row[0]]+row[1].split(",")
		else:
			listik = [row[1]]+row[0].split(",")
		listik=[[i] for i in listik]
		for i in listik:
			writer.writerow(i)