# ParcourStat - Base de données Parcoursup

## Description 
ParcourStat est une base de données relationnelle fondée sur PostgreSQL qui récupère et structure des données Parcoursup issues des sessions de 2024 et de 2018 tout en permettant de les comparer. Elle permet plus globalement une analyse de l'offre de formation de l'enseignement supérieur à l'aide de données issues des candidatures et des admissions des étudiants au sein des établissements. 

## Objectifs
Notre base de données a pour objectif de : 
- Structurer les données Parcoursup en un modèle logique de données
- Faciliter une comparaison entre les données de 2018 et 2024
- Permettre une lecture des données sur l'enseignement supérieur à travers des indicateurs géographiques
- Concrétiser l'enrichissement des données issues de wikidata pour les établissements
- Permettre l'élaboration future de datavisualisations et, à terme, d'une application Flask

## Source principale de données 
Notre base de données est fondée sur des données Parcoursup des sessions de 2018 et 2024, récupérées sous la forme de fichiers csv depuis le site du gouvernement français : 
- https://www.data.gouv.fr/datasets/parcoursup-2018-voeux-de-poursuite-detudes-et-de-reorientation-dans-lenseignement-superieur-et-reponses-des-etablissements 
- https://www.data.gouv.fr/datasets/parcoursup-2024-voeux-de-poursuite-detudes-et-de-reorientation-dans-lenseignement-superieur-et-reponses-des-etablissements

Comme évoqué lors de la réunion, ces jeux de données ont subi des modifications pour que Postgres les accepte : les en-têtes de certaines colonnes ont étées renommées suivant le système d'abréviation ci-dessous.

