text = "REMOVER is an EXAMPLE text that DESIGNAR MULTIPLE PALAVRAS capitalized WORDS."

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
print(upper_words)
print(target)

keywords = [
    'DISPENSAR',
    'DESIGNAR',
    'APLICAR',
    'CONCEDER',
    'REVERTER',
    'SUBSTITUIR',
    'CONVALIDADOS',
    'PARTIR DE ',
    'DURANTE',
    'DE ',
    'TORNAR ',
    'CEDER',
    'CONVALIDADOS',
    'FICANDO',
    'TORNANDO',
    'REMOVER'
]
keylow = []
for el in keywords:
    keylow.append(el.lower())

print(keylow)
