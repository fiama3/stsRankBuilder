import pandas as pd
import numpy as np

#Inizializzo i dataframe per il totale non definitivo
df_man_rank_pergusa_final = pd.DataFrame(columns=['Full Name','Pts Pergusa'])
df_man_rank_marzamemi_final = pd.DataFrame(columns=['Full Name','Pts Marzamemi'])
df_man_rank_marinadimodica_final = pd.DataFrame(columns=['Full Name','Pts Marina di Modica'])
df_man_rank_cefalu_final = pd.DataFrame(columns=['Full Name','Pts Cefalù'])
df_man_rank_etna_final = pd.DataFrame(columns=['Full Name','Pts Etna'])
df_man_rank_augusta_final = pd.DataFrame(columns=['Full Name','Pts Augusta'])
df_man_rank_catania_final = pd.DataFrame(columns=['Full Name','Pts Catania'])
df_woman_rank_pergusa_final = pd.DataFrame(columns=['Full Name','Pts Pergusa'])
df_woman_rank_marzamemi_final = pd.DataFrame(columns=['Full Name','Pts Marzamemi'])
df_woman_rank_marinadimodica_final = pd.DataFrame(columns=['Full Name','Pts Marina di Modica'])
df_woman_rank_cefalu_final = pd.DataFrame(columns=['Full Name','Pts Cefalù'])
df_woman_rank_etna_final = pd.DataFrame(columns=['Full Name','Pts Etna'])
df_woman_rank_augusta_final = pd.DataFrame(columns=['Full Name','Pts Augusta'])
df_woman_rank_catania_final = pd.DataFrame(columns=['Full Name','Pts Catania'])


#importo il file dei punti
df_points = pd.read_excel('points.xlsx')

#Importo i file delle singole gare per uomini donne e bambini
df_man_results_pergusa = pd.read_excel('resultsmanPergusa.xlsx')
df_woman_results_pergusa = pd.read_excel('resultswomanPergusa.xlsx')
#df_young_results_pergusa = pd.read_excel('resultsyoungPergusa.xlsx')

#Pulisco i dataframe lasciando solo i dati utili alla classifica
df_man_results_pergusa_3field = df_man_results_pergusa[['Pos', 'Surname', 'FirstName']].copy()
df_woman_results_pergusa_3field = df_woman_results_pergusa[['Pos', 'Surname', 'FirstName']].copy()
#df_young_results_pergusa_3field = df_young_results_pergusa[['CatPos', 'Category', 'Surname', 'FirstName']].copy()

#Genero la classifica di ogni singola gara per uomini donne bambini
# inner join
df_man_rank_pergusa = pd.merge(df_man_results_pergusa_3field,df_points,on='Pos',how='left')
df_woman_rank_pergusa = pd.merge(df_woman_results_pergusa_3field,df_points,on='Pos',how='left')

#Verifico se si tratta di gara a punteggio doppio e se i partenti sono <=50
#UOMINI
if (len(df_man_rank_pergusa.index) < 50):
	df_man_rank_pergusa = df_man_rank_pergusa[['Pos', 'Surname', 'FirstName', 'Half']]
else:
	df_man_rank_pergusa = df_man_rank_pergusa[['Pos', 'Surname', 'FirstName', 'Full']]

#DONNE
if (len(df_woman_rank_pergusa.index) < 50):
	df_woman_rank_pergusa = df_woman_rank_pergusa[['Pos', 'Surname', 'FirstName', 'Half']]
else:
	df_woman_rank_pergusa = df_woman_rank_pergusa[['Pos', 'Surname', 'FirstName', 'Full']]


#Genero la classifica totale per uomini donne e bambini
df_man_rank_pergusa.insert(0,'Full Name', df_man_rank_pergusa['Surname'] + ' ' + df_man_rank_pergusa['FirstName'])
df_woman_rank_pergusa.insert(0,'Full Name', df_woman_rank_pergusa['Surname'] + ' ' + df_woman_rank_pergusa['FirstName'])

df_man_rank_pergusa_final = df_man_rank_pergusa.drop(['Pos', 'Surname', 'FirstName'], 1)
df_woman_rank_pergusa_final = df_woman_rank_pergusa.drop(['Pos', 'Surname', 'FirstName'], 1)

