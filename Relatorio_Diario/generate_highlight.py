import re

alvo = [
'designar',
'dispensar',
'instaurar',
'ceder',
'requisitar',
'declarar',
'conceder',
'nomear',
'indicar',
'reintegrar',
'autorizar',
'prorrogar',
'reconduzir',
'subdelegar',
'autoriza', 
'retificação',
'cessar',
'exonerar', 
'extrato de acordo de cooperação não oneroso',
'extrato de termo aditivo',
'extrato de extinção',
'instituir'
]

target = ['cgu','controladoria geral da união', 'controladoria-geral da união', 'controladoria-geral da uniao',
          'controladoria geral da uniao']

def extract_special_words(text):
    special_words = []
    for word in text.split():
        if re.search(r"[a-zA-Z]+(ar|er|ir|or|ur)\b", word):
            special_words.append(word)
    return special_words

def prioritize_string(text):
    monitorado = text.replace(',','').replace(':',' ').lower()
    tratado = text.replace(',','').replace(':',' ')
    resposta = []
    for r in alvo:
        if r in monitorado:
            index = monitorado.index(r)
            response = tratado[index:index + 200]
            if len(tratado) < 200:
                resposta.append(response)
                break
            else:
                resposta.append(response + '...')
                break
    else:
        resposta.append(tratado[:200] + '...') 
    return resposta[0]


def prioritize_external(text):
    monitorado = text.replace(',','').replace(':',' ').lower()
    tratado = text.replace(',','').replace(':',' ')
    resposta = []
    for r in alvo:
        if r in monitorado:
            index = monitorado.index(r)
            response = tratado[index:index + 85]
            resposta.append(response)
            for t in target:
                if t in monitorado:
                    index_target = monitorado.index(t)
                    resposta.append(tratado[index_target - max((index_target - (index_target - 80)), 0):index_target + 80] + '...')
                    break
            break
                
    else:
        c = 0
        for t in target:
            if t in monitorado and c == 0:
                index = monitorado.index(t)
                if monitorado[index:index + 7] == 'cgu/agu':
                    break
                resposta.append('...' + tratado[index - max((index - (index-150)), 0):index +150] + '...')
                c += 1
    if len(resposta) > 1:   
        return '...'.join(resposta)
    elif len(resposta) != 0:
        return resposta[0]
    

# apa =prioritize_external(' MINISTRA DE ESTADO DA SAÚDE, no uso de suas atribuições legais e considerando o disposto no artigo 93 da Lei nº 8.112, de 11 de dezembro de 1990, Decreto nº 10.835 de 14 de outubro de 2021, alterado pelo Decreto nº 11.306 de 22 de dezembro de 2022 e ainda pela Lei artigo nº Art. 16-B. da Lei nº 11.356, de 19 de outubro de 2006 e demais informações que constam no NUP 00190.101306/2023-97, resolve: Art. 1º Cedr a servidora RAFAELLA DA COSTA SANTIN DE ANDRADE, matrícula no SIAPE nº 2040286, ocupante do cargo efetivo Analista Técnico de Políticas Sociais (ATPS), Classe "B", Padrão II, do Quadro de Pessoal do Ministério da Saúde, para percepção da Gratificação Temporária das Unidades dos Sistemas Estruturadores da Administração Pública Federal-GSISTE, Nível Superior, na Controladoria-Geral da União (CGU). Art. 2º O ônus pela remuneração é do órgão cedente. Art. 3º A servidora deverá apresentar-se imediatamente ao órgão cedente, ao término da cessão, observando o disposto no artigo 8º do Decreto nº 10.835, de 14 de outubro de 2021. Art. 4º Torna-se sem efeito o disposto nesta Portaria caso a servidora não se apresente ao órgão cessionário no prazo de 30 (trinta) dias. Art. 5º Esta Portaria entra em vigor na data de sua publicação.')
# print(apa)