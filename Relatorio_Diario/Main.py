import xml.etree.ElementTree as ET
import os
from unidecode import unidecode
import re
from generate_highlight import HighlightGenerator
import generate_pdf
from datetime import date

class DOUParser:
    def __init__(self, dou_directory):
        self.dou_directory = dou_directory
        self.target = [
            "cgu",
            "controladoria geral da união",
            "controladoria-geral da união",
            "controladoria-geral da uniao",
        ]
        self.objeto = []
        self.high = HighlightGenerator()

    @staticmethod
    def monta_url(url):
        def pega_pagina(string):
            last_equals_index = string.rfind("=")
            if last_equals_index == -1:
                return None
            return string[last_equals_index + 1 :]

        data_index = url.find("data=")
        data = f"data={url[data_index + 5:data_index + 15]}" if data_index != -1 else ""
        jornal_index = url.find("jornal=")
        jornal = (
            f"jornal={url[jornal_index + 7:jornal_index + 10]}"
            if jornal_index != -1
            else ""
        )
        pagina = f"pagina={pega_pagina(url)}"
        url_comp = (
            "https://pesquisa.in.gov.br/imprensa/jsp/visualiza/index.jsp?"
            + jornal
            + "&"
            + pagina
            + "&"
            + data
        )
        return url_comp

    @staticmethod
    def limpa_portaria(portaria):
        tratado = re.sub(r"<[/]?p[^>]*>", "", portaria)
        tratado = re.sub(r"<p[^>]*>.*?</p>", "", tratado)
        ocorrencias = re.findall(r"2023*", tratado)
        if portaria[:8].lower() == "portaria":
            index = tratado.index(ocorrencias[0]) + 4
            tratado = tratado[index:]
        return tratado

    def parse_xml(self, xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for child in root:
            monitorado = unidecode(child[0][5].text).lower()
            tratado = self.limpa_portaria(child[0][5].text)
            org = root.find("./article").attrib["artCategory"]
            for k in self.target:
                if k in monitorado:
                    portaria = child[0][0].text
                    link = self.monta_url(root.find("./article").attrib["pdfPage"])
                    if "Controladoria-Geral da União" in org:
                        destaque = self.high.prioritize_string(tratado)
                    else:
                        destaque = self.high.prioritize_external(tratado)

                        if destaque is None:
                            break
                    self.objeto.append([portaria, org, destaque, link])
                    break

    def generate_pdf(self):
        pdf = generate_pdf.Gerador()

        hj = date.today()
        hj_format = hj.strftime("%d-%m-%Y")
        output_file = os.path.join(os.getcwd(), f'Relatório DOU {hj_format}.pdf')

        for portaria, org, destaque, link in self.objeto:
            pdf.add_port(portaria, org, destaque, link)

        pdf.output(output_file, "F")

    def process_directory(self):
        for d in os.listdir(self.dou_directory):
            for xml in os.listdir(os.path.join(self.dou_directory, d)):
                filename, file_extension = os.path.splitext(xml)
                if file_extension != ".xml":
                    continue
                current = os.path.join(self.dou_directory, d, xml)
                self.parse_xml(current)


if __name__ == "__main__":
    dou_directory = (
        "C:\\Users\\gab36\\OneDrive\\Documentos\\Development\\FetchDOU\\DOUS\\"
    )
    parser = DOUParser(dou_directory)
    parser.process_directory()
    parser.generate_pdf()

