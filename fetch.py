import xml.etree.ElementTree as ET
import os
import csv


directory = 'C:\\Users\\gab36\\OneDrive\\Documentos\\Development\\FetchDOU\\DOUS\\2023-03-20-DO2\\529_20230320_20432158.xml'
dou = 'C:\\Users\\gab36\\OneDrive\\Documentos\\Development\\FetchDOU\\DOUS\\2023-03-20-DO2'
url_pad_pdf = 'https://pesquisa.in.gov.br/imprensa/jsp/visualiza/index.jsp?'

keywords = [
    'CONCEDER',
    'DISPENSAR',
    'DESIGNAR',
    'APLICAR',
    'REVERTER',
    'SUBSTITUIR',
    'CONVALIDADOS',
    'PARTIR',
    'DURANTE',
    'TORNAR',
    'CEDER',
    'CONVALIDADOS',
    'FICANDO',
    'TORNANDO',
    'REMOVER',
    'PRORROGAR',
    'RECONDUZIR',
    'INSTITUIR'
]


inf = ['ar', 'AR', 'er', 'ER', 'ir', 'IR', 'or', 'OR', 'ur', 'UR']

def check_upper(text):

    upper_words = []
    target = []
    current_word = ""

    infvar = ['ar', 'AR', 'er', 'ER', 'ir', 'IR', 'or', 'OR', 'ur', 'UR']

    for word in text.split():
        if word.isupper():
            if word[-2:] in infvar:
                target.append(word)
                continue
            else:
                current_word += word + ' '      
        else:
            if current_word != "":
                upper_words.append(current_word)
                current_word = ""
    if current_word != "":
        upper_words.append(current_word)

def palavra_destaque(texto):
    tar = []
    for word in texto.split():
        strin = str(word).upper()
        if strin in keywords:
            print(word)
            tar.append(strin)
        elif '</p><p>' in word:
            word.replace('</p><p>', ' ')
        else:
            continue
    # print(tar)
    return tar

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

        org = root.find('./article').attrib['artCategory']
        
        if 'Controladoria-Geral da União' in org:
            portaria = (child[0][0].text)
            preescopo = (child[0][5].text)
            escopo = preescopo.replace('</p><p>', ' ')
            pdf = monta_url(root.find('./article').attrib['pdfPage'])
            destaque = palavra_destaque(escopo)
            # ET.dump(tree)
            writer.writerow({'Portaria': portaria, 'Orgao': org, 'Destaque': destaque, 'File': file})
        else:
            continue
        

    
with open('result.csv', 'a', newline='') as f:

    headers = ['Portaria', 'Orgao', 'Destaque', 'File']
    writer = csv.DictWriter(f, fieldnames=headers)

    for file in os.listdir(dou):
        current = os.open((os.path.join(dou, file)), os.O_RDONLY)
        puxa_dados(current)

        

