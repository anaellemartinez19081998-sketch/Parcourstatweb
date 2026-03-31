-- Début de la transaction
BEGIN;

-- Toujours utiliser le même schéma
CREATE SCHEMA IF NOT EXISTS "ParcourStat";
SET search_path TO "ParcourStat";


-- Création d'une vue permettant de montrer le nombre de formation par région. 
-- Cela permet de créer une première connaissance : la répartition inégale de l'accès à la formation supérieure dû à la concentration des formations en île de France et à la rareté de ces formations notamment dans les Territoires d'Outre Mer et les lieux d'expatriation.

create view nombre_formation_par_region as  
	select r.nom as region, count(f.id ) as nbr_formation 
	from region r
	join departement d on r.id = d.region_id 
	join commune c on d.code = c.departement_id 
	join etablissement e on c.id = e.commune_id 
	join formation f on e.id = f.etablissement_id 
	group by r.nom 
	order by nbr_formation DESC;






-- Création d'une vue permettant de montrer le taux d'acceptation des filles dans les disciplines en combinant 2018 et 2024. 

create view taux_filles_acceptées_par_disciplines as 
	select d.nom as discipline, AVG(a.pa_f) as taux_acceptation_candidates
	from admissions a 
	join formation f on a.formation_id = f.id 
	join discipline d on f.discipline_id = d.id 
	GROUP BY discipline 
	order by taux_acceptation_candidates DESC;






-- Création d'une vue permettant de montrer le nombre moyen de boursiers admis par région.
-- Elle permet d'identifier les régions qui accueillent le plus de boursiers et celles qui en accueillent le moins.
-- Cela crée de la connaissance autour du taux d'accessibilité sociale de chaque région.
-- Toutefois, elle reste limitée puisqu'elle ne prend pas en compte le nombre de formations par régions, croisée avec le nombre de boursiers. Une région qui accueille un grand nombre de boursiers ne possède donc pas forcément une grande accessibilité sociale, mais peut avoir un grand nombre de formations.


create view boursiers_admis_regions as
select
   region.nom AS region,
   AVG(admissions.PA_NB_B) AS boursiers_admis
from admissions
join formation ON admissions.formation_id = formation.id
join etablissement ON formation.etablissement_id = etablissement.id
join commune ON etablissement.commune_id = commune.id
join departement ON commune.departement_id = departement.code
join region ON departement.region_id = region.id
group by region.nom;




--- Création d'une vue permettant de croiser le niveau de richesse des départements 
-- avec les caractéristiques des formations Parcoursup qui y sont proposées.
-- Elle permet d'identifier si les départements les plus riches proposent davantage
-- de formations sélectives, et inversement si les territoires moins favorisés
-- sont davantage orientés vers des formations non sélectives.

CREATE OR REPLACE VIEW VUE_simple_formations_richesse AS
SELECT
    dep.nom AS "Departement",
    dep.code AS "Code_departement",
    reg.nom AS "Region",
    r.revenu_moyen_par_foyer_euros AS "Revenu_moyen_par_foyer",
    r.taux_foyers_imposes_pct AS "Taux_foyers_imposes",
    f.nom AS "Nom_formation",
    f.selectivite AS "Selective",
    tt.nom AS "Type_formation"

FROM formation f
-- Remontée de la hiérarchie géographique : formation → établissement → commune → département → région
JOIN etablissement e 
ON f.etablissement_id = e.id
JOIN commune com 
ON e.commune_id = com.id
JOIN departement dep 
ON com.departement_id = dep.code
JOIN region reg 
ON dep.region_id = reg.id
-- Jointure avec les données fiscales IRCOM 2023
-- Le filtre sur 'Total' garantit une seule ligne par département
JOIN revenu_fiscal_reference_def r
ON r.code_departement = dep.code
AND r.tranche_revenus = 'Total'
-- LEFT JOIN car certaines formations peuvent ne pas avoir de type renseigné
-- On évite ainsi de perdre ces formations dans le résultat
LEFT JOIN discipline dt
ON dt.id = f.discipline_id
LEFT JOIN types_formations tt
ON tt.id = dt.type;






-- Création d'une vue permettant de croiser nos informations sur les admissions des boursiers et les IPS. 
-- Vue générale qui permet de comparer une analyses multi échelles et multi critère.

CREATE VIEW Boursiers_et_IPS as
SELECT
    e.id AS code_uai,
    e.nom AS nom_etablissement,
    il.ips_etablissement,
    il.ips_legt,
    il.ips_pro,
    il.typologie,
    a.ea_bn_b AS nb_admis_boursiers_neobac,
    a.ea_nb AS nb_admis_neobac_total,
    a.pa_nb_b AS pct_admis_neobac_boursiers,
    CASE 
        WHEN il.ips_etablissement < n.ips_national_legt THEN 'Sous la moyenne nationale'
        WHEN il.ips_etablissement > n.ips_national_legt THEN 'Au dessus de la moyenne nationale'
        ELSE 'Dans la moyenne nationale'
    END AS position_nationale,
    ROUND((il.ips_etablissement - n.ips_national_legt)::numeric, 2) AS ecart_ips_national,
    n.ips_national_legt AS ips_ref_nationale
