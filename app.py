import streamlit as st
import pandas as pd
from translate import Translator
from simplemma import text_lemmatizer

import urllib.request
from bs4 import BeautifulSoup

def get_context_based_translation(source_lang, target_lang, sentence):
    search = "+" + sentence.replace(" ", "+")
    url = f'http://context.reverso.net/translation/{source_lang}-{target_lang}/' + search
    page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')

    # Assuming the first translation is the most relevant
    translated_word = soup.find_all("div", {"class": "trg"})[0].em.text
    return translated_word


st.header("Aplicacio per a automaticament traduir paraules:")

languages = {
    "català": "ca",
    "anglès": "en",
    "francès": "fr",
    "espanyol": "es",
    "alemany": "de",
    "italià": "it",
    "portugues": "pt",
    "rumanès": "ro",
    "polones": "pl",
    "holandes": "nl",
    "grec": "el",
    "hongares": "hu",
    "norueg": "no",
    "finlandes": "fi",
    "suec": "sv",
    "danès": "da"
}

idioma_input = st.selectbox("Selecciona l'idioma de la paraula a traduir:", list(languages.keys()))

paraula = st.text_input("Introdueix la paraula a traduir:")

frase = st.text_input("Introdueix la frase per a definir el context:")


language_code = languages[idioma_input]
idiomes_output = st.multiselect("Selecciona els idiomes al/s qual/s vols traduir la paraula:", list(languages.keys()))
taula = pd.DataFrame(columns=[ "Paraula","Arrel", "Traducció", "Idioma"])

for idioma in idiomes_output:
    idioma_output = languages[idioma]
    translated_word = get_context_based_translation(idioma_input, idioma_output, frase)

    translator = Translator(from_lang=language_code, to_lang=idioma_output)
    frase_traduida = translator.translate(frase)
    paraula_traduida = translator.translate(paraula)
    arrel = text_lemmatizer(paraula, lang=idioma_output)[0]
    new_row = pd.DataFrame({ "Traducció": [frase_traduida], "Paraula": [paraula_traduida], "Idioma": [idioma], "Arrel": arrel})
    taula = pd.concat([taula, new_row], ignore_index=True)

st.table(taula)
