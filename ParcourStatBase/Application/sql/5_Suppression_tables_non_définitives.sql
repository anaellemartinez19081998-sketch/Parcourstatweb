-- Ce script permet la destruction automatique des tables ayant servi à la construction de la Base de donnée.

BEGIN; 

drop table parcoursup2018;

drop table parcoursup2024;

drop table wikidata;

DROP TABLE resultat_pivot_2018;

DROP TABLE resultat_pivot_2024;

drop table revenu_fiscal_reference;

drop table lycee;

drop table tmp_parcoursup2018;

drop table tmp_parcoursup2024;

DROP TABLE TMP_resultat_pivot_2018;

DROP TABLE TMP_resultat_pivot_2024;

drop table TMP_revenu_fiscal_reference;

drop table TMP_IPS_Lycee_College;

COMMIT;