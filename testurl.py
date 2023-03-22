keywords = ['partir']

input_string = 'Designar bernardinho, a partir de 1 de julho de 2022'

for keyword in keywords:
    if keyword in input_string:
        start_index = input_string.index(keyword) + len(keyword)
        for i in range(start_index, len(input_string)):
            if input_string[i:i+4].isdigit():
                end_index = i + 4
                break
        else:
            end_index = len(input_string)
        extracted_text = input_string[start_index:end_index]
        print(extracted_text)





