-- Début de la transaction
BEGIN;

-- Toujours utiliser le même schéma
SET search_path TO "ParcourStat";


/* 

Après examen de notre jeu de données, nous avons remarqué qu'entre 2018 et 2024 certains établissements changent de noms ou de type de saisie. La problématique réside dans le Code_UAI, qui ne change pas, ce qui, sans normalisation, créerait deux valeurs pour un même code. 

Nous avons donc pensé cette requête afin de normaliser les noms des établissements communs aux deux jeux de données, au sein de tables temporaires. 

Le script se base sur le Code_UAI : s'il repère le même Code_UAI avec deux valeurs différentes dans la colonne "Etablissement", alors il normalise en appliquant au jeu de donnée 2018, la valeur de 2024. 

De cette manière, nous facilitons l'insertion future des données dans les tables définitives et réduisons les conflits de clés primaires.

De plus, nous avons pensé cette requête pour résoudre un second problème : la présence de Code_UAI ayant pour valeur "identifiant obsolète" dans le csv de 2018. 
En effet, 29 établissements en 2018 présentent en Code_UAI 'identifiant obsolète', ce qui aurait posé problème pour pour instaurer le code_UAI comme clé primaire.

Ainsi nous avons pensé une seconde requête qui se base sur les coordonnées GPS. Si des enregistrements ont les même coordonnées GPS 
entre 2018 et 2024 mais des valeurs différentes dans "Etablissement" et "Code_UAI", la normalisation s'effectue selon la grahie de 2024.

Après de multiples vérifications, ces établissement ne semblent pas avoir leurs équivalent strict en 2024. 
Nous nous retrouvons dans l'impossibilité de croiser ces données, et avons donc été contraints d'effacer ces données de nos tables temporaires. 
Néanmoins, nous laissons la seconde requête par sûreté.

*/




-- Première requête : normalisation des noms d'établissement selon la graphie de 2024 et selon la correspondance du Code_UAI
UPDATE tmp_parcoursup2018 AS tp1
SET "Etablissement" = tp2."Etablissement" -- On remplace la valeur de "Etablissement" dans tmp_parcoursup2018 par celle de 2024
FROM tmp_parcoursup2024 AS tp2
WHERE tp1."Code_UAI" = tp2."Code_UAI" -- Sur la base de la correspondance entre les code UAI 2018 et 2024
  AND tp1."Etablissement" != tp2."Etablissement" -- La valeur est modifiée uniquement si une différence est relevée 
  AND tp2."Code_UAI" IS NOT NULL  -- La valeur est modifiée uniquement si le code UAI n'est pas null 
  AND TRIM(tp2."Code_UAI") != '' -- La valeur est modifiée uniquement si la valeur n'est pas vide
  AND LOWER(TRIM(tp2."Code_UAI")) != 'identifiant obsolète'; -- La valeur est modifiée uniquement si elle n'est pas 'identifiant_obsolète' (il n'y en a pas en 2024).


-- Deuxième requête : normalisation des codes UAI et des noms d'établissements selon la correspondance des coordonnées GPS, avec une priorité à la graphie de 2024. 
UPDATE tmp_parcoursup2018 AS tp1
SET 
    "Etablissement" = tp2."Etablissement", -- On remplace les valeurs "Etablissement" et "Code_UAI" en 2018 par celles de 2024 
    "Code_UAI" = tp2."Code_UAI"
FROM tmp_parcoursup2024 AS tp2
WHERE tp1."Coordonnees_gps_formation" = tp2."Coordonnees_gps_formation" -- Sur correspondance des données GPS
  AND (tp1."Code_UAI" IS NULL -- Même critère que la requête précédente. Il faut que le Code_UAI soit valide.
       OR TRIM(tp1."Code_UAI") = '' 
       OR LOWER(TRIM(tp1."Code_UAI")) = 'identifiant obsolète')
  AND tp2."Code_UAI" IS NOT NULL 
  AND TRIM(tp2."Code_UAI") != ''
  AND LOWER(TRIM(tp2."Code_UAI")) != 'identifiant obsolète'
  AND tp2."Coordonnees_gps_formation" IS NOT NULL -- Même critère que la requête précédente mais appliquées aux coordonnées GPS.
  AND TRIM(tp2."Coordonnees_gps_formation") != ''
  AND tp1."Coordonnees_gps_formation" IS NOT NULL 
  AND TRIM(tp1."Coordonnees_gps_formation") != '';


-- On réalise un processus similaire pour les Académies entre 2018 et 2024. 

/* Nous avons remarqué des changements d'Académie entre 2018 et 2024. Par exemple, pour un établissement en Normandie présent en 2018 et 2024, il peut avoir en 2018 l'académie de Rouen, et en 2024 l'académie de Normandie. 
Pour notre table établissement, cela poserait problème. 

Ainsi nous allons normaliser les données. Si un établissement présente une telle différence, alors il y aura une normalisation en faisant primer la valeur de 2024. 

*/

UPDATE tmp_parcoursup2018 tp1
SET "Academie_etablissement" = tp2."Academie_etablissement"
FROM tmp_parcoursup2024 tp2
WHERE tp1."Code_UAI" = tp2."Code_UAI"
  AND tp1."Academie_etablissement" != tp2."Academie_etablissement";



-- Fin de la transaction 
COMMIT;
