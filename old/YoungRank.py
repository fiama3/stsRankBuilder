import pandas as pd
import numpy as np


#Inizializzo i dataframe per il totale non definitivo
df_young_rank_pergusa_final = pd.DataFrame(columns=['Full Name', 'Category', 'Club', 'Pts Pergusa'])
df_young_rank_marinadimodica_final = pd.DataFrame(columns=['Full Name', 'Category', 'Club', 'Pts Marina di Modica'])
df_young_rank_cefalu_final = pd.DataFrame(columns=['Full Name', 'Category', 'Club', 'Pts Cefalù'])
df_young_rank_augusta_final = pd.DataFrame(columns=['Full Name', 'Category', 'Club', 'Pts Augusta'])
df_young_rank_catania_final = pd.DataFrame(columns=['Full Name', 'Category', 'Club', 'Pts Catania'])


#importo il file dei punti
df_points = pd.read_excel('pointsyoung.xlsx')

#Importo i file delle singole gare per uomini donne e bambini
df_young_results_pergusa = pd.read_excel('resultsyoungPergusa.xlsx')

#Pulisco i dataframe lasciando solo i dati utili alla classifica
df_young_results_pergusa_3field = df_young_results_pergusa[['CatPos', 'Category', 'Club', 'Surname', 'FirstName']].copy()

#Genero la classifica di ogni singola gara per uomini donne bambini
# inner join
df_young_rank_pergusa = pd.merge(df_young_results_pergusa_3field,df_points,on='CatPos',how='left')

df_young_rank_pergusa = df_young_rank_pergusa[['CatPos', 'Category', 'Club', 'Surname', 'FirstName', 'Full']]

#Genero la classifica totale per uomini donne e bambini
df_young_rank_pergusa.insert(0,'Full Name', df_young_rank_pergusa['Surname'] + ' ' + df_young_rank_pergusa['FirstName'])

df_young_rank_pergusa_final = df_young_rank_pergusa.drop(['Surname', 'FirstName'], 1)

#Cambio il nome delle colonne
df_young_rank_pergusa_final.columns = ['Full Name', 'CatPos', 'Category', 'Club', 'Pts Pergusa']

#Genero dataframe con nome e punteggio totale ordinato per punteggio

df_young_rank_total = df_young_rank_pergusa_final.merge(df_young_rank_marinadimodica_final, on=['Full Name', 'Category', 'Club'], how='outer').merge(df_young_rank_cefalu_final, on=['Full Name', 'Category', 'Club'], how='outer').merge(df_young_rank_augusta_final, on=['Full Name', 'Category', 'Club'], how='outer').merge(df_young_rank_catania_final, on=['Full Name', 'Category', 'Club'], how='outer').fillna(0)


df_young_rank_total.insert(9, 'Total', df_young_rank_total['Pts Pergusa'] + df_young_rank_total['Pts Marina di Modica'] + df_young_rank_total['Pts Cefalù'] + df_young_rank_total['Pts Augusta'] + df_young_rank_total['Pts Catania'])

#Ordino per punteggio finale
df_young_rank_total = df_young_rank_total.sort_values(['Category', 'Total'], ascending=[False, False])

#Salvo in file
#print(df_young_rank_pergusa_final)
#print(df_woman_rank_pergusa_final)
print(df_young_rank_total)

df_young_rank_total.to_excel('TotalRankYoung.xlsx', index=True) 