desig = ['DESIGNAR', 'Designar', 'DISPENSAR', 'Dispensar', 'SUBSTITUIR', 'Substituir', 'NOMEAR', 'Nomear']
comissao = ['COMISSÃO', 'Comissão', 'comissão', 'COMISSAO', 'Comissao', 'SINDICÂNCIA', 'Sindicância', 'SINDICANCIA', 'Sindicancia']

def check_desig(text):
    
    words = text.split()  # split text into a list of words
    for word in words:
        if word in desig and all(forbidden not in words for forbidden in comissao):
            return word
    return None


print(check_desig('Designar minha rola na'))