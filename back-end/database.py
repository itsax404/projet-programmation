import sqlite3
import os
from pathlib import Path
from classes.bases.adresse import Adresse
from classes.bases.personne import Personne
from classes.bases.entreprise import Entreprise
from classes.facture import Facture

class Database:

	def __init__(self):
		"""
		TODO docstring
		"""
		self.connexion = sqlite3.connect(os.path.join(Path(__file__).parents[1], "database.db"))
		self.__creer_tables__()

	def __creer_tables__(self):
		cursor = self.connexion.cursor()
		instructions_sql = 	[
			'CREATE TABLE IF NOT EXISTS adresses (id INTEGER PRIMARY KEY AUTOINCREMENT, numero INT, rue TEXT, code_postal INT, ville TEXT, region TEXT, pays TEXT)',
			'CREATE TABLE IF NOT EXISTS personnes (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prenom TEXT)',
			'CREATE TABLE IF NOT EXISTS entreprises (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, adresse INT, FOREIGN KEY (adresse) REFERENCES adresses(id))',
			'CREATE TABLE IF NOT EXISTS factures (id INTEGER PRIMARY KEY AUTOINCREMENT, acheteur INT, adresse_acheteur INT, entreprise INT, prix_ht DOUBLE, prix_ttc DOUBLE, date_achat DATE, fichier LONGBLOB, FOREIGN KEY (acheteur) REFERENCES personnes(id), FOREIGN KEY (adresse_acheteur) REFERENCES adresses(id), FOREIGN KEY (entreprise) REFERENCES entreprises(id))',
			'CREATE TABLE IF NOT EXISTS modeles (id INTEGER PRIMARY KEY AUTOINCREMENT,nom_modele TEXT ,rectangle_x1_1 FLOAT, rectangle_x1_2 FLOAT, rectangley1_1 FLOAT, rectangley1_2 FLOAT, utilisation_rectangle1 TEXT,rectangle_x2_1 FLOAT, rectangle_x2_2 FLOAT, rectangley2_1 FLOAT, rectangley2_2 FLOAT, utilisation_rectangle2 TEXT,rectangle_x3_1 FLOAT, rectangle_x3_2 FLOAT, rectangley3_1 FLOAT, rectangley3_2 FLOAT, utilisation_rectangle3 TEXT,rectangle_x4_1 FLOAT, rectangle_x4_2 FLOAT, rectangley4_1 FLOAT, rectangley4_2 FLOAT, utilisation_rectangle4 TEXT,rectangle_x5_1 FLOAT, rectangle_x5_2 FLOAT, rectangley5_1 FLOAT, rectangley5_2 FLOAT, utilisation_rectangle5 TEXT,rectangle_x6_1 FLOAT, rectangle_x6_2 FLOAT, rectangley6_1 FLOAT, rectangley6_2 FLOAT, utilisation_rectangle6 TEXT,rectangle_x7_1 FLOAT, rectangle_x7_2 FLOAT, rectangley7_1 FLOAT, rectangley7_2 FLOAT, utilisation_rectangle7 TEXT,rectangle_x8_1 FLOAT, rectangle_x8_2 FLOAT, rectangley8_1 FLOAT, rectangley8_2 FLOAT, utilisation_rectangle8 TEXT,rectangle_x9_1 FLOAT, rectangle_x9_2 FLOAT, rectangley9_1 FLOAT, rectangley9_2 FLOAT, utilisation_rectangle9 TEXT,rectangle_x10_1 FLOAT, rectangle_x10_2 FLOAT, rectangley10_1 FLOAT, rectangley10_2 FLOAT, utilisation_rectangle10 TEXT,rectangle_x11_1 FLOAT, rectangle_x11_2 FLOAT, rectangley11_1 FLOAT, rectangley11_2 FLOAT, utilisation_rectangle11 TEXT,rectangle_x12_1 FLOAT, rectangle_x12_2 FLOAT, rectangley12_1 FLOAT, rectangley12_2 FLOAT, utilisation_rectangle12 TEXT,rectangle_x13_1 FLOAT, rectangle_x13_2 FLOAT, rectangley13_1 FLOAT, rectangley13_2 FLOAT, utilisation_rectangle13 TEXT,rectangle_x14_1 FLOAT, rectangle_x14_2 FLOAT, rectangley14_1 FLOAT, rectangley14_2 FLOAT, utilisation_rectangle14 TEXT)'
		]
		for instruction in instructions_sql:
			cursor.execute(instruction)
		self.connexion.commit()
		cursor.close()

	def ajotuer_adresse(self, adresse: Adresse):
		"""
		TODO docstring
		:param adresse:
		:return:
		"""
		cursor = self.connexion.cursor()
		cursor.execute('INSERT INTO adresses (numero, rue, code_postal, ville, region, pays) VALUES (?, ?, ?, ?, ?, ?)', tuple(adresse.avoir_donnees().values()))
		self.connexion.commit()
		cursor.close()

	def avoir_adresse(self, id: int):
		"""
		TODO docstring
		:param id:
		:return:
		"""
		cursor = self.connexion.cursor()
		cursor.execute('SELECT * FROM adresses WHERE id = ?', (id,))
		resultat = cursor.fetchone()
		cursor.close()
		return Adresse(resultat[1], resultat[2], resultat[3], resultat[4], resultat[5], resultat[6])

	def adresse_est_dans_la_base(self, adresse: Adresse):
		adresses = self.avoir_toutes_les_adresses()
		for adresse_de_la_base in adresses:
			if adresse_de_la_base == adresse:
				return True
		return False

	def avoir_toutes_les_adresses(self):
		"""
		TODO docstring
		:return:
		"""
		cursor = self.connexion.cursor()
		cursor.execute('SELECT * FROM adresses')
		resultat = cursor.fetchall()
		adresses = []
		for adresse in resultat:
			adresse_classe = Adresse(adresse[1], adresse[2], adresse[3], adresse[4], adresse[5], adresse[6])
			adresses.append(adresse_classe)
		cursor.close()
		return adresses

	def ajouter_personne(self, personne: Personne):
		"""
		TODO docstring
		:param adresse:
		:return:
		"""
		cursor = self.connexion.cursor()
		cursor.execute('INSERT INTO personnes (nom, prenom) VALUES (?, ?, ?, ?, ?, ?)', tuple(personne.avoir_donnees().values()))
		self.connexion.commit()
		cursor.close()

	def avoir_personne(self, id: int):
		"""
		TODO docstring
		:param id:
		:return:
		"""
		cursor = self.connexion.cursor()
		cursor.execute('SELECT * FROM personnes WHERE id = ?', (id,))
		resultat = cursor.fetchone()
		cursor.close()
		return Personne(resultat[1], resultat[2])

	def avoir_toutes_les_personnes(self):
		"""
		TODO docstring
		:return:
		"""
		cursor = self.connexion.cursor()
		cursor.execute('SELECT * FROM personnes')
		resultat = cursor.fetchall()
		personnes = []
		for personne in resultat:
			personne_classe = Personne(personne[1], personne[2])
			personnes.append(personne_classe)
		cursor.close()
		return personnes

	def ajouter_entreprise(self, entreprise: Entreprise):
		curseur = self.connexion.cursor()
		adresse_entreprise = entreprise.adresse
		if not self.adresse_est_dans_la_base(adresse_entreprise):
			self.ajouter_adresse(adresse_entreprise)
		self.connexion.commit()
		curseur.close()

	def ajouter_facture(self, facture: Facture):
		"""
		TODO docstring
		:param facture:
		:return:
		"""
		donnees = facture.avoir_donnees()
		cursor = self.connexion.cursor()
		cursor.execute('INSERT INTO factures (nom_acheteur, prenom_acheteur, adresse_acheteur, enseigne_magasin, adresse_magasin, prix_ht, prix_ttc, date_achat, fichier) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', donnees.values())
		self.connexion.commit()
		cursor.close()
