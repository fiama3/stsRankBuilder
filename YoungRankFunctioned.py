
import pandas as pd
import numpy as np
import os  

def rankSingolaGara(racename, rusultsfilepath, pointsfilepath):
	if(os.path.isfile(rusultsfilepath)):
		#importo il file dei punti
		df_points = pd.read_excel(pointsfilepath)

		#Importo i file delle singole gare per uomini donne e bambini
		df_results_race = pd.read_excel(rusultsfilepath)
	    
		#Pulisco i dataframe lasciando solo i dati utili alla classifica
		df_results_race_3field = df_results_race[['CatPos', 'Category', 'Club', 'Surname', 'FirstName']].copy()

		#Genero la classifica di ogni singola gara per uomini donne bambini
		df_rank_race = pd.merge(df_results_race_3field,df_points,on='CatPos',how='left')

		df_rank_race = df_rank_race[['CatPos', 'Category', 'Club', 'Surname', 'FirstName', 'Full']]

		#Genero la classifica totale per uomini donne e bambini
		df_rank_race.insert(0,'Full Name', df_rank_race['Surname'] + ' ' + df_rank_race['FirstName'])

		df_rank_race_final = df_rank_race.drop(['CatPos', 'Surname', 'FirstName'], 1)

		#Cambio il nome delle colonne
		df_rank_race_final.columns = ['Full Name', 'Category', 'Club', 'Pts ' + racename]
	else:
		df_rank_race_final = pd.DataFrame(columns=['Full Name', 'Category', 'Club','Pts ' + racename])

	return df_rank_race_final

def calcolaTotale(df_rank_total, races):
	total = 0
	#Aggiungo la colonna col totale
	for race in races:
		total = total + df_rank_total['Pts ' + race[0]]
		
	df_rank_total.insert(len(df_rank_total.columns), 'Total', total)

	#Ordino per punteggio finale
	df_rank_total = df_rank_total.sort_values(['Category', 'Total'], ascending=[False, False])
	return df_rank_total

def mergeGare(df_rank_races_final):
	#print(type(df_rank_races_final[1]))
	#Genero dataframe con nome e punteggio totale ordinato per punteggio
	df_rank_total = pd.DataFrame(columns=['Full Name', 'Category', 'Club', 'Pts'])

	#Faccio merge di tutte le gare
	for (i, df_race) in enumerate(df_rank_races_final):
		df_rank_total = df_rank_total.merge(pd.DataFrame(df_race), on=['Full Name', 'Category'], how='outer')

	#Elimino colonna Pts aggiunta per tracchiggio
	df_rank_total = df_rank_total.drop('Pts',1)

	df_rank_total = df_rank_total.fillna(0)
	return df_rank_total



#Creo la lista delle gare
my_path = os.path.abspath(os.path.dirname(__file__))
races = [['Pergusa', my_path+'/dataIn/resultsyoungPergusa.xlsx'],['Cefalu', my_path+'/dataIn/resultsyoungCefalu.xlsx'],['Augusta', my_path+'/dataIn/resultsyoungAugusta.xlsx'],['Marina di Modica', my_path+'/dataIn/resultsyoungMarinadimodica.xlsx'],['Catania', my_path+'/dataIn/resultsyoungCatania.xlsx']]
df_young_rank_race_final = []
#Creo i dataframe delle singole gare per uomini e donne
for (i, race) in enumerate(races):
	print(race[1])
	df_young_rank_race_final.append(rankSingolaGara(race[0], race[1], my_path+'/dataIn/pointsyoung.xlsx'))

#Calcolo il dataframe totale per uomini e donne
df_young_rank_total = mergeGare(df_young_rank_race_final)
df_young_rank_total = calcolaTotale(df_young_rank_total, races)

#Salvo in file (sovrascrivo)
df_young_rank_total.to_excel(my_path+'/TotalRankGiovani.xlsx', index=False)