| NOM_ORIGINE                                                                                                                                      | NOM_ABREGE    |
| ------------------------------------------------------------------------------------------------------------------------------------------------ | ------------- |
| Effectif des admis en phase complémentaire                                                                                                       | EA_PC         |
| Dont effectif des admis ayant reçu leur proposition d’admission à l'ouverture de la procédure principale                                         | EA_PA_OP      |
| Dont effectif des admis ayant reçu leur proposition d’admission avant le baccalauréat                                                            | EA_PA_AB      |
| Dont effectif des admis ayant reçu leur proposition d’admission avant la fin de la procédure principale                                          | EA_PA_PP      |
| Dont effectif des admis en internat                                                                                                              | EA_I          |
| Dont effectif des admis boursiers néo bacheliers                                                                                                 | EA_BN_B       |
| Effectif des admis néo bacheliers                                                                                                                | EA_NB         |
| Effectif des admis néo bacheliers généraux                                                                                                       | EA_NB_G       |
| Effectif des admis néo bacheliers technologiques                                                                                                 | EA_NB_T       |
| Effectif des admis néo bacheliers professionnels                                                                                                 | EA_NB_P       |
| Effectif des autres candidats admis                                                                                                              | EA_AC         |
| Dont effectif des admis néo bacheliers sans information sur la mention au bac                                                                    | EA_NB_SI      |
| Dont effectif des admis néo bacheliers sans mention au bac                                                                                       | EA_NB_SM      |
| Dont effectif des admis néo bacheliers avec mention Assez Bien au bac                                                                            | EA_NB_AB      |
| Dont effectif des admis néo bacheliers avec mention Bien au bac                                                                                  | EA_NB_B       |
| Dont effectif des admis néo bacheliers avec mention Très Bien au bac                                                                             | EA_NB_TB      |
| Dont effectif des admis néo bacheliers avec mention Très Bien avec félicitations au bac                                                          | EA_NB_TBF     |
| Effectif des admis néo bacheliers généraux ayant eu une mention au bac                                                                           | EA_NB_G_M     |
| Effectif des admis néo bacheliers technologiques ayant eu une mention au bac                                                                     | EA_NB_T_M     |
| Effectif des admis néo bacheliers professionnels ayant eu une mention au bac                                                                     | EA_NB_P_M     |
| Dont effectif des admis issus du même établissement (BTS/CPGE)                                                                                   | EA_NB_IME     |
| Dont effectif des admises issues du même établissement (BTS/CPGE)                                                                                | EA_F_IME      |
| Dont effectif des admis issus de la même académie                                                                                                | EA_IMA        |
| Dont effectif des admis issus de la même académie (Paris/Créteil/Versailles réunies)                                                             | EA_IMA_PCV    |
| % d’admis ayant reçu leur proposition d’admission à l'ouverture de la procédure principale                                                       | PA_OP_PP      |
| % d’admis ayant reçu leur proposition d’admission avant le baccalauréat                                                                          | PA_AB         |
| % d’admis ayant reçu leur proposition d’admission avant la fin de la procédure principale                                                        | PA_AF_PP      |
| % d’admis dont filles                                                                                                                            | PA_F          |
| % d’admis néo bacheliers issus de la même académie                                                                                               | PA_NB_IMA     |
| % d’admis néo bacheliers issus de la même académie (Paris/Créteil/Versailles réunies)                                                            | PA_NB_IMA_PCV |
| % d’admis néo bacheliers issus du même établissement (BTS/CPGE)                                                                                  | PA_NB_IME     |
| % d’admis néo bacheliers boursiers                                                                                                               | PA_NB_B       |
| % d’admis néo bacheliers                                                                                                                         | PA_NB         |
| % d’admis néo bacheliers sans information sur la mention au bac                                                                                  | PA_NB_SI_MB   |
| % d’admis néo bacheliers sans mention au bac                                                                                                     | PA_NB_SM      |
| % d’admis néo bacheliers avec mention Assez Bien au bac                                                                                          | PA_NB_AB      |
| % d’admis néo bacheliers avec mention Bien au bac                                                                                                | PA_NB_B       |
| % d’admis néo bacheliers avec mention Très Bien au bac                                                                                           | PA_NB_TB      |
| % d’admis néo bacheliers avec mention Très Bien avec félicitations au bac                                                                        | PA_NB_TB_F    |
| % d’admis néo bacheliers généraux                                                                                                                | PA_NB_G       |
| Dont % d’admis avec mention (BG)                                                                                                                 | PA_M_BG       |
| % d’admis néo bacheliers technologiques                                                                                                          | PA_NB_T       |
| Dont % d’admis avec mention (BT)                                                                                                                 | PA_M_BT       |
| % d’admis néo bacheliers professionnels                                                                                                          | PA_NB_P       |
| Dont % d’admis avec mention (BP)                                                                                                                 | PA_M_BP       |
| Effectif total des candidats pour une formation                                                                                                  | ET_C          |
| Dont effectif des candidates pour une formation                                                                                                  | ET_CF         |
| Effectif total des candidats en phase principale                                                                                                 | ET_C_PP       |
| Dont effectif des candidats ayant postulé en internat                                                                                            | EC_I          |
| Effectif des candidats néo bacheliers généraux en phase principale                                                                               | EC_NB_G       |
| Dont effectif des candidats boursiers néo bacheliers généraux en phase principale                                                                | EC_B_NB_G     |
| Effectif des candidats néo bacheliers technologiques en phase principale                                                                         | EC_NB_T       |
| Dont effectif des candidats boursiers néo bacheliers technologiques en phase principale                                                          | EC_B_NB_T     |
| Effectif des candidats néo bacheliers professionnels en phase principale                                                                         | EC_NB_P       |
| Dont effectif des candidats boursiers néo bacheliers professionnels en phase principale                                                          | EC_B_NB       |
| Effectif des autres candidats en phase principale                                                                                                | EC_AC         |
| Effectif total des candidats en phase complémentaire                                                                                             | ETC_PC        |
| Effectif des candidats néo bacheliers généraux en phase complémentaire                                                                           | EC_NB_G_PC    |
| Effectif des candidats néo bacheliers technologique en phase complémentaire                                                                      | EC_NB_T_PC    |
| Effectif des candidats néo bacheliers professionnels en phase complémentaire                                                                     | EC_NB_P_PC    |
| Effectifs des autres candidats en phase complémentaire                                                                                           | EAC_PC        |
| Effectif total des candidats classés par l’établissement en phase principale                                                                     | ETC_CE        |
| Effectif des candidats classés par l’établissement en phase complémentaire                                                                       | EC_CE_PC      |
| Effectif des candidats classés par l’établissement en internat (CPGE)                                                                            | EC_CE_I       |
| Effectif des candidats classés par l’établissement hors internat (CPGE)                                                                          | EFC_CE_HI     |
| Effectif des candidats néo bacheliers généraux classés par l’établissement                                                                       | EC_NB_CE      |
| Dont effectif des candidats boursiers néo bacheliers généraux classés par l’établissement                                                        | EC_B_NB_CE    |
| Effectif des candidats néo bacheliers technologiques classés par l’établissement                                                                 | EC_NB_T_CE    |
| Dont effectif des candidats boursiers néo bacheliers technologiques classés par l’établissement                                                  | EC_B_NB_T_CE  |
| Effectif des candidats néo bacheliers professionnels classés par l’établissement                                                                 | EC_NB_CE      |
| Dont effectif des candidats boursiers néo bacheliers professionnels classés par l’établissement                                                  | EC_B_NB_P_CE  |
| Effectif des autres candidats classés par l’établissement                                                                                        | EC_AC_CE      |
| Effectif total des candidats ayant reçu une proposition d’admission de la part de l’établissement                                                | ETC_R_PA      |
| Effectif total des candidats ayant accepté la proposition de l’établissement (admis)                                                             | ETC_A_PE      |
| Dont effectif des candidates admises                                                                                                             | ETC_F_A_PE    |
| Effectif des candidats en terminale générale ayant reçu une proposition d’admission de la part de l’établissement                                | EC_TG_PA_E    |
| Dont effectif des candidats boursiers en terminale générale ayant reçu une proposition d’admission de la part de l’établissement                 | EC_B_TG_PA_E  |
| Effectif des candidats en terminale technologique ayant reçu une proposition d’admission de la part de l’établissement                           | EC_TT_PA_E    |
| Dont effectif des candidats boursiers en terminale technologique ayant reçu une proposition d’admission de la part de l’établissement            | EC_B_TT_PA_E  |
| Effectif des candidats en terminale professionnelle ayant reçu une proposition d’admission de la part de l’établissement                         | EC_TP_PA_E    |
| Dont effectif des candidats boursiers en terminale générale professionnelle ayant reçu une proposition d’admission de la part de l’établissement | EC_B_TP_PA_E  |
| Effectif des autres candidats ayant reçu une proposition d’admission de la part de l’établissement                                               | EAC_PA_E      |



