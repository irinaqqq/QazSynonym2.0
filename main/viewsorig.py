from django.shortcuts import render,HttpResponse
from googletrans import Translator
import nltk


nltk.download('wordnet')
from nltk.corpus import wordnet
# Create your views here.


def home_view(request):
    words = {}
    text = ''
    if request.method == "POST":
        if "translate" in request.POST:
            text = request.POST["translate"]
            # print(text)
            
            translator = Translator() 
            translate_text = translator.translate(text, src='auto', dest='en')  
            # print(translate_text.text)
            Text1 = translate_text.text.lower().replace('.', '')
            word_list = Text1.split()
            
            
            # print(word_list)
            for word in word_list:
                
                kk_word = translator.translate(word, src='auto', dest='kk')
                kk_word = kk_word.text
                
                
                synonyms = get_some_word_synonyms(word)
                if synonyms:
                    words[kk_word]= []
                    # print( kk_word, 's synonym is:')
                    for synonym in synonyms:
                        # print(synonym)
                        translate_text = translator.translate(synonym, src='auto', dest='kk')
                        synonym = translate_text.text
                        
                        words[kk_word].append(synonym)
                        # print("     ", translate_text.text)
                        # result.append(translate_text.text)
                
            print(*words)           
                    
        
    # return redirect('result')
    return render(request,'index.html', {'words': words, 'text': text})


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
        if (lemma_name != word and lemma_name not in synonyms):
            synonyms.append(lemma_name)
    return synonyms

def result(request):
     return render(request,'result.html')