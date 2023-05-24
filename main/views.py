from django.shortcuts import render, HttpResponse
from googletrans import Translator
import nltk
import functools

nltk.download('wordnet')
from nltk.corpus import wordnet

translator = Translator()

# cache for storing translation results
translate_cache = {}

# cache decorator to cache translation results
def cache_translation(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key in translate_cache:
            return translate_cache[key]
        result = func(*args, **kwargs)
        translate_cache[key] = result
        return result
    return wrapper

# Create your views here.
def home_view(request):
    words = {}
    text = ''
    if request.method == "POST":
        
        text = request.POST["translate"]
        # print(text)
        
        translator = Translator() 
        translate_text = translator.translate(text, src='auto', dest='en')  
        # print(translate_text.text)
        
        text1 = translate_text.text.lower().replace('.', '')
        word_list = text1.split()
        
        
        for word in word_list:
            kk_word = translator.translate(word, src='auto', dest='kk').text
            if kk_word not in words:
                words[kk_word] = set()
            synonyms = get_some_word_synonyms(word)
            if synonyms:
                for synonym in synonyms:
                    if synonym.lower() == word:
                        continue
                    translate_text = translator.translate(synonym, src='auto', dest='kk')
                    synonym = translate_text.text
                    words[kk_word].add(synonym.lower())
        words = {k: v for k, v in words.items() if v}         
        
    return render(request,'index.html', {'words': words, 'text': text})


# Cache the translation results for get_some_word_synonyms function
@cache_translation
def translate(text, src, dest):
    return translator.translate(text, src=src, dest=dest)

def get_some_word_synonyms(word):
    word = word.lower()
    synonyms = []
    synsets = wordnet.synsets(word)
    if (len(synsets) == 0):
        return []
    synset = synsets[0]
    lemma_names = synset.lemma_names()
    for lemma_name in lemma_names:
        lemma_name = lemma_name.lower().replace('_', ' ')
        if (lemma_name != word):
            translate_text = translate(lemma_name, 'en', 'kk')
            synonym = translate_text.text.lower()
            if (synonym != word and synonym not in synonyms):
                synonyms.append(synonym)
    return synonyms

def result(request):
    return render(request,'result.html')