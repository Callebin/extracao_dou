import xml.etree.ElementTree as ET
import os

import csv
from baixa_pdf import download_pdf

directory = "C:\\Users\\gab36\\OneDrive\\Documentos\\Development\\FetchDOU\\DOUS\\2023-04-11-DO2\\529_20230320_20432158.xml"
dou = "C:\\Users\\gab36\\OneDrive\\Documentos\\Development\\FetchDOU\\DOUS\\2023-07-11-DO2"
url_pad_pdf = "https://pesquisa.in.gov.br/imprensa/jsp/visualiza/index.jsp?"


referencia = {
    "Vacância": ["Declarar vago", "posse", "vacância"],
    "Designação/Dispensa": ["DESIGNAR", "DISPENSAR", "SUBSTITUIR"],
}
desig = [
    "DESIGNAR",
    "DESIGNAR,",
    "Designar",
    "DISPENSAR",
    "Dispensar",
    "Dispensar,",
    "SUBSTITUIR",
    "Substituir",
    "NOMEAR",
    "Nomear",
]
comissao = [
    "COMISSÃO",
    "Comissão",
    "comissão",
    "COMISSAO",
    "Comissao",
    "comissao",
    "SINDICÂNCIA",
    "Sindicância",
    "SINDICANCIA",
    "Sindicancia",
    "sindicancia",
    "sindicância",
]
cod_funcao = ["FCE", "CCE", "FG", "FCT", "DAS", "FCPE"]
ficando = [
    "Ficando dispensado",
    "ficando dispensado",
    "Ficando dispensada",
    "ficando dispensada",
]


def check_desig(text):
    words = text.split()
    result = {}
    c = 0
    f = 0
    for word in words:
        if word in desig and all(forbidden not in words for forbidden in comissao):
            index = text.find(word)
            result[word] = text[index + len(word) : text.find(",", index)].strip()
            for cod in cod_funcao:
                if cod in text:
                    indexcod = text.find(cod)
                    codigo = cod + text[indexcod + len(cod) : indexcod + len(cod) + 5]
                    result["Código"] = codigo
                    c += 1
                elif c == 0:
                    result["Código"] = "Não encontrado!"
            for dis in ficando:
                if dis in text:
                    result["Ficando Dispensado"] = True
                    f += 1
                elif f == 0:
                    result["Ficando Dispensado"] = False
            return result
    return None


def monta_url(url):
    data_index = url.find("data=")
    if data_index != -1:
        data_url = url[data_index + 5 : data_index + 15]
        data = f"data={data_url}"
    jornal_index = url.find("jornal=")
    if jornal_index != -1:
        jornal_url = url[jornal_index + 7 : jornal_index + 10]
        jornal = f"jornal={jornal_url}"

    def pega_pagina(string):
        last_equals_index = string.rfind("=")
        if last_equals_index == -1:
            return None
        return string[last_equals_index + 1 :]

    pagina = f"pagina={pega_pagina(url)}"
    url_comp = url_pad_pdf + jornal + "&" + pagina + "&" + data
    return url_comp


def puxa_dados(arq):
    tree = ET.parse(arq)
    root = tree.getroot()

    for child in root:
        org = root.find("./article").attrib["artCategory"]
        if "Controladoria-Geral da União" in org:
            portaria = child[0][0].text
            escopo = (child[0][5].text).replace("</p><p>", " ")
            pdf = monta_url(root.find("./article").attrib["pdfPage"])
            destaque = check_desig(escopo)
            if destaque:
                print(destaque)

                nome_arquivo = list(destaque.values())[0]
                start = escopo.find(list(destaque.keys())[0])
                end = escopo.find("Controladoria-Geral da União") + len(
                    "Controladoria-Geral da União"
                )
                # download_pdf(pdf, nome_arquivo, escopo[start:end])
                writer.writerow(
                    {
                        "Escopo": portaria,
                        "Orgao": org,
                        "Destaque": destaque,
                        "File": pdf,
                    }
                )
        else:
            continue


with open("result.csv", "a", newline="") as f:
    headers = ["Escopo", "Orgao", "Destaque", "File"]
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()

    for file in os.listdir(dou):
        current = os.open((os.path.join(dou, file)), os.O_RDONLY)
        puxa_dados(current)


## PRÓXIMAAA:
# Datas designações
# Presidência
# Tornar sem efeito
# Retificar
# Edição Extra
# Exoneração e Vacância
# Afastamentos
# PAD
