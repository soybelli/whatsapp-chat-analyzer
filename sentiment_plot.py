import string
from collections import Counter

import matplotlib.pyplot as plt

# reading text file
def sentiment_plot():
    text = open("data.txt", encoding="utf-8").read()

    # converting to lowercase
    lower_case = text.lower()

    # Removing punctuations
    cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))

    # splitting text into words
    tokenized_words = cleaned_text.split()

    f=open('stop_words.txt','r')
    stop_words=f.read()


    # Removing stop words from the tokenized words list
    final_words = []
    for word in tokenized_words:
        if word not in stop_words:
            final_words.append(word)

    # NLP Emotion Algorithm NATURAL LANGUAGE PROCESSING
    # 1) Check if the word in the final word list is also present in emotion.txt
    #  - open the emotion file
    #  - Loop through each line and clear it
    #  - Extract the word and emotion using split

    # 2) If word is present -> Add the emotion to emotion_list
    # 3) Finally count each emotion in the emotion list

    emotion_list = []
    with open("emotion.txt", 'r') as file:
        for line in file:
            clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
            word, emotion = clear_line.split(':')

            if word in final_words:
                emotion_list.append(emotion)

    #print(emotion_list)
    w = Counter(emotion_list)
    # print(w)
    return w