#Cambio il nome delle colonne
df_man_rank_pergusa_final.columns = ['Full Name', 'Pts Pergusa']
df_woman_rank_pergusa_final.columns = ['Full Name', 'Pts Pergusa']

#Genero dataframe con nome e punteggio totale ordinato per punteggio

df_man_rank_total = df_man_rank_pergusa_final.merge(df_man_rank_marzamemi_final, on='Full Name', how='outer').merge(df_man_rank_marinadimodica_final, on='Full Name', how='outer').merge(df_man_rank_cefalu_final, on='Full Name', how='outer').merge(df_man_rank_etna_final, on='Full Name', how='outer').merge(df_man_rank_augusta_final, on='Full Name', how='outer').merge(df_man_rank_catania_final, on='Full Name', how='outer').fillna(0)

df_woman_rank_total = df_woman_rank_pergusa_final.merge(df_woman_rank_marzamemi_final, on='Full Name', how='outer').merge(df_woman_rank_marinadimodica_final, on='Full Name', how='outer').merge(df_woman_rank_cefalu_final, on='Full Name', how='outer').merge(df_woman_rank_etna_final, on='Full Name', how='outer').merge(df_woman_rank_augusta_final, on='Full Name', how='outer').merge(df_woman_rank_catania_final, on='Full Name', how='outer').fillna(0)

df_man_rank_total.insert(8, 'Total', df_man_rank_total['Pts Pergusa'] + df_man_rank_total['Pts Marzamemi'] + df_man_rank_total['Pts Marina di Modica'] + df_man_rank_total['Pts Cefalù'] + df_man_rank_total['Pts Etna'] + df_man_rank_total['Pts Augusta'] + df_man_rank_total['Pts Catania'])
df_woman_rank_total.insert(8, 'Total', df_woman_rank_total['Pts Pergusa'] + df_woman_rank_total['Pts Marzamemi'] + df_woman_rank_total['Pts Marina di Modica'] + df_woman_rank_total['Pts Cefalù'] + df_woman_rank_total['Pts Etna'] + df_woman_rank_total['Pts Augusta'] + df_woman_rank_total['Pts Catania'])

#Ordino per punteggio finale
df_man_rank_total = df_man_rank_total.sort('Total', ascending=False)
df_woman_rank_total = df_woman_rank_total.sort('Total', ascending=False)

#Salvo in file
#print(df_man_rank_pergusa_final)
#print(df_woman_rank_pergusa_final)
print(df_man_rank_total)
print(df_woman_rank_total)
df_man_rank_total.to_excel('TotalRankUomini.xlsx', index=False) 
df_woman_rank_total.to_excel('TotalRankDonne.xlsx', index=False) 


def rankSingolaGara(racename, rusultsfilepath, pointsfilepath):
	#importo il file dei punti
	df_points = pd.read_excel(pointsfilepath)

	#Importo i file delle singole gare per uomini donne e bambini
	df_man_results_pergusa = pd.read_excel(rusultsfilepath)
    
	#Pulisco i dataframe lasciando solo i dati utili alla classifica
	df_man_results_pergusa_3field = df_man_results_pergusa[['Pos', 'Surname', 'FirstName']].copy()

	#Genero la classifica di ogni singola gara per uomini donne bambini
	df_man_rank_pergusa = pd.merge(df_man_results_pergusa_3field,df_points,on='Pos',how='left')

	#Verifico se si tratta di gara a punteggio doppio e se i partenti sono <=50
	#UOMINI
	if (len(df_man_rank_pergusa.index) < 50):
		df_man_rank_pergusa = df_man_rank_pergusa[['Pos', 'Surname', 'FirstName', 'Half']]
	else:
		df_man_rank_pergusa = df_man_rank_pergusa[['Pos', 'Surname', 'FirstName', 'Full']]

	#Genero la classifica totale per uomini donne e bambini
	df_man_rank_pergusa.insert(0,'Full Name', df_man_rank_pergusa['Surname'] + ' ' + df_man_rank_pergusa['FirstName'])

	df_man_rank_pergusa_final = df_man_rank_pergusa.drop(['Pos', 'Surname', 'FirstName'], 1)

	#Cambio il nome delle colonne
	df_man_rank_pergusa_final.columns = ['Full Name', 'Pts ' + racename]

    return df_man_rank_pergusa_final