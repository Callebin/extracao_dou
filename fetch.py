# Here is the optimized and organized code

# Import necessary modules
import os
import xml.etree.ElementTree as ET
import csv
from baixa_pdf import download_pdf  # Assuming this is a local module


# Define constants

DIRECTORY = "C:\\Users\\gab36\\OneDrive\\Documentos\\Development\\FetchDOU\\DOUS\\2023-04-11-DO2\\529_20230320_20432158.xml"
DOU = "C:\\Users\\gab36\\OneDrive\\Documentos\\Development\\FetchDOU\\DOUS\\2023-08-01-DO2"
URL_PAD_PDF = "https://pesquisa.in.gov.br/imprensa/jsp/visualiza/index.jsp?"

KEYWORDS = {
    "Vacância": ["Declarar vago", "posse", "vacância"],
    "Designação/Dispensa": ["DESIGNAR", "DISPENSAR", "SUBSTITUIR"],
}

DESIG = ["DESIGNAR", "DESIGNAR,", "Designar", "DISPENSAR", "Dispensar", "Dispensar,", "SUBSTITUIR", "Substituir", "NOMEAR", "Nomear"]
COMISSAO = ["COMISSÃO", "Comissão", "comissão", "COMISSAO", "Comissao", "comissao", "SINDICÂNCIA", "Sindicância", "SINDICANCIA", "Sindicancia", "sindicancia", "sindicância"]
COD_FUNCAO = ["FCE", "CCE", "FG", "FCT", "DAS", "FCPE"]
FICANDO = ["Ficando dispensado", "ficando dispensado", "Ficando dispensada", "ficando dispensada"]

def check_desig(text):
    """
    Verifica se existe designação na portaria.
    Pega os dados do Código da Funcção e também se há dispensa.
    Passa os resultados para um dicionário.
    """
    words = text.split()
    result = {}
    c = f = 0
    for word in words:
        if word in DESIG and all(forbidden not in words for forbidden in COMISSAO):
            index = text.find(word)
            result[word] = text[index + len(word): text.find(",", index)].strip()
            for cod in COD_FUNCAO:
                if cod in text:
                    indexcod = text.find(cod)
                    codigo = cod + text[indexcod + len(cod): indexcod + len(cod) + 5]
                    result["Código"] = codigo
                    c += 1
                elif c == 0:
                    result["Código"] = "Não encontrado!"
            for dis in FICANDO:
                if dis in text:
                    result["Ficando Dispensado"] = True
                    f += 1
                elif f == 0:
                    result["Ficando Dispensado"] = False
            return result
    return None


def monta_url(url):
    """
    Conserta o formato da URL passado pelo arquivo XML;
    O formato passado não é compatível.
    """
    def pega_pagina(string):
        last_equals_index = string.rfind("=")
        if last_equals_index == -1:
            return None
        return string[last_equals_index + 1:]

    data_index = url.find("data=")
    data_url = url[data_index + 5 : data_index + 15] if data_index != -1 else None
    jornal_index = url.find("jornal=")
    jornal_url = url[jornal_index + 7 : jornal_index + 10] if jornal_index != -1 else None
    pagina = f"pagina={pega_pagina(url)}"
    url_comp = f"{URL_PAD_PDF}{jornal_url}&{pagina}&{data_url}"

    return url_comp


def puxa_dados(arq):
    """
    Pulls data from a given XML file.
    """
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
                end = escopo.find("Controladoria-Geral da União") + len("Controladoria-Geral da União")
                # download_pdf(pdf, nome_arquivo, escopo[start:end])
                writer.writerow({
                    "Escopo": portaria,
                    "Orgao": org,
                    "Destaque": destaque,
                    "File": pdf,
                })


if __name__ == '__main__':

    with open("result.csv", "a", newline="") as f:
        headers = ["Escopo", "Orgao", "Destaque", "File"]
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

        for file in os.listdir(DOU):
            current = os.open((os.path.join(DOU, file)), os.O_RDONLY)
            puxa_dados(current)