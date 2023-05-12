import re

def extract_special_words(text):
    special_words = []
    for word in text.split():
        if re.search(r"[a-zA-Z]+(ar|er|ir|or|ur)\b", word):
            special_words.append(word)
    return special_words

def prioritize_string(text):
    special_words = extract_special_words(text)
    print(len(special_words))
    if len(special_words) == 0:
        return text[:400]
    elif len(special_words) == 1:
        index = text.index(special_words[0])
        inicio = max(index-100, 0)
        fim = index + min(len(text), 200)
        # words = text[max(index-15, 0):index] + " " + special_words[0] + " " + text[index+1:index+16]
        resultado = text[inicio:fim]
        return '...' + resultado + '...'
    elif len(special_words) > 1:
        best_words = ""
        best_count = 0
        for word in special_words:
            index = text.index(word)
            words = text[max(index-15, 0):index] + " " + word + " " + text[index+1:index+16]
            count = len(words.split())
            if count > best_count:
                best_words = words
                best_count = count
        return " ".join(best_words.split()[:30])
    else:
        return " ".join(text[:30])

text = 'no, uso da competência que lhe foi subdelegada pelo art. 2.º da Portaria CGU n.º 364, de 14 de fevereiro de 2023, o disposto no Decreto n.º 11.330, de 1.º de janeiro de 2023, no art. 38 da Lei nº 8.112, de 11 de dezembro de 1990, e o que consta no Processo n.º 00190.107429/2022-51, resolve:DESIGNar FERNANDA CURSINO VILLELA para substitu a Chefe, código FCE 1.07, da Divisão de Atendimento a Usuários da Coordenação-Geral de Infraestrutura Tecnológica da Diretoria de Tecnologia da Informação da Secretaria Executiva da Controladoria-Geral da União, em seus afastamentos e impedimentos legais ou regulamentares'
result = prioritize_string(text)
print(result)

tratado = text.replace(',','')
print(tratado)
vlad = [

'DESIGNAR'
'DISPENSAR'
'INSTAURAR'
'CEDER'
'REQUISITAR'
'DECLARAR'
'CONCEDER'
'NOMEAR'
'INDICAR'
'REINTEGRAR'
'AUTORIZAR'
'PRORROGAR'
'RECONDUZIR'
'SUBDELEGAR'
'AUTORIZA'
'RETIFICAÇÃO'
'CESSAR'
'EXONERAR'
'EXTRATO DE ACORDO DE COOPERAÇÃO NÃO ONEROSO'
'EXTRATO DE TERMO ADITIVO'
'EXTRATO DE EXTINÇÃO'

]