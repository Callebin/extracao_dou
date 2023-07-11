import re


class HighlightGenerator:
    def __init__(self):
        self.alvo = [
            "designar",
            "dispensar",
            "instaurar",
            "ceder",
            "requisitar",
            "declarar",
            "conceder",
            "nomear",
            "indicar",
            "reintegrar",
            "autorizar",
            "prorrogar",
            "reconduzir",
            "subdelegar",
            "autoriza",
            "retificação",
            "cessar",
            "exonerar",
            "extrato de acordo de cooperação não oneroso",
            "extrato de termo aditivo",
            "extrato de extinção",
            "instituir",
        ]
        self.target = [
            "cgu",
            "controladoria geral da união",
            "controladoria-geral da união",
            "controladoria-geral da uniao",
            "controladoria geral da uniao",
        ]

    @staticmethod
    def extract_special_words(text):
        special_words = []
        for word in text.split():
            if re.search(r"[a-zA-Z]+(ar|er|ir|or|ur)\b", word):
                special_words.append(word)
        return special_words

    def prioritize_string(self, text):
        monitorado = text.replace(",", "").replace(":", " ").lower()
        tratado = text.replace(",", "").replace(":", " ")
        resposta = []
        for r in self.alvo:
            if r in monitorado:
                index = monitorado.index(r)
                response = (
                    tratado[index : index + 200]
                    if len(tratado) < 200
                    else tratado[index : index + 200] + "..."
                )
                resposta.append(response)
                break
        else:
            resposta.append(tratado[:200] + "...")
        return resposta[0]

    def prioritize_external(self, text):
        monitorado = text.replace(",", "").replace(":", " ").lower()
        tratado = text.replace(",", "").replace(":", " ")
        resposta = []
        for r in self.alvo:
            if r in monitorado:
                index = monitorado.index(r)
                response = tratado[index : index + 85]
                resposta.append(response)
                for t in self.target:
                    if t in monitorado:
                        index_target = monitorado.index(t)
                        start_index = index_target - max(
                            (index_target - (index_target - 80)), 0
                        )
                        end_index = index_target + 80
                        resposta.append(tratado[start_index:end_index] + "...")
                        break
                break
        else:
            c = 0
            for t in self.target:
                if t in monitorado and c == 0:
                    index = monitorado.index(t)
                    if monitorado[index : index + 7] == "cgu/agu":
                        break
                    start_index = index - max((index - (index - 150)), 0)
                    end_index = index + 150
                    resposta.append("..." + tratado[start_index:end_index] + "...")
                    c += 1
        if len(resposta) > 1:
            return "...".join(resposta)
        elif len(resposta) != 0:
            return resposta[0]


if __name__ == "__main__":
    external = """O CHEFE SUBSTITUTO DO SERVIÇO DE GESTÃO DE PESSOAS DA
    SUPERINTENDÊNCIA ESTADUAL DO MINISTÉRIO DA SAÚDE NO MARANHÃO, no uso das
    atribuições que lhe foram conferidas pela PT/SAA/SE/MS 1.804, de 01/10/2013, publicada
    no DOU 192, de 03.10.2013 e PT/SAA/MS Nº 52, de 23.01.2023, publicada no DOU 17, de
    24.01.2023, resolve:
    Tornar sem efeito, a partir de 30/06/2023, a Portaria SEGAD/MA Nº 135, DE 22
    DE ABRIL DE 2020, pub. no DOU nº 82 de 30/04/2020, que concedeu aposentadoria a
    servidora WALMIRA PORTELA COELHO, matrículas 1029502, SIAPE nº 551943, ocupante do
    cargo de Agente Administrativo, com fundamento nas Notas Técnicas nº
    3280/2022/CGUNE/CRG e nº 637/2021/CGUNE/CRG, tendo em vista acumulo indevido
    cargos públicos. (Processo nº 25014.000648/2023-52)."""

    res = HighlightGenerator()

    print(res.prioritize_external(external))