FROM ips_lycee il
JOIN etablissement e ON e.id = il.code_uai
JOIN formation f ON f.etablissement_id = e.id
JOIN admissions a ON a.formation_id = f.id AND a.annee = 2024
CROSS JOIN ips_nationaux n
WHERE a.ea_bn_b IS NOT NULL
AND a.ea_nb > 0;






-- Création d'une vue s'appuyant sur la précédente. 
-- Elle permet une analyse plus précise à l'échelle de la région. 
-- Script créer dans l'optique d'une création d'une carte choroplète, dynamique et interactive sur Tableau.

CREATE VIEW ips_boursiers_region AS
WITH ips_region_agg AS (
    SELECT
        r.id AS region_id,
        r.nom AS region_nom,
        -- IPS moyen pondéré
        ROUND(
            SUM(a.ips_etablissement * a.nb_admis_neobac_total)::numeric
            / NULLIF(SUM(a.nb_admis_neobac_total), 0), 2
        ) AS ips_region_pondere,
        -- Effectifs boursiers
        SUM(a.nb_admis_boursiers_neobac) AS total_boursiers_admis,
        SUM(a.nb_admis_neobac_total) AS total_admis_neobac,
        -- Taux de boursiers
        ROUND(
            SUM(a.nb_admis_boursiers_neobac)::numeric
            / NULLIF(SUM(a.nb_admis_neobac_total), 0) * 100, 2
        ) AS taux_boursiers_region,
        -- Nombre d'établissements
        COUNT(DISTINCT a.code_uai) AS nb_etablissements
    FROM boursiers_et_ips a
    JOIN etablissement e ON e.id = a.code_uai
    JOIN commune c ON c.id = e.commune_id
    JOIN departement d ON d.code = c.departement_id
    JOIN region r ON r.id = d.region_id
    GROUP BY r.id, r.nom
)
SELECT
    *,
    -- Quintile pour la couleur (calculé après l'agrégation)
    NTILE(5) OVER (ORDER BY ips_region_pondere) AS quintile_ips,
    -- Écart à la moyenne nationale
    ROUND(ips_region_pondere - 118.5, 2) AS ecart_national
FROM ips_region_agg;



-- Creation d'une vue qui regroupe le nombre total d'admis par département et par année, et la population totale et la population des 15-19 ans
CREATE VIEW pop_admis_annee AS

SELECT
   -- Code du département
   d."code" AS "code_departement",

   -- Nom du département
   d."nom" AS "nom_departement",

   -- Année d'admission
   a."annee",

   -- Total des effectifs admis (ea_ac + ea_nb) ea_ac et ea_nb représentent deux types d'admissions
   SUM(a."ea_ac" + a."ea_nb") AS "total_ea",

   -- Population totale des 15-19 ans pour le département et l'année
   p."total_pop_15_19" AS "total_pop_15_19",

   -- Population totale tous âges confondus
   p."total_population" AS "total_population"

FROM admissions a

-- Jointure pour relier une admission à sa formation
JOIN formation f
   ON a."formation_id" = f."id"

-- Jointure pour relier la formation à l'établissement
JOIN etablissement e
   ON f."etablissement_id" = e."id"

-- Jointure pour relier l'établissement à la commune
JOIN commune c
   ON e."commune_id" = c."id"

-- Jointure pour relier la commune au département
JOIN departement d
   ON c."departement_id" = d."code"

-- Sous-requête qui agrège la population par département et par année
JOIN (
   SELECT
       "dep",

       -- Conversion explicite de l'année en entier
       CAST("annee" AS INT) AS "annee",

       -- Somme de la population des 15-19 ans
       SUM("age_15_19") AS "total_pop_15_19",

       -- Somme de toutes les tranches d'âge pour obtenir la population totale
       SUM(
           "age_0_4" + "age_5_9" + "age_10_14" + "age_15_19" + "age_20_24" +
           "age_25_29" + "age_30_34" + "age_35_39" + "age_40_44" + "age_45_49" +
           "age_50_54" + "age_55_59" + "age_60_64" + "age_65_69" + "age_70_74" +
           "age_75_79" + "age_80_plus"
       ) AS "total_population"

   FROM population

   -- Agrégation par département et par année
   GROUP BY "dep", "annee"

) p

-- Jointure entre la population agrégée et les admissions sur le département et l'année
ON p."dep" = d."code"
AND p."annee" = a."annee"

-- Regroupement nécessaire car on utilise SUM()
GROUP BY
   d."code",
   d."nom",
   a."annee",
   p."total_pop_15_19",
   p."total_population"

-- Tri des résultats par département puis par année
ORDER BY
   d."code",
   a."annee";

-- Validation finale de la transaction
COMMIT;


