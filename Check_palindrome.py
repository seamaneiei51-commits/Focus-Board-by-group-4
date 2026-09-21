def function(word):
    lower_word = word.lower()
    if lower_word == lower_word[::-1]:
        return True
    else:
        return False