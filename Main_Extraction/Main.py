import xml.etree.ElementTree as ET
import os
from unidecode import unidecode
import re

directory = 'C:\\Users\\gab36\\OneDrive\\Documentos\\Development\\FetchDOU\\DOUS\\2023-04-11-DO2\\529_20230320_20432158.xml'
dou = 'C:\\Users\\gab36\\OneDrive\\Documentos\\Development\\FetchDOU\\DOUS\\2023-05-02-DO2'
url_pad_pdf = 'https://pesquisa.in.gov.br/imprensa/jsp/visualiza/index.jsp?'
          
target = ['cgu','controladoria geral da união', 'controladoria-geral da união', 'controladoria-geral da uniao',
          'controladoria-geral da uniao']

def monta_url(url):
    data_index = url.find('data=')
    if data_index != -1:
        data_url = url[data_index+5:data_index+15]
        data = f'data={data_url}'
    jornal_index = url.find('jornal=')
    if jornal_index != -1:
        jornal_url = url[jornal_index+7:jornal_index+10]
        jornal = f'jornal={jornal_url}'
    def pega_pagina(string):
        last_equals_index = string.rfind('=')
        if last_equals_index == -1:
            return None
        return string[last_equals_index + 1:]
    pagina = f'pagina={pega_pagina(url)}'
    url_comp = url_pad_pdf + jornal + '&' + pagina + '&' + data
    return url_comp


def puxa_dados(arq):
    tree = ET.parse(arq)
    root = tree.getroot()

    for child in root:
        monitorado = unidecode(child[0][5].text).lower()
        tratado = re.sub(r'<[/]?p[^>]*>', '', child[0][5].text)
        tratado = re.sub(r'<p[^>]*>.*?</p>', '', tratado)
        org = root.find('./article').attrib['artCategory']
        for k in target:
            if k in monitorado:
                portaria = (child[0][0].text)
                pdf = monta_url(root.find('./article').attrib['pdfPage'])
                print(tratado, 'END', portaria, 'END',pdf, 'END', org)
            else:
                continue

    
for file in os.listdir(dou):
    current = os.open((os.path.join(dou, file)), os.O_RDONLY)
    puxa_dados(current)



