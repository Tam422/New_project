import streamlit as st

import matplotlib.pyplot as plt
from bokeh.plotting import figure
import altair as alt
import pandas as pd 
import numpy as np
import seaborn as sns
import calendar
import locale
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

def main():

    path = '/Users/tam/code/Tam422/Projet_MP/Local/One_year_compiled.csv'
    @st.cache_data (persist=True)
    def export_data(path, nRowsRead=None):
        df = pd.read_csv(path, delimiter=',', nrows = nRowsRead)
        #CHANGER LE NOM DES COLONNES
        new_names = {'pCut::Motor_Torque': 'Cut_Motor', 
                        'pCut::CTRL_Position_controller::Lag_error': 'Cut_Lag_error', 
                        'pCut::CTRL_Position_controller::Actual_position': 'Cut_Actual_position', 
                        'pCut::CTRL_Position_controller::Actual_speed': 'Cut_Actual_speed', 
                        'pSvolFilm::CTRL_Position_controller::Actual_position': 'Film_Actual_position', 
                        'pSvolFilm::CTRL_Position_controller::Actual_speed': 'Film_Actual_speed', 
                        'pSvolFilm::CTRL_Position_controller::Lag_error': 'Film_Lag_error', 
                        'pSpintor::VAX_speed': 'Spintor_VAX_speed'}
        df.rename(columns=new_names, inplace=True)
        return df
    df = export_data(path, nRowsRead=None)
    
    def select_ligne(df,record_number, record_size):
        start = int(0 +(record_number-1)*record_size)
        end = int(start + record_size)
        sliced_df = df.iloc[start:end]
        return sliced_df

    def select_colonne(df,selected_Col ):
        nouveau_df = df[selected_Col]
        return nouveau_df
    
    def graph(df, parameter_X, parameter_Y):
        brush = alt.selection(type='interval')
        points = alt.Chart(df).mark_point().encode(
        x= parameter_X ,
        y=parameter_Y ,
        color=alt.condition(brush, 'mode' , alt.value('Black'))
        ).add_params(brush)
        if parameter_X == 'timestamp':
            st.subheader(f"{parameter_Y} en fonction du temps")
        else:
            st.subheader(f"{parameter_Y} en fonction de {parameter_X}")
        st.write(points)
        return points
    
    record_size = 2049
    record_number = st.sidebar.number_input(
        "Choisir un numéro d'échantillon entre 1 et 519", 1,519, step=1)
    selected_Col = ['timestamp','Cut_Motor', 'Cut_Lag_error', 'Cut_Actual_position',
        'Cut_Actual_speed', 'Film_Actual_position', 'Film_Actual_speed',
        'Film_Lag_error', 'Spintor_VAX_speed','mode']
   
    sliced_df = select_ligne(df,record_number, record_size).reset_index(drop=True)
    final_df_tps = select_colonne(sliced_df, selected_Col)
    
    jr = sliced_df["day"][1]
    mois = calendar.month_name[int(sliced_df["month"][1])].capitalize()
    hr = int(sliced_df["hour"][1])// 10000
    min = (int(sliced_df["hour"][1])% 10000) // 100

    st.title("Visualisation d'un enregistrement")
    st.write("La visualisation des enregistrements nous permet de repérer le caractère périodique et constant de certains paramètres.")
    st.write(" Choisissez un numéro d'échantillon dans la barre latérale")
    
    st.sidebar.write(f" Enregistrement pris le {jr} {mois} à {hr}:{min}")

    point_Cut_Motor = graph(final_df_tps, 'timestamp', 'Cut_Motor')
    st.write(f"Couple moteur de la lame (périodique).")

    point_Cut_Lag_error = graph(final_df_tps, 'timestamp', 'Cut_Lag_error')
    st.write(f"Ce paramètre représente l'erreur de position instantanée entre le point de consigne du générateur de trajectoire et la position réelle du codeur de courant du moteur (périodique).")


    point_Cut_Actual_position = graph(final_df_tps, 'timestamp', 'Cut_Actual_position')
    st.write("Position de la lame de coupe en mm (constant). ")

    point_Cut_Actual_speed = graph(final_df_tps, 'timestamp', 'Cut_Actual_speed')
    st.write("Vitesse de la lame de coupe (périodique). ")

    point_Film_Actual_position = graph(final_df_tps, 'timestamp', 'Film_Actual_position')
    st.write("Position du dérouleur de film en mm (constant). ")

    point_Film_Actual_speed = graph(final_df_tps, 'timestamp', 'Film_Actual_speed')
    st.write("Vitesse du dérouleur de film plastique (périodique). ")

    point_Film_Lag_error = graph(final_df_tps, 'timestamp', 'Film_Lag_error')
    st.write("Représente l'erreur de position instantanée entre le point de consigne du générateur de trajectoire et la position réelle du codeur de courant du moteur (périodique). ")

    point_Film_Spintor_VAX_speed= graph(final_df_tps, 'timestamp', 'Spintor_VAX_speed')
    st.write("Pas d'information (constant). ")

    pointXY = graph(final_df_tps, 'Cut_Actual_speed', 'Film_Actual_speed')
    st.write("Graphique additionnel de la vitesse du dérouleur de film en fonction de la vitesse de la lame. On constate que chaque coupe dessine un motif régulier. Ce motif diffère en fonction des modes et est plus ou moins constant en fonction des échantillons. ")

    point1 = graph(final_df_tps, 'Spintor_VAX_speed',  'Film_Actual_speed')
    st.write("Graphique additionnel")

    point2 = graph(final_df_tps, 'Film_Actual_speed',  'Film_Lag_error')
    st.write("Graphique additionnel")




if __name__ == "__main__":
    main()