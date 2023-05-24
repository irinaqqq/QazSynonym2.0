import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize

def find_synonyms(input_text):
    words = word_tokenize(input_text)
    synonyms_dict = {}

    # Find synonyms for each word in the text
    for wrd in words:
        # Exclude words like "A" and "the"
        if wrd.lower() in ["a", "the"]:
            continue
        
        # Find synsets (sets of synonyms) for the word
        synsets = wn.synsets(wrd)
        # If synsets are found, add the word and its synonyms to the dictionary
        if synsets:
            synonyms = []
            for synset in synsets:
                # Get the synonyms for the synset
                syn_list = synset.lemma_names()
                synonyms.extend(syn_list)
            # Exclude words that contain "_" and have only one character
            synonyms = [s for s in synonyms if not ("_" in s or len(s) == 1)]
            word_kk = translate_textkk(wrd.lower())
            synonyms_kk = [translate_textkk(syn.lower()) for syn in synonyms]
            synonyms_dict[word_kk] = set(synonyms_kk)

    return synonyms_dict





import requests

def translate_texten(text):
    api_key = 'trnsl.1.1.20230418T235155Z.fd3bcdc52bf66856.5cb5e0070fb5c4064672349f59be246111e93bf8'
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    params = {
        'key': api_key,
        'text': text,
        'lang': 'kk-en'
    }
    response = requests.get(url, params=params)
    json_data = response.json()
    translated_text = json_data['text'][0]
    return translated_text

def translate_textkk(text):
    api_key = 'trnsl.1.1.20230418T235155Z.fd3bcdc52bf66856.5cb5e0070fb5c4064672349f59be246111e93bf8'
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    params = {
        'key': api_key,
        'text': text,
        'lang': 'en-kk'
    }
    response = requests.get(url, params=params)
    json_data = response.json()
    translated_text = json_data['text'][0]
    return translated_text


input_text = "Жылдам қоңыр түлкі жалқау иттің үстінен секіреді."
input_texten = translate_texten(input_text)
print(input_texten)
# input_texten = translate_textkk(input_texten)
# print(input_texten)
synonyms_dict = find_synonyms(input_texten)

for word, synonyms in synonyms_dict.items():
    print(f"{word}: {', '.join(synonyms)}")

# word_kk = translate_textkk(word.lower())
# synonyms_kk = ", ".join(translate_textkk(syn.lower()) for syn in synonyms)
# print(f"{word_kk}: {synonyms_kk}")