from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def get_context_based_translation(source_lang, target_lang, sentence):
    search = "+" + sentence.replace(" ", "+")
    url = f'http://context.reverso.net/translation/{source_lang}-{target_lang}/' + search

    # Define headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
    }

    # Create a Request object with the headers
    req = Request(url, headers=headers)

    # Use the Request object to open the URL
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')

# Find all elements with the class "trg"
    translations = soup.find_all("div", {"class": "trg"})
    print(translations)
    # Check if any translations were found
    if translations:
        # Assuming the first translation is the most relevant
        translated_word = translations[0].em.text
        return translated_word
    else:
        # Handle the case where no translations were found
        return "No translation found"

text = "el cap del carrer"
translated_word = get_context_based_translation('catalan', "german", text)
print(translated_word)
