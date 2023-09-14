### CLI à lancer : 
# streamlit run app.py


import streamlit as st
from PIL import Image

@st.cache_data (persist=True)
def main():
    st.title("Création d’un outils No-Code avec Streamlite pour découvrir les paramètres de fonctionnement d'une Fardeleuse.")
    image = Image.open('./Fardeleuse.png')
    st.image(image, caption='Fardeleuse')

if __name__ == '__main__':
    main()
