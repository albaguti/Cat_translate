import streamlit as st
import pandas as pd
from translate import Translator
from simplemma import text_lemmatizer
from nltk.corpus import wordnet as wn
import nltk
import re
import os

st.set_page_config(
    page_title="Cat Traductor",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.github.com/albaguti/cat-traductor',
        'Report a bug': "https://www.github.com/albaguti/cat-traductor/issues",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

path = os.getcwd() + "/nltk_data"
if os.path.exists(path):
    st.success("Data already exists !")
else:
    with st.spinner("Please wait we are downloading the NLTK Data."):
        mode = 0o777
        os.mkdir(path, mode)
        nltk.download('wordnet', download_dir=path)
        nltk.download('omw-1.4', download_dir=path)
    st.success("NLTK Data has been downloaded successfully !")

nltk.data.path.append(path)

st.header("Aplicacio per a traduir paraules a múltiples idiomes:", divider='rainbow')

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
    translator = Translator(from_lang=language_code, to_lang=idioma_output)
    frase_traduida = translator.translate(frase)
    paraula_traduida = translator.translate(paraula)
    arrel = text_lemmatizer(paraula_traduida, lang=idioma_output)[0]
    new_row = pd.DataFrame({ "Traducció": [frase_traduida], "Paraula": [paraula_traduida], "Idioma": [idioma], "Arrel": arrel})
    taula = pd.concat([taula, new_row], ignore_index=True)

st.table(taula)


st.divider()
st.header("Sinònims de la paraula introduida:", divider='rainbow')
# Streamlit input for the word
derivat = st.text_input("Introdueix la paraula per a buscar tots els seus significats:", key="paraula_sinonims")

# Find synonyms in Catalan
synonyms = wn.synsets(derivat, lang='cat')

# Regex pattern to extract lemma and form
pattern = r"Lemma\('(.*?)\.n\.\d+\.(.*?)'\)"
# Extract and store all pairs
pairs = []
for syn in synonyms:
    # Convert synset to string to apply regex
    syn_str = str(syn.lemmas(lang='cat'))
    match = re.search(pattern, syn_str)
    if match:
        lemma_form = match.group(1), match.group(2)
        pairs.append(lemma_form)

# Create a DataFrame from the pairs
df = pd.DataFrame(pairs, columns=['Lemma', 'Form'])

# Display the DataFrame in Streamlit
st.dataframe(df, use_container_width=True)
