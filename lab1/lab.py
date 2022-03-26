import re
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import nltk
import pymorphy2
from nltk.tokenize import word_tokenize, sent_tokenize

urls = ['https://ru.wikipedia.org/wiki/MTV_Unplugged_in_New_York', 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D0%BB-%D0%B3%D1%83%D0%B1%D0%B5%D1%80%D0%BD%D0%B0%D1%82%D0%BE%D1%80%D0%BE%D0%B2_%D0%91%D0%B0%D1%80%D0%B1%D0%B0%D0%B4%D0%BE%D1%81%D0%B0',
        'https://ru.wikipedia.org/wiki/%D0%90%D0%B2%D1%81%D1%82%D1%80%D0%B0%D0%BB%D0%B8%D1%8F_%D0%B2%D0%BE_%D0%92%D1%82%D0%BE%D1%80%D0%BE%D0%B9_%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%BE%D0%B9_%D0%B2%D0%BE%D0%B9%D0%BD%D0%B5']

links = ''
morph = pymorphy2.MorphAnalyzer()
lemmas = ''
lemma_freq = {}

for i in range(len(urls)):
    source = urlopen(urls[i]).read()

    soup = BeautifulSoup(source, 'html.parser')
    text = ''
    for paragraph in soup.find_all('p'):
        text += paragraph.text

    for img in soup.find_all('img'):
        links += img['src'][2:] + '\n'

    text = re.sub(r'\[][@#%^]+', '', text)

    with open(f'text{i + 1}.txt', 'w') as f:
        f.write(text)

    word_tokenized_text = word_tokenize(text, language="russian")

    for word in word_tokenized_text:
        if word[0].isalpha():
            lemmas += morph.parse(word)[0].normal_form + " "

    print(f"{i + 1} TOKENIZED TEXT:")
    print("TOKENIZED BY SENTENCE:")
    print(sent_tokenize(text, language="russian"))
    print("TOKENIZED BY WORDS:")
    print(word_tokenized_text)

    # with open(f'text{i}.txt', 'w') as f:
    #     f.write(text)
with open(f'links.txt', 'w') as f:
    f.write(links)

with open(f'lemmas.txt', 'w') as f:
    f.write(lemmas)

for lemma in lemmas.split(" "):
    if not lemma in lemma_freq.keys():
        lemma_freq[lemma] = 1
    else:
        lemma_freq[lemma] += 1

print(lemma_freq)

with open('lemmas_frequencies.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['lemma', 'frequency'])
    for key in lemma_freq.keys():
        csvfile.write("%s, %s\n" % (key, lemma_freq[key]))

headers = ['Лемма', 'Частота']
data = []

for lemma in lemma_freq.keys():
    data.append([lemma, lemma_freq[lemma]])

with open('lemmas_frequencies.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(data)