## Croisement et enrichissement des données
Les données issues de Parcoursup ont été enrichies par des données sur les établissements requêtées depuis wikidata. Ainsi, les données suivantes sur les établissements ont été ajoutées  au sein de notre base de données :
- site web
- adresse 
- nombre d'étudiants
- logo
- image

## Architecture de la base de données 
Notre base de données compte 10 tables organisées comme suit : 

- Tables de données géographiques :
  - Académies  
  - Communes
  - Départements
  - Régions 

- Tables de données statistiques relatives aux étudiants : 
  - Candidatures
  - Admissions

- Tables de données générales sur l'enseignement supérieur :
  - Disciplines
  - Formations
  - Type_formations
  - Etablissements


### Note sur les tables candidatures et admissions 
Les tables 'Candidatures' et 'Admissions' possèdent un grand nombre d'attributs. Toutefois, ces tables sont déjà issues d'une sélection effectuée depuis les csv d'origine, et contiennent donc uniquement les données que nous souhaitons conserver. La table 'Admissions' intègre notamment des calculs de pourcentage déjà effectués au sein des données originales, utiles à notre analyse.

### Contenu du dépôt 
Ce dépôt Github contient : 
- un dossier global 'Application'.
- une image du modèle logique de notre base.
- une image du modèle physique de notre base.
- un sous-dossier 'csv' avec trois fichiers csv : parcoursup2018, parcoursup2024, wikidata.
- un sous-dossier 'sql' contenant quatre scripts sql : un script de création des tables de travail, un script de normalisation des données, un script de création des tables définitives, un script de création des vues.
- un fichier 'run.py' contenant un script python qui lance la création de la base de données.
  Comme évoqué lors de la réunion, ce fichier a été modifié car sniffer ne reconnaisait pas nos séparateurs.

## Installation de la base de données 
Pour installer notre base de données, il faut :
- Créer la base de données : 
CREATE DATABASE "ParcourStat";
- Créer le schéma au sein de la base de données :
CREATE SCHEMA "ParcourStat";

- Télécharger les requirements.txt dans un environnement virtuel
- Lancer la commande 'python run.py' pour exécuter l'installation

## Auteurs 
- Florian Martin
- Solange Cussaguet
- Anaelle Martinez
- Clotilde Long




