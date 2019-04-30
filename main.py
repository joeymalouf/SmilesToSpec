import re
from lxml import html
from bs4 import BeautifulSoup
import requests
import csv


norine_search_data_request = requests.post(url="https://bioinfo.lifl.fr/norine/fingerPrintSearch.jsp?nrps1=Ac-Phe%2CCys%2CPro%2CIle%2CVal%2CIst%401%2C2%400%400%2C5%404%405%2C3%402%2C4")
norine_search_data_request = norine_search_data_request.content

norine_search_data_soup = BeautifulSoup(norine_search_data_request, 'html.parser')
norine_search_links = [link['href'] for link in norine_search_data_soup.find_all("a", {'href': re.compile('.*ID=NOR.*')})]
norine_search_codes = [re.search('ID=NOR(.*)', link)[1] for link in norine_search_links]
norine_csv_form_data = []

for code in norine_search_codes:
    norine_csv_form_data.append(('choix', code))
norine_csv_request = requests.post(url="https://bioinfo.lifl.fr/norine/norineText.csv?peptide=id_peptide&peptide=name&peptide=family&peptide=syno&peptide=activity&peptide=category&peptide=formula&peptide=mw&peptide=comment&peptide=statut&structure=type&structure=mono&structure=pdb&structure=graph&orga=name_orga&orga=taxo&orga=gram&orga=syno&orga=taxid&link=acc&link=name_db", data=norine_csv_form_data)

norine_csv_text = norine_csv_request.text
norine_csv_text = re.search('acc;\s\s((\s|.)*)',norine_csv_text)[1]
potential_matches_csv = open('test.csv', 'w', encoding='ISO-8859-1')
potential_matches_csv.write(norine_csv_text)
potential_matches_csv.close()

csv.register_dialect('semicolon', delimiter = ';')
test = open('test.csv', 'r')
reader = csv.reader(test, dialect='semicolon')

for row in reader:
    print(row)