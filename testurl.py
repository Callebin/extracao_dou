text = "This is a TEXT with DESIGNAR BERNARDINHO, some of which are KEYWORDS."

keywords = ["KEYWORDS", "SOME"]

upper_case_words = []
previous_word_was_upper_case = False

for word in text.split():
    if word.isupper() and (word not in keywords or not previous_word_was_upper_case):
        if previous_word_was_upper_case:
            upper_case_words[-1] += " " + word
        else:
            upper_case_words.append(word)
        previous_word_was_upper_case = True
    else:
        previous_word_was_upper_case = False

print(upper_case_words)
