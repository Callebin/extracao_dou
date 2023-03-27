# text = "This is some sample text with a code snippet FCE 5.8. and some other stuff DAS 5678."

# FCE  = ['DAS', 'FCE']  # list of target words to find

# for word in text.split():
#     for target in FCE:
#         if target in word:
#             # extract the digits that come after the target word
#             digits = ""
#             for char in word[len(target):]:
#                 if char.isdigit():
#                     digits += char
#                 elif char == ".":
#                     digits += char
#                     break  # stop at the first non-digit character (except dot)
#             print(target + digits)  # print the target word and the digits found


cod_funcao = ['DAS', 'FCE']

# def find_word(text):
#     words = text.split()
#     result = []
#     for i in range(len(words)):
#         if words[i] in cod_funcao:
#             word = words[i]
#             j = i + 1
#             while j < len(words) and (words[j] == ' ' or words[j].isdigit() or words[j] == '.'):
#                 result.append(words[j])
#                 j += 1
#             return (word, ''.join(result))
#     return None

text = "Nomear NARA MEIRELLY LIMA RODRIGUES, código FCE 1.03, da Coordenação-Geral de Gestão de Pessoas"

for word in text.split():
    if word in cod_funcao:
            index = text.index(word)
            cod = text[index+len(word):index+len(word)+5].strip()
            print(word, cod)
