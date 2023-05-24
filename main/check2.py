import requests

def translate_text(text):
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

kazakh_text = 'Сәлем, әлем!'
english_text = translate_text(kazakh_text)
print(english_text)
