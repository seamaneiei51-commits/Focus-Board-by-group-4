def remove_and_count(text):
    if "Python" in text:
        modified_text = text.replace("Python ", "")
        words = modified_text.split()
        print("your sentence is :", modified_text)
        return len(words)
    elif "python" in text:
        modified_text = text.replace("python ", "")
        words = modified_text.split()
        print("your sentence is :", modified_text)
        return len(words)
    else:
        print('There is no word "Python" in your text')