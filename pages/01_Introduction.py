import streamlit as st

import matplotlib.pyplot as plt
from bokeh.plotting import figure
import altair as alt
import pandas as pd 
import numpy as np
import seaborn as sns
from PIL import Image

def main():
        
    st.title("Introduction")

    st.header("Context")
    st.write("La fardeleuse Vega d'OCME est déployée sur de grandes lignes de production dans l'industrie alimentaire et des boissons. La machine regroupe les bouteilles ou les canettes en vrac en fonction de la taille de l'emballage, les enveloppe dans un film plastique, puis rétracte le film plastique à chaud pour les réunir dans un emballage. Le film plastique est introduit dans la machine à partir de grandes bobines et est ensuite coupé à la longueur nécessaire pour l'enrouler autour d'un paquet de marchandises.")
    if st.checkbox("Voir le fonctionnement en vidéo"):
        video_file = open('video.mp4', 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)
    st.write("Le système de coupe se compose d'une lame et d'une contre-lame entraînées par un moteur sans balais. Cela garantit une grande précision à toutes les vitesses.\n L'ensemble du système de coupe se déplace et peut être positionné automatiquement à l'endroit où la vitesse de déroulement est faible en fonction de la longueur du film et de la vitesse de la machine.")

    st.header("Objectifs")
    st.write(" L'ensemble de coupe est un composant important de la machine pour atteindre l'objectif de haute disponibilité. La lame doit donc être réglée et entretenue correctement. En outre, la lame ne peut pas être inspectée visuellement pendant le fonctionnement, car elle est enfermée dans un boîtier métallique et sa vitesse de rotation est rapide.")
    image = Image.open('./Cut_blade.png')
    st.image(image, caption='Lame de coupe')
    st.write( "La surveillance des lames de coupe peut permettre de modéliser le phénomène de dégradation. Ceci augmenterait la fiabilité des machines et réduirait les temps d'arrêt imprévus dus à des coupes défectueuses.")

    st.header("Problèmatiques du jeu de données")
    st.write("Nous disposons de 519 fichiers csv")
    st.write("Chaque fichier représente un enregistrement du système de coupe d'environ 8 secondes, avec une mesure prise toute les 4 ms, soit un total de 2048 lignes pour chaque fichier. Ainsi chaque colonne représente une série temporelle.")
    st.write("Nous détaillerons les paramètres enregistrés dans la page suivante intitulée 'Visualisation des enregistrements'.")
    st.write("Nous disposons de très peu d'informations concernant les données de ce jeux. Nous allons utiliser streamlit pour explorer ce jeu de données.")

    st.subheader("Nomenclature des fichiers")
    st.write("Chaque fichier est nommé de la façon suivante:  MM-DDTHHMMSS_NUM_modeX.csv")
    st.write("MM est le mois de 1 à 12 (pas le mois calendaire)")
    st.write("DD est le jour du mois")
    st.write("HHMMSS est l'heure de début du jour d'enregistrement.")
    st.write("NUM est le numéro de l'échantillon ")
    st.write("X représente le mode. La machine peut être utilisée dans 8 modes différents et à plusieurs vitesses. ")
    
if __name__ == "__main__":
    main()