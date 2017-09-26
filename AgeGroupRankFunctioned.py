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
		df_results_race_3field = df_results_race[['Pos', 'Surname', 'FirstName', 'Club']].copy()

		#Genero la classifica di ogni singola gara per uomini donne bambini
		df_rank_race = pd.merge(df_results_race_3field,df_points,on='Pos',how='left')

		#Verifico se si tratta di gara a punteggio doppio e se i partenti sono <=50
		#UOMINI
		double = 0
		if ("Etna" == racename):
			double = 1

		if (len(df_rank_race.index) < 50):
			if (double):
				df_rank_race = df_rank_race[['Pos', 'Surname', 'FirstName', 'Club', 'Full']]
			else:
				df_rank_race = df_rank_race[['Pos', 'Surname', 'FirstName', 'Club', 'Half']]
		else:
			if (double):
				df_rank_race = df_rank_race[['Pos', 'Surname', 'FirstName', 'Club', 'Double']]
			else:
				df_rank_race = df_rank_race[['Pos', 'Surname', 'FirstName', 'Club', 'Full']]

		#Genero la classifica totale per uomini donne e bambini
		df_rank_race.insert(0,'Full Name', df_rank_race['Surname'] + ' ' + df_rank_race['FirstName'])

		df_rank_race_final = df_rank_race.drop(['Pos', 'Surname', 'FirstName'], 1)

		#Cambio il nome delle colonne
		df_rank_race_final.columns = ['Full Name', 'Club', 'Pts ' + racename]
	else:
		df_rank_race_final = pd.DataFrame(columns=['Full Name', 'Club', 'Pts ' + racename])
	return df_rank_race_final

def calcolaTotale(df_rank_total, races):
	total = 0
	#Aggiungo la colonna col totale
	for race in races:
		total = total + df_rank_total['Pts ' + race[0]]
		
	df_rank_total.insert(len(df_rank_total.columns), 'Total', total)

	#Ordino per punteggio finale
	df_rank_total = df_rank_total.sort_values(['Total'], ascending=[False])
	return df_rank_total


def mergeGare(df_rank_races_final):
	#print(type(df_rank_races_final[1]))
	#Genero dataframe con nome e punteggio totale ordinato per punteggio
	df_rank_total = pd.DataFrame(columns=['Full Name','Pts'])

	#Faccio merge di tutte le gare
	for (i, df_race) in enumerate(df_rank_races_final):
		df_rank_total = df_rank_total.merge(pd.DataFrame(df_race), on='Full Name', how='outer')

	#Elimino colonna Pts aggiunta per tracchiggio
	df_rank_total = df_rank_total.drop('Pts',1)

	df_rank_total = df_rank_total.fillna(0)
	return df_rank_total



#Creo la lista delle gare
my_path = os.path.abspath(os.path.dirname(__file__))
races = [['Pergusa', my_path+'/dataIn/resultsmanPergusa.xlsx',my_path+'/dataIn/resultswomanPergusa.xlsx'],['Marzamemi',my_path+'/dataIn/resultsmanMarzamemi.xlsx',my_path+'/dataIn/resultswomanMarzamemi.xlsx'],['Marina di Modica',my_path+'/dataIn/resultsmanMarinadimodica.xlsx',my_path+'/dataIn/resultswomanMarinadimodica.xlsx'],['Cefalu',my_path+'/dataIn/resultsmanCefalu.xlsx',my_path+'/dataIn/resultswomanCefalu.xlsx'],['Etna',my_path+'/dataIn/resultsmanEtna.xlsx',my_path+'/dataIn/resultswomanEtna.xlsx'],['Augusta',my_path+'/dataIn/resultsmanAugusta.xlsx',my_path+'/dataIn/resultswomanAugusta.xlsx'],['Catania',my_path+'/dataIn/resultsmanCatania.xlsx',my_path+'/dataIn/resultswomanCatania.xlsx']]
df_man_rank_race_final = []
df_woman_rank_race_final = []
#Creo i dataframe delle singole gare per uomini e donne
for (i, race) in enumerate(races):
	df_man_rank_race_final.append(rankSingolaGara(race[0], race[1], my_path+'/dataIn/points.xlsx'))
	df_woman_rank_race_final.append(rankSingolaGara(race[0], race[2], my_path+'/dataIn/points.xlsx'))

#Calcolo il dataframe totale per uomini e donne
df_man_rank_total = mergeGare(df_man_rank_race_final)
df_woman_rank_total = mergeGare(df_woman_rank_race_final)
df_man_rank_total = calcolaTotale(df_man_rank_total, races)
df_woman_rank_total = calcolaTotale(df_woman_rank_total, races)

#Salvo in file (sovrascrivo)
print(df_man_rank_total)
print(df_woman_rank_total)
df_man_rank_total.to_excel(my_path+'/TotalRankUomini.xlsx', index=False) 
df_woman_rank_total.to_excel(my_path+'/TotalRankDonne.xlsx', index=False)