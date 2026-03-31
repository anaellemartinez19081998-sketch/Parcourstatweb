
-- Début de la transaction
BEGIN;

CREATE SCHEMA IF NOT EXISTS "ParcourStat";

-- Toujours utiliser le même schéma
SET search_path TO "ParcourStat";

-- Création de la table temporaire parcoursup2018 et transformation des données : suppression des espaces et normalisation

CREATE TABLE TMP_parcoursup2018 AS (
SELECT
    CAST("Annee" as INT) as "Annee",
	TRIM("Code_UAI") as "Code_UAI",
	TRIM("Etablissement") as "Etablissement",
	CASE -- Permet de normaliser avec efficacité le code départemental de la Corse du Sud.
        WHEN TRIM(INITCAP("Departement_etablissement")) = 'Corse-Du-Sud' THEN '2A'
        ELSE TRIM(CAST("Code_departemental_etablissement" as VARCHAR(100)))
    END AS "Code_departemental_etablissement",
	CASE -- Permet de normaliser avec efficacité les tirets de Corse-Du-Sud. 
		WHEN TRIM(INITCAP("Departement_etablissement")) = 'Corse Du Sud' THEN 'Corse-Du-Sud'
		ELSE TRIM(INITCAP("Departement_etablissement"))
	END AS "Departement_etablissement",
	CASE -- Normalisation des noms des régions.
        WHEN TRIM("Region_etablissement") = 'Auvergne-Rhône-Alpes' THEN 'Auvergne-Rhône-Alpes'
        WHEN TRIM("Region_etablissement") = 'Bourgogne-Franche-Comté' THEN 'Bourgogne-Franche-Comté'
        WHEN TRIM("Region_etablissement") = 'Bretagne' THEN 'Bretagne'
        WHEN TRIM("Region_etablissement") = 'Centre-Val de Loire' THEN 'Centre-Val-de-Loire'
		WHEN TRIM("Region_etablissement") = 'Centre' THEN 'Centre-Val-de-Loire'
        WHEN TRIM("Region_etablissement") = 'Grand Est' THEN 'Grand-Est'
        WHEN TRIM("Region_etablissement") = 'Hauts-de-France' THEN 'Hauts-de-France'
        WHEN TRIM("Region_etablissement") = 'Île-de-France' THEN 'Île-de-France'
        WHEN TRIM("Region_etablissement") = 'Normandie' THEN 'Normandie'
        WHEN TRIM("Region_etablissement") = 'Nouvelle Aquitaine' THEN 'Nouvelle-Aquitaine'
        WHEN TRIM("Region_etablissement") = 'Occitanie' THEN 'Occitanie'
        WHEN TRIM("Region_etablissement") = 'Pays de la Loire' THEN 'Pays-de-la-Loire'
        WHEN TRIM("Region_etablissement") = 'Provence Alpes Côte d''Azur' THEN 'Provence-Alpes-Côte-d''Azur'
        WHEN TRIM("Region_etablissement") = 'Guadeloupe' THEN 'Guadeloupe'
        WHEN TRIM("Region_etablissement") = 'Martinique' THEN 'Martinique'
        WHEN TRIM("Region_etablissement") = 'Guyane' THEN 'Guyane'
        WHEN TRIM("Region_etablissement") = 'Mayotte' THEN 'Mayotte'
		WHEN TRIM("Academie_etablissement") = 'Etranger' THEN 'Etranger'
		WHEN TRIM("Academie_etablissement") = 'Polynésie Française' THEN 'Polynésie Française'
        ELSE TRIM("Region_etablissement")
    END as "Region_etablissement" ,
	TRIM("Academie_etablissement") as "Academie_etablissement",
	TRIM("Filiere_formation_tres_agregee") as "Filiere_formation_tres_agregee",
	TRIM("Filiere_formation") as "Filiere_formation",
	TRIM("Concours_communs_banques_epreuves") as "Concours_communs_banques_epreuves",
	TRIM("Filiere_formation_detaillee") as "Filiere_formation_detaillee",
	TRIM("Filiere_formation_tres_detaillee") as "Filiere_formation_tres_detaillee",
	TRIM("Lien_formation_Parcoursup") as "Lien_formation_parcoursup",
	TRIM("Coordonnees_GPS_formation") as "Coordonnees_gps_formation",
	CAST("Capacite_etablissement_formation" as INT) as "Capacite_etablissement_formation",
	CAST("ET_C" as INT) as "ET_C", -- Entre 2018 et 2024, le type n'est pas toujours fixe entre 2018 et 2024 entre INT et FLOAT. Afin d'éviter toute incompatibilité, nous avons eu recourt à un CAST en INT de toutes les données numériques.
	CAST("ET_CF" as INT) as "ET_CF",
	CAST("ET_CP" as INT) as "ET_CP",
	CAST("ET_C_PP" as INT) as "ET_C_PP",
	CAST("EC_I" as INT) as "EC_I",
	CAST("EC_NB_G" as INT) as "EC_NB_G",
	CAST("EC_B_NB_G" as INT) as "EC_B_NB_G",
	CAST("EC_NB_T" as INT) as "EC_NB_T",
	CAST("EC_B_NB_T" as INT) as "EC_B_NB_T",
	CAST("EC_NB_P" as INT) as "EC_NB_P",
	CAST("EC_B_NB" as INT) as "EC_B_NB",
	CAST("EC_AC" as INT) as "EC_AC",
	CAST("ETC_PC" as INT) as "ETC_PC",
	CAST("EC_NB_G_PC" as INT) as "EC_NB_G_PC",
	CAST("EC_NB_T_PC" as INT) as "EC_NB_T_PC",
	CAST("EC_NB_P_PC" as INT) as "EC_NB_P_PC",
	CAST("EAC_PC" as INT) as "EAC_PC",
	CAST("ETC_CE" as INT) as "ETC_CE",
	CAST("EC_CE_PC" as INT) as "EC_CE_PC",
	CAST("EC_CE_I" as INT) as "EC_CE_I",
	CAST("EFC_CE_HI" as INT) as "EFC_CE_HI",
	CAST("EC_NBG_CE" as INT) as "EC_NBG_CE",
	CAST("EC_B_NB_CE" as INT) as "EC_B_NB_CE",
	CAST("EC_NB_T_CE" as INT) as "EC_NB_T_CE",
	CAST("EC_B_NB_T_CE" as INT) as "EC_B_NB_T_CE",
	CAST("EC_NBP_CE" as INT) as "EC_NBP_CE",
	CAST("EC_B_NB_P_CE" as INT) as "EC_B_NB_P_CE",
	CAST("EC_AC_CE" as INT) as "EC_AC_CE",
	CAST("ETC_R_PA" as INT) as "ETC_R_PA",
	CAST("Rang_dernier_appele" as INT) as "Rang_dernier_appele",
	CAST("ETC_A_PE" as INT) as "ETC_A_PE",
	CAST("EC_A" as INT) as "EC_A",
	CAST("EA_PP" as INT) as "EA_PP",
	CAST("EA_PC" as INT) as "EA_PC",
	CAST("EA_I" as INT) as "EA_I",
	CAST("EA_BN_B" as INT) as "EA_BN_B",
	CAST("EA_NB" as INT) as "EA_NB",
	CAST("EA_NB_G" as INT) as "EA_NB_G",
	CAST("EA_NB_T" as INT) as "EA_NB_T",
	CAST("EA_NB_P" as INT) as "EA_NB_P",
	CAST("EA_AC" as INT) as "EA_AC",
	CAST("EA_NB_SI" as INT) as "EA_NB_SI",
	CAST("EA_NB_SM" as INT) as "EA_NB_SM",
	CAST("EA_NB_AB" as INT) as "EA_NB_AB",
	CAST("EA_NB_B" as INT) as "EA_NB_B",
	CAST("EA_NB_TB" as INT) as "EA_NB_TB",
	CAST("EA_NB_G_M" as INT) as "EA_NB_G_M",
	CAST("EA_NB_T_M" as INT) as "EA_NB_T_M",
	CAST("EA_NB_P_M" as INT) as "EA_NB_P_M",
	CAST("EA_NB_IME" as INT) as "EA_NB_IME",
	CAST("EA_F_IME" as INT) as "EA_F_IME",
	CAST("EA_IMA" as INT) as "EA_IMA",
	CAST("EA_IMA_PCV" as INT) as "EA_IMA_PCV",
	CAST("PA_F" as INT) as "PA_F",
	CAST("PA_NB_IMA" as INT) as "PA_NB_IMA",
	CAST("PA_NB_IMA_PCV" as INT) as "PA_NB_IMA_PCV",
	CAST("PA_NB_IME" as INT) as "PA_NB_IME",
	CAST("PA_NB_B" as INT) as "PA_NB_B",
	CAST("PA_NB" as INT) as "PA_NB",
	CAST("PA_NB_SI_MB" as INT) as "PA_NB_SI_MB",
	CAST("PA_NB_SM_B" as INT) as "PA_NB_SM_B",
	CAST("PA_NB_AB" as INT) as "PA_NB_AB",
	CAST("PA_NB_B_MB" as INT) as "PA_NB_B_MB", 
	CAST("PA_NB_TB" as INT) as "PA_NB_TB",
	CAST("PA_NB_G" as INT) as "PA_NB_G",
	CAST("PA_M" as INT) as "PA_M",
	CAST("PA_NB_T" as INT) as "PA_NB_T",
	CAST("PA_M_BT" as INT) as "PA_M_BT",
	CAST("PA_NB_P" as INT) as "PA_NB_P",
	CAST("PA_M_BP" as INT) as "PA_M_BP",
	TRIM("tri") as "Tri"
FROM
    parcoursup2018
);




-- Création de la table temporaire parcourusp2024 et transformation des données : suppression des espaces et normalisation


CREATE TABLE TMP_parcoursup2024 AS (
SELECT
    CAST("Annee" as INT) as "Annee",
	TRIM("Statut_etablissement_filière_formation") as "Statut_etablissement_filière_formation",
	TRIM("Code_UAI") as "Code_UAI",
	CASE 
		WHEN TRIM("Etablissement") = '3il' THEN '3IL' 
		ELSE TRIM(INITCAP("Etablissement"))	
	END AS "Etablissement",
	CASE 
		WHEN TRIM(INITCAP("Departement_etablissement")) = 'Corse-Du-Sud' then '2A'
		WHEN TRIM(INITCAP("Departement_etablissement")) = 'Haute-Corse' then '2B'
		WHEN TRIM("Commune_etablissement") = 'Sarrola-Carcopino' THEN '2A'
        WHEN TRIM("Commune_etablissement") = 'Borgo' THEN '2B'
		ELSE TRIM(CAST("Code_departemental_etablissement" as VARCHAR(100)))
	END AS "Code_departemental_etablissement", -- Disparition des codes départementaux de Corse au profit de "20" ou d'une cellule vide. Alignement forcé sur 2018 pour la cohérence des données.
	CASE 
		WHEN TRIM("Commune_etablissement") = 'Sarrola-Carcopino' THEN 'Corse-Du-Sud'
        WHEN TRIM("Commune_etablissement") = 'Borgo' THEN 'Haute-Corse'
		WHEN TRIM(INITCAP("Departement_etablissement")) = 'Corse Du Sud' THEN 'Corse-Du-Sud'
		ELSE TRIM(INITCAP("Departement_etablissement"))
	END AS "Departement_etablissement", -- Les départements de Corse ont disparus au profit de "Corse". Pour éviter une incompabilité, nous avons normalisé cela.
    CASE
        WHEN TRIM("Region_etablissement") = 'Auvergne-Rhône-Alpes' THEN 'Auvergne-Rhône-Alpes'
        WHEN TRIM("Region_etablissement") = 'Bourgogne-Franche-Comté' THEN 'Bourgogne-Franche-Comté'
        WHEN TRIM("Region_etablissement") = 'Bretagne' THEN 'Bretagne'
        WHEN TRIM("Region_etablissement") = 'Centre-Val de Loire' THEN 'Centre-Val-de-Loire'
		WHEN TRIM("Region_etablissement") = 'Centre' THEN 'Centre-Val-de-Loire'
        WHEN TRIM("Region_etablissement") = 'Grand Est' THEN 'Grand-Est'
        WHEN TRIM("Region_etablissement") = 'Hauts-de-France' THEN 'Hauts-de-France'
        WHEN TRIM("Region_etablissement") = 'Île-de-France' THEN 'Île-de-France'
        WHEN TRIM("Region_etablissement") = 'Normandie' THEN 'Normandie'
        WHEN TRIM("Region_etablissement") = 'Nouvelle Aquitaine' THEN 'Nouvelle-Aquitaine'
        WHEN TRIM("Region_etablissement") = 'Occitanie' THEN 'Occitanie'
        WHEN TRIM("Region_etablissement") = 'Pays de la Loire' THEN 'Pays-de-la-Loire'
        WHEN TRIM("Region_etablissement") = 'Provence-Alpes-Côte d''Azur' THEN 'Provence-Alpes-Côte-d''Azur'
        WHEN TRIM("Region_etablissement") = 'Guadeloupe' THEN 'Guadeloupe'
        WHEN TRIM("Region_etablissement") = 'Martinique' THEN 'Martinique'
        WHEN TRIM("Region_etablissement") = 'Guyane' THEN 'Guyane'
		WHEN TRIM("Region_etablissement") = 'Réunion' THEN 'La Réunion' 
        WHEN TRIM("Region_etablissement") = 'Mayotte' THEN 'Mayotte'
		WHEN TRIM("Academie_etablissement") = 'Etranger' THEN 'Etranger'
		WHEN TRIM("Academie_etablissement") = 'Polynésie Française' THEN 'Polynésie Française'
        ELSE TRIM("Region_etablissement")
    END as "Region_etablissement" , -- Permet de s'assurer que l'on a les mêmes régions présentes aux mêmes endroits dans nos deux jeux de données.
	TRIM("Academie_etablissement") as "Academie_etablissement",
	TRIM("Commune_etablissement") as "Commune_etablissement",
	TRIM("Filiere_formation") as "Filiere_formation",
	cast(case -- Création d'un booléen au lieu d'un Varchar. 
		when "Selectivite" = 'formation sélective' then true
		else false
	end as BOOLEAN) as "Selectivite",
	TRIM("Filiere_formation_tres_agregee") as "Filiere_formation_tres_agregee",
	TRIM("Filiere_formation detaillee") as "Filiere_formation_Detaillee",
	TRIM("Filiere_formation_agregee") as "Filiere_formation_agregee", 
	TRIM("Filiere_formation_detaillee_bis") as "Filiere_formation_detaillee_bis",
	TRIM("Filiere_formation_détaillée") as "Filiere_formation_détaillée",
	TRIM("Coordonnees_GPS_formation") as "Coordonnees_gps_formation",
	CAST("Capacite_etablissement_formation" as INT) as "Capacite_etablissement_formation",
	CAST("ET_C" as INT) as "ET_C", -- Entre 2018 et 2024, le type n'est pas toujours fixe entre 2018 et 2024 entre INT et FLOAT. Afin d'éviter toute incompatibilité, recourt à un CAST manuel en INT de toutes les données numériques.
	CAST("ET_CF" as INT) as "ET_CF",
	CAST("ET_C_PP" as INT) as "ET_C_PP",
	CAST("EC_I" as INT) as "EC_I",
	CAST("EC_NB_G" as INT) as "EC_NB_G",
	CAST("EC_B_NB_G" as INT) as "EC_B_NB_G",
	CAST("EC_NB_T" as INT) as "EC_NB_T",
	CAST("EC_B_NB_T" as INT) as "EC_B_NB_T",
	CAST("EC_NB_P" as INT) as "EC_NB_P",
	CAST("EC_B_NB" as INT) as "EC_B_NB",
	CAST("EC_AC" as INT) as "EC_AC",
	CAST("ETC_PC" as INT) as "ETC_PC",
	CAST("EC_NB_G_PC" as INT) as "EC_NB_G_PC",
	CAST("EC_NB_T_PC" as INT) as "EC_NB_T_PC",
	CAST("EC_NB_P_PC" as INT) as "EC_NB_P_PC",
	CAST("EAC_PC" as INT) as "EAC_PC",
	CAST("ETC_CE" as INT) as "ETC_CE",
	CAST("EC_CE_PC" as INT) as "EC_CE_PC",
	CAST("EC_CE_I" as INT) as "EC_CE_I",
	CAST("EFC_CE_HI" as INT) as "EFC_CE_HI",
	CAST("EC_NB_CE" as INT) as "EC_NB_CE",
	CAST("EC_B_NB_CE" as INT) as "EC_B_NB_CE",
	CAST("EC_NB_T_CE" as INT) as "EC_NB_T_CE",
	CAST("EC_B_NB_T_CE" as INT) as "EC_B_NB_T_CE",
	CAST("EC_NB_P_CE" as INT) as "EC_NB_P_CE",
	CAST("EC_B_NB_P_CE" as INT) as "EC_B_NB_P_CE",
	CAST("EC_AC_CE" as INT) as "EC_AC_CE",
	CAST("ETC_R_PA" as INT) as "ETC_R_PA",
	CAST("ETC_A_PE" as INT) as "ETC_A_PE",
	CAST("ETC_F_A_PE" as INT) as "ETC_F_A_PE",
	CAST("EA_PP" as INT) as "EA_PP",
	CAST("EA_PC" as INT) as "EA_PC",
	CAST("EA_PA_OP" as INT) as "EA_PA_OP",
	CAST("EA_PA_AB" as INT) as "EA_PA_AB",
	CAST("EA_PA_PP" as INT) as "EA_PA_PP",
	CAST("EA_I" as INT) as "EA_I",
	CAST("EA_BN_B" as INT) as "EA_BN_B",
	CAST("EA_NB" as INT) as "EA_NB",
	CAST("EA_NB_G" as INT) as "EA_NB_G",
	CAST("EA_NB_T" as INT) as "EA_NB_T",
	CAST("EA_NB_P" as INT) as "EA_NB_P",
	CAST("EA_AC" as INT) as "EA_AC",
	CAST("EA_NB_SI" as INT) as "EA_NB_SI",
	CAST("EA_NB_SM" as INT) as "EA_NB_SM",
	CAST("EA_NB_AB" as INT) as "EA_NB_AB",
	CAST("EA_NB_B" as INT) as "EA_NB_B",
	CAST("EA_NB_TB" as INT) as "EA_NB_TB",
	CAST("EA_NB_TBF" as INT) as "EA_NB_TBF",
	CAST("EA_NB_G_M" as INT) as "EA_NB_G_M",
	CAST("EA_NB_T_M" as INT) as "EA_NB_T_M",
	CAST("EA_NB_P_M" as INT) as "EA_NB_P_M",
	CAST("EA_NB_IME" as INT) as "EA_NB_IME",
	CAST("EA_F_IME" as INT) as "EA_F_IME",
	CAST("EA_IMA" as INT) as "EA_IMA",
	CAST("EA_IMA_PCV" as INT) as "EA_IMA_PCV",
	CAST("PA_OP_PP" as INT) as "PA_OP_PP",
	CAST("PA_AB" as INT) as "PA_AB",
	CAST("PA_AF_PP" as INT) as "PA_AF_PP",
	CAST("PA_F" as INT) as "PA_F",
	CAST("PA_NB_IMA" as INT) as "PA_NB_IMA",
	CAST("PA_NB_IMA_PCV" as INT) as "PA_NB_IMA_PCV",
	CAST("PA_NB_IME" as INT) as "PA_NB_IME",
	CAST("PA_NB_B" as INT) as "PA_NB_B",
	CAST("PA_NB" as INT) as "PA_NB",
	CAST("PA_NB_SI_MB" as INT) as "PA_NB_SI_MB",
	CAST("PA_NB_SM" as INT) as "PA_NB_SM",
	CAST("PA_NB_AB" as INT) as "PA_NB_AB",
	CAST("PA_NB_B_MB" as INT) as "PA_NB_B_MB", 
	CAST("PA_NB_TB" as INT) as "PA_NB_TB",
	CAST("PA_NB_TB_F" as INT) as "PA_NB_TB_F",
	CAST("PA_NB_G" as INT) as "PA_NB_G",
	CAST("PA_M_BG" as INT) as "PA_M_BG",
	CAST("PA_NB_T" as INT) as "PA_NB_T",
	CAST("PA_M_BT" as INT) as "PA_M_BT",
	CAST("PA_NB_P" as INT) as "PA_NB_P",
	CAST("PA_M_BP" as INT) as "PA_M_BP",
	CAST("EC_TG_PA_E" as INT) as "EC_TG_PA_E",
	CAST("EC_B_TG_PA_E" as INT) as "EC_B_TG_PA_E",
	CAST("EC_TT_PA_E" as INT) as "EC_TT_PA_E",
	CAST("EC_B_TT_PA_E" as INT) as "EC_B_TT_PA_E",
	CAST("EC_TP_PA_E" as INT) as "EC_TP_PA_E",
	CAST("EC_B_TP_PA_E" as INT) as "EC_B_TP_PA_E",
	CAST("EAC_PA_E" as INT) as "EAC_PA_E",
	TRIM("Regroupement_1_par_formations_pour_classements") as "Regroupement_1_par_formations_pour_classements",
	CAST("Rang_dernier_appele_groupe 1" as INT) as "Rang_dernier_appele_groupe_1",
	TRIM("Regroupement_2_par_formations_pour_classements") as "Regroupement_2_par_formations_pour_classements",
	CAST("Rang_dernier_appele_groupe_2" as INT) as "Rang_dernier_appele_groupe_2",
	TRIM("Regroupement_3_par_formations_pour_classements") as "Regroupement_3_par_formations_pour_classements",
	CAST("Rang_dernier_appele_groupe_3" as INT) as "Rang_dernier_appele_groupe_3",
	TRIM("list_com") as "List_com",
	TRIM("tri") as "Tri",
	CAST("cod_aff_form" as INT) as "Cod_aff_form",
	TRIM("Concours_communs_banque_epreuves") as "Concours_communs_banque_epreuves",
	TRIM("Lien_formation_Parcoursup") as "Lien_formation_parcoursup",
	CAST("Taux_acces" as INT) as "Taux_acces",
	CAST("Part _terminales_generales_pouvant_recevoir_proposition_phase_principale" as INT) as "Part__terminales_generales_pouvant_recevoir_proposition_phase_principale",
	CAST("Part_terminales_technologiques_pouvant_recevoir_proposition_phase_principale" as INT) as "Part_terminales_technologiques_pouvant_recevoir_proposition_phase_principale",
	CAST("Part_ terminales_professionnelles_pouvant_recevoir_proposition_phase principale" as INT) as "Part__Terminales_professionnelles_pouvant_recevoir_proposition_phase_Principale",
	TRIM("etablissement_id_paysage") as "Etablissement_id_paysage",
	TRIM("composante_id_paysage") as "Composante_id_paysage"
FROM
    parcoursup2024
);




-- Création de la table temporaire pour la population par région en 2024 (1er enrichissement)

CREATE TABLE TMP_resultat_pivot_2024 AS (
SELECT
    TRIM(CAST("dep" AS VARCHAR(3))) AS "dep",
    TRIM("sexe") AS "sexe",
    CAST(2024 AS  VARCHAR(4)) AS "annee",  -- Valeur essentielle mais non existante à l'origine. Ont ajoute la colonne avec une valeur fixe "2024".
    CAST("0 à 4 ans" AS INT) AS "age_0_4",
    CAST("5 à 9 ans" AS INT) AS "age_5_9",
    CAST("10 à 14 ans" AS INT) AS "age_10_14",
    CAST("15 à 19 ans" AS INT) AS "age_15_19",
    CAST("20 à 24 ans" AS INT) AS "age_20_24",
    CAST("25 à 29 ans" AS INT) AS "age_25_29",
    CAST("30 à 34 ans" AS INT) AS "age_30_34",
    CAST("35 à 39 ans" AS INT) AS "age_35_39",
    CAST("40 à 44 ans" AS INT) AS "age_40_44",
    CAST("45 à 49 ans" AS INT) AS "age_45_49",
    CAST("50 à 54 ans" AS INT) AS "age_50_54",
    CAST("55 à 59 ans" AS INT) AS "age_55_59",
    CAST("60 à 64 ans" AS INT) AS "age_60_64",
    CAST("65 à 69 ans" AS INT) AS "age_65_69",
    CAST("70 à 74 ans" AS INT) AS "age_70_74",
    CAST("75 à 79 ans" AS INT) AS "age_75_79",
    CAST("80 ans et plus" AS INT) AS "age_80_plus"
FROM
    resultat_pivot_2024
);


-- Creation de table temporaire pour la population par région en 2018 (1er croisement)

CREATE TABLE TMP_resultat_pivot_2018 AS (
SELECT
    TRIM(CAST("dep" AS VARCHAR(3))) AS "dep",
    TRIM("sexe") AS "sexe",
    CAST(2018 AS VARCHAR(4)) AS "annee",  -- Valeur essentielle mais non existante à l'origine. Ont ajoute la colonne avec une valeur fixe "2018".
    CAST("0 à 4 ans" AS INT) AS "age_0_4",
    CAST("5 à 9 ans" AS INT) AS "age_5_9",
    CAST("10 à 14 ans" AS INT) AS "age_10_14",
    CAST("15 à 19 ans" AS INT) AS "age_15_19",
    CAST("20 à 24 ans" AS INT) AS "age_20_24",
    CAST("25 à 29 ans" AS INT) AS "age_25_29",
    CAST("30 à 34 ans" AS INT) AS "age_30_34",
    CAST("35 à 39 ans" AS INT) AS "age_35_39",
    CAST("40 à 44 ans" AS INT) AS "age_40_44",
    CAST("45 à 49 ans" AS INT) AS "age_45_49",
    CAST("50 à 54 ans" AS INT) AS "age_50_54",
    CAST("55 à 59 ans" AS INT) AS "age_55_59",
    CAST("60 à 64 ans" AS INT) AS "age_60_64",
    CAST("65 à 69 ans" AS INT) AS "age_65_69",
    CAST("70 à 74 ans" AS INT) AS "age_70_74",
    CAST("75 à 79 ans" AS INT) AS "age_75_79",
    CAST("80 ans et plus" AS INT) AS "age_80_plus"
FROM
    resultat_pivot_2018
);



--création d'une table temporaire à partir du csv sur le revenu fiscal de reference (2ème croisement)


CREATE TABLE TMP_revenu_fiscal_reference AS
SELECT
    CASE --case pour normaliser les codes départements et qu'ils soient les mêmes que dans la table département à venir.
    WHEN TRIM(CAST("Dép." AS VARCHAR)) IN ('971', '972', '973', '974', '976') 
        THEN TRIM(CAST("Dép." AS VARCHAR))
    -- Corse
    WHEN TRIM(CAST("Dép." AS VARCHAR)) = '2A0' THEN '2A'
    WHEN TRIM(CAST("Dép." AS VARCHAR)) = '2B0' THEN '2B'
    -- Paris arrondissements → 75
    WHEN TRIM(CAST("Dép." AS VARCHAR)) IN ('754', '755', '756', '757', '758') THEN '75'
    -- Petite couronne arrondissements
    WHEN TRIM(CAST("Dép." AS VARCHAR)) IN ('921', '922') THEN '92'
    WHEN TRIM(CAST("Dép." AS VARCHAR)) = '930' THEN '93'
    WHEN TRIM(CAST("Dép." AS VARCHAR)) = '940' THEN '94'
    WHEN TRIM(CAST("Dép." AS VARCHAR)) = '950' THEN '95'
    -- Bouches-du-Rhône et Nord
	WHEN TRIM(CAST("Dép." AS VARCHAR)) IN ('131', '132') THEN '13'
	WHEN TRIM(CAST("Dép." AS VARCHAR)) IN ('591', '592') THEN '59'
    -- Non-résidents : exclusion
    WHEN TRIM(CAST("Dép." AS VARCHAR)) = 'B31' THEN NULL
    -- Cas général : suppression du zéro final
    WHEN RIGHT(TRIM(CAST("Dép." AS VARCHAR)), 1) = '0'
        THEN LEFT(TRIM(CAST("Dép." AS VARCHAR)), LENGTH(TRIM(CAST("Dép." AS VARCHAR))) - 1)
    ELSE TRIM(CAST("Dép." AS VARCHAR))
END AS "Code_departement",
    TRIM(CAST("Revenu fiscal de référence par tranche (en euros)" AS VARCHAR)) AS "Tranche_revenus",
    SUM(
        CAST(NULLIF(TRIM(CAST("Nombre de foyers fiscaux" AS VARCHAR)), 'n.c.') AS INT)
    )                                                                      AS "Nombre_foyers_fiscaux",
    SUM(
        CAST(NULLIF(TRIM(CAST("Revenu fiscal de référence des foyers fiscaux" AS VARCHAR)), 'n.c.') AS BIGINT)
    )                                                                      AS "Revenu_fiscal_reference_milliers",
    SUM(
        CAST(NULLIF(TRIM(CAST("Nombre de foyers fiscaux imposés" AS VARCHAR)), 'n.c.') AS INT)
    )                                                                      AS "Nombre_foyers_imposes",
    SUM(
        CAST(NULLIF(TRIM(CAST("Revenu fiscal de référence des foyers fiscaux imposés" AS VARCHAR)), 'n.c.') AS BIGINT)
    )                                                                      AS "Revenu_fiscal_reference_imposes_milliers"
FROM revenu_fiscal_reference

WHERE TRIM(CAST("Commune" AS VARCHAR)) NOT IN ('', ' ')
  AND TRIM(CAST("Commune" AS VARCHAR)) IS NOT NULL
  AND TRIM(CAST("Dép." AS VARCHAR)) != 'B31'  -- ← exclure les non-résidents
GROUP BY
    CASE
        WHEN TRIM(CAST("Dép." AS VARCHAR)) IN ('971', '972', '973', '974', '976') 
            THEN TRIM(CAST("Dép." AS VARCHAR))
        WHEN TRIM(CAST("Dép." AS VARCHAR)) = '2A0' THEN '2A'
        WHEN TRIM(CAST("Dép." AS VARCHAR)) = '2B0' THEN '2B'
        WHEN TRIM(CAST("Dép." AS VARCHAR)) IN ('754', '755', '756', '757', '758') THEN '75'
        WHEN TRIM(CAST("Dép." AS VARCHAR)) IN ('921', '922') THEN '92'
        WHEN TRIM(CAST("Dép." AS VARCHAR)) = '930' THEN '93'
        WHEN TRIM(CAST("Dép." AS VARCHAR)) = '940' THEN '94'  -- ← corrigé
        WHEN TRIM(CAST("Dép." AS VARCHAR)) = '950' THEN '95'
        WHEN TRIM(CAST("Dép." AS VARCHAR)) IN ('131', '132') THEN '13'
		WHEN TRIM(CAST("Dép." AS VARCHAR)) IN ('591', '592') THEN '59'
        WHEN TRIM(CAST("Dép." AS VARCHAR)) = 'B31' THEN NULL
        WHEN RIGHT(TRIM(CAST("Dép." AS VARCHAR)), 1) = '0'
            THEN LEFT(TRIM(CAST("Dép." AS VARCHAR)), LENGTH(TRIM(CAST("Dép." AS VARCHAR))) - 1)
        ELSE TRIM(CAST("Dép." AS VARCHAR))
    END,
    TRIM(CAST("Revenu fiscal de référence par tranche (en euros)" AS VARCHAR))
ORDER BY
    "Code_departement",
    "Tranche_revenus";


-- Création de la table temporaire sur les IPS des lycée (3ème croisement)

CREATE TABLE TMP_IPS_Lycee_College AS (
SELECT
TRIM("Rentrée scolaire") as "Session",
CAST("Code région" as INT) as "Région_id",
TRIM(INITCAP("Région académique")) as "région",
CAST("Code académie" as INT) as "Académie_id",
TRIM(INITCAP("Académie")) as "Académie",
TRIM("Code du département") as "Département_id",
TRIM(INITCAP("Département")) as "Département",
TRIM(INITCAP("Nom de la commune")) as "Commune_nom",
TRIM("UAI") as "Code_UAI",
TRIM(INITCAP("Nom de l'établissement")) as "Etablissement_nom",
case
	when("Secteur") = 'public' then 'Public'
	when("Secteur") = 'privé sous contrat' then 'Privé sous contrat d''association'
end as "Statut",
TRIM("Type de lycée") as "Type_lycée",  
CASE WHEN CAST("IPS voie GT" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS voie GT" AS FLOAT) ELSE NULL END as "IPS_LEGT", -- Utilisation d'une regex qui permet de forcer du "null" dans les colonnes float. Permet de remplacer les vides de notre csv sans entrer de données erronnées.
CASE WHEN CAST("IPS voie PRO" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS voie PRO" AS FLOAT) ELSE NULL END as "IPS_PRO",
CASE WHEN CAST("IPS post BAC" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS post BAC" AS FLOAT) ELSE NULL END as "IPS_Post_BAC",
CASE WHEN CAST("IPS de l'établissement" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS de l'établissement" AS FLOAT) ELSE NULL END as "IPS_Etablissement",
CASE WHEN CAST("Ecart type voie GT" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("Ecart type voie GT" AS FLOAT) ELSE NULL END as "Ecart_Type_GT",
CASE WHEN CAST("Ecart type voie PRO" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("Ecart type voie PRO" AS FLOAT) ELSE NULL END as "Ecart_Type_PRO",
CASE WHEN CAST("Ecart-type établissement" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("Ecart-type établissement" AS FLOAT) ELSE NULL END as "Ecart_Type_Etablissement",
CASE WHEN CAST("IPS national LEGT" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS national LEGT" AS FLOAT) ELSE NULL END as "IPS_National",
CASE WHEN CAST("IPS national LPO" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS national LPO" AS FLOAT) ELSE NULL END as "IPS_National_LGPO",
CASE WHEN CAST("IPS national LP" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS national LP" AS FLOAT) ELSE NULL END as "IPS_National_LP",
CASE WHEN CAST("IPS national LEGT privé" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS national LEGT privé" AS FLOAT) ELSE NULL END as "IPS_National_LEGT_Prive",
CASE WHEN CAST("IPS national LEGT public" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS national LEGT public" AS FLOAT) ELSE NULL END as "IPS_National_LEGT_Public",
CASE WHEN CAST("IPS national LPO privé" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS national LPO privé" AS FLOAT) ELSE NULL END as "IPS_National_LPO_Prive",
CASE WHEN CAST("IPS national LPO public" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS national LPO public" AS FLOAT) ELSE NULL END as "IPS_National_LPO_Public",
CASE WHEN CAST("IPS national LP privé" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS national LP privé" AS FLOAT) ELSE NULL END as "IPS_National_LP_Prive",
CASE WHEN CAST("IPS national LP public" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS national LP public" AS FLOAT) ELSE NULL END as "IPS_National_LP_Public",
CASE WHEN CAST("IPS académique LEGT" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS académique LEGT" AS FLOAT) ELSE NULL END as "IPS_Academique_LEGT",
CASE WHEN CAST("IPS académique LPO" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS académique LPO" AS FLOAT) ELSE NULL END as "IPS_Academique_LPO",
CASE WHEN CAST("IPS académique LP" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS académique LP" AS FLOAT) ELSE NULL END as "IPS_Academique_LP",
CASE WHEN CAST("IPS académique LEGT privé" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS académique LEGT privé" AS FLOAT) ELSE NULL END as "IPS_Academique_LEGT_Prive",
CASE WHEN CAST("IPS académique LEGT public" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS académique LEGT public" AS FLOAT) ELSE NULL END as "IPS_Academique_LEGT_Public",
CASE WHEN CAST("IPS académique LPO privé" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS académique LPO privé" AS FLOAT) ELSE NULL END as "IPS_Academique_LPO_Prive",
CASE WHEN CAST("IPS académique LPO public" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS académique LPO public" AS FLOAT) ELSE NULL END as "IPS_Academique_LPO_Public",
CASE WHEN CAST("IPS académique LP privé" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS académique LP privé" AS FLOAT) ELSE NULL END as "IPS_Academique_LP_Prive",
CASE WHEN CAST("IPS académique LP public" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS académique LP public" AS FLOAT) ELSE NULL END as "IPS_Academique_LP_Public",
CASE WHEN CAST("IPS départemental LEGT" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS départemental LEGT" AS FLOAT) ELSE NULL END as "IPS_Departemental_LEGT",
CASE WHEN CAST("IPS départemental LPO" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS départemental LPO" AS FLOAT) ELSE NULL END as "IPS_Departemental_LPO",
CASE WHEN CAST("IPS départemental LP" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS départemental LP" AS FLOAT) ELSE NULL END as "IPS_Départemental_LP",
CASE WHEN CAST("IPS départemental LEGT privé" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS départemental LEGT privé" AS FLOAT) ELSE NULL END as "IPS_Departemental_LEGT_Prive",
CASE WHEN CAST("IPS départemental LEGT public" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS départemental LEGT public" AS FLOAT) ELSE NULL END as "IPS_Departemental_LEGT_Public",
CASE WHEN CAST("IPS départemental LPO privé" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS départemental LPO privé" AS FLOAT) ELSE NULL END as "IPS_Departemental_LPO_Prive",
CASE WHEN CAST("IPS départemental LPO public" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS départemental LPO public" AS FLOAT) ELSE NULL END as "IPS_Departemental_LPO_Public",
CASE WHEN CAST("IPS départemental LP privé" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS départemental LP privé" AS FLOAT) ELSE NULL END as "IPS_Departemental_LP_Prive",
CASE WHEN CAST("IPS départemental LP public" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("IPS départemental LP public" AS FLOAT) ELSE NULL END as "IPS_Departemental_LP_Public",
CASE WHEN CAST("num_ligne" AS TEXT) ~ '^-?[0-9]+(\.[0-9]+)?$' THEN CAST("num_ligne" AS FLOAT) ELSE NULL END as "Num_Ligne"
FROM 
    lycee
);

COMMIT;
