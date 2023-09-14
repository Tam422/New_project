import streamlit as st

import matplotlib.pyplot as plt
from bokeh.plotting import figure
import altair as alt
import pandas as pd 
import numpy as np
import seaborn as sns
from PIL import Image



#Correction dataset
#list_ech_to_corr = [292,293,294, 295] 
#for ech in list_ech_to_corr:
#    df.loc[df['sample_Number'] == ech, 'mode'] = 'mode5'

def main():
    st.title("Exploration de l'influence des paramètres")
    st.write("Dans cette partie nous allons explorer notre jeu de données et tenter de répondre au questions suivantes:")
    st.write("Existe-t-il des relations entre les paramètres  enregistrés?")
    st.write("Dans quelle mesure les modes de fonctionnement de la Fardeleuse influencent-ils ces paramètres? ")
    path = './One_year_compiled.csv'
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

#if st.sidebar.checkbox("Afficher les Données Brutes", False):
    st.subheader("Jeu de données")
    if st.checkbox("Afficher le jeu de donnée"):
        st.write(df)



    
    @st.cache_data (persist=True)
    def plotCorrelationMatrix(df):
        corr = df.corr()
        ax = sns.heatmap(
            corr, 
            annot=True, fmt='.1f', linewidths=.5,
            vmin=-1, vmax=1, center=0,
            cmap='coolwarm',
            square=True)
        ax.set_xticklabels(
            ax.get_xticklabels(),
            rotation=45,
            horizontalalignment='right')
        st.pyplot(plt)

    @st.cache_data (persist=True)
    def pairplot(df_para):
        sns.pairplot(df_para, hue='mode', palette='Set1')
        st.pyplot(plt)

    def select_colonne(df,selected_Col ):
        nouveau_df = df[selected_Col]
        return nouveau_df
    
    st.header("Analyse des paramètres de fonctionnement de la machine")
    
    st.subheader("Matrice des Corrélations")
    st.write("La matrice de corrélation nous permet de visualiser le degré de dépendance entre les différents paramètres de la machine. ")
    selected_Col1 = ['Cut_Motor', 'Cut_Lag_error', 'Cut_Actual_position',
        'Cut_Actual_speed', 'Film_Actual_position', 'Film_Actual_speed',
        'Film_Lag_error', 'Spintor_VAX_speed']
    df_para1 = select_colonne(df, selected_Col1)
    plotCorrelationMatrix(df_para1)
    st.write("Il en ressort que:")
    st.write("Le couple du moteur (Cut_Motor) est le paramètre qui présente le plus de corrélations avec les paramètres de vitesse(_Actual speed) et de décallage (_lag error) de la lame et du film. Le couple moteur étant responsable du mouvement de la lame, il n'est pas étonnant que l'intensité de la corrélation du moteur avec les paramètres propre à la lame soit plus intense qu'avec ceux du film.")
    st.write("Les paramètres propres à la lame ne semblent pas avoir de corrélations ni entre eux, ni avec les autres, à l'exception de la vitesse de coupe (Cut_Actual speed) qui elle semble être reliée à la vitesse et au décalage du film (Film_Actual speed et Film_lag error), tout comme le couple moteur mais dans des dégrés différents.")
    st.write("Parmis les paramètres propres au film plastique, on peut noter que le décallage et la vitesse présentent une légère corrélation entre eux. La vitesse du film présente la plus forte correlation avec le paramètre Spintor_VAX_speed. Ce qui est intéressant dans la mesure où nous avons peu d'informations sur ce paramètre. ")
    st.write("Enfin on remarque que les variables de position du film et de la lame ne semblent pas influencer de façon importante les autres paramètres.")



    st.subheader("Matrice des Graphiques")
    st.write("Afin d'amèliorer notre vision d'ensemble des paramètres, on affiche la matrice des graphiques ")
    st.write("On décide également de colorer les données en fonction du mode de fonctionnement. " )
    
    #Le temps de calcul pour obtenir ce graphe étant supérieur à 15 min
    #On décide de remplacer le code par l'affichage d'une image
    image = Image.open('./pairplot.png')
    st.image(image, caption='Pairplot')
    #selected_Col2 = ['Cut_Motor', 'Cut_Lag_error', 'Cut_Actual_position',
    #    'Cut_Actual_speed', 'Film_Actual_position', 'Film_Actual_speed',
    #    'Film_Lag_error', 'Spintor_VAX_speed','mode']
    #df_para2 = select_colonne(df, selected_Col2)
    #pairplot(df_para2)

    st.write("On constate que pour certains graphiques, le format semble dépendant du mode")

    def select_colonne(df,selected_Col ):
            nouveau_df = df[selected_Col]
            return nouveau_df

    @st.cache_data (persist=True)    
    def graph(df, parameter_X, parameter_Y):
        brush = alt.selection(type='interval')
        points = alt.Chart(df).mark_point().encode(
        x= parameter_X ,
        y=parameter_Y ,
        color=alt.condition(brush, 'mode' , alt.value('Black'))
        ).add_params(brush)
        if parameter_X == 'timestamp':
            st.subheader(f"{parameter_Y} en fonction du tps")
        else:
            st.subheader(f"{parameter_Y} en fonction de {parameter_X}")
        st.write(points)
        return points
    
    parameter_X = st.selectbox(
        "parameter X",
        ('Cut_Motor', 'Cut_Lag_error', 'Cut_Actual_position',
       'Cut_Actual_speed', 'Film_Actual_position', 'Film_Actual_speed',
       'Film_Lag_error', 'Spintor_VAX_speed'))
    
    parameter_Y = st.selectbox(
        "parameter Y",
        ('Cut_Motor', 'Cut_Lag_error', 'Cut_Actual_position',
       'Cut_Actual_speed', 'Film_Actual_position', 'Film_Actual_speed',
       'Film_Lag_error', 'Spintor_VAX_speed'))
    
    point3 = graph(df, parameter_X, parameter_Y)
    


if __name__ == "__main__":
    main()