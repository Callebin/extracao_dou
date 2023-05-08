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
                    resposta.append(tratado[index_target - max(index-10,0):index_target + 80] + '...')
                    break
            break
                
    else:
        for t in target:
            if t in monitorado:
                index = text.index(t)
                resposta.append('...' + tratado[index - max(index-20, 0):index +300] + '...')
    if len(resposta) > 1:   
        return '...'.join(resposta)
    else:
        return resposta[0]
    

apa =prioritize_external('eu quero que seja oq seja doce nessa porra e DESIGNAR ambém quero o senhor para que possa, com muito orgulho, e com muita dedicação, auxiliar a CGU nessa empreitada de melhorar o serviço públixo a e também quero o senhsa empreitada de melhorar o serviço públixo a e ')
print(apa)