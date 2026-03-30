## Comparaison des taux de boursiers par formation

La page de comparaison permet de mettre en regard jusqu'à cinq formations sur la question de l'accès des étudiants boursiers, en comparant les données Parcoursup de 2018 et 2024. Elle s'organise en deux zones : un volet de filtres sur la gauche et une zone de visualisation sur la droite.

### Volet de filtres

Le volet de filtres permet à l'utilisateur de constituer sa sélection de formations. Les formations y sont présentées dans une liste déroulante organisée par établissement, ce qui permet de naviguer facilement parmi les milliers de formations disponibles sans être confronté à des doublons de noms. L'utilisateur peut ajouter jusqu'à cinq formations à comparer en cliquant sur le bouton **« Ajouter une formation »**, et supprimer chaque ligne individuellement. Un résumé s'actualise en temps réel au fil des sélections, et le bouton **« Générer »** reste désactivé tant qu'aucune formation n'a été choisie. Une fois la visualisation lancée, le volet se rétracte automatiquement pour laisser la place aux graphiques, et peut être rouvert à tout moment via une flèche latérale.

### Visualisation et synthèse

Pour chaque formation sélectionnée, le graphique affiche côte à côte quatre barres :

- le **pourcentage de candidats boursiers** en 2018
- le **pourcentage d'admis boursiers** en 2018
- le **pourcentage de candidats boursiers** en 2024
- le **pourcentage d'admis boursiers** en 2024

Ce format permet de visualiser simultanément l'évolution temporelle (2018 a 2024) et l'écart de sélectivité entre candidats et admis au sein d'une même formation. Les pourcentages sont calculés en agrégeant les effectifs des filières baccalauréat général, technologique et professionnel.

Un résumé textuel accompagne systématiquement le graphique et détaille, pour chaque formation, les effectifs exacts de candidats et d'admis ainsi que les pourcentages de boursiers correspondants pour les deux années. Lorsqu'une formation ne dispose pas de données pour l'une des deux années, cela est signalé explicitement dans le résumé par un avertissement et indiqué sur le graphique par la mention **n/d**.

### Architecture

Côté utilisateur, un fichier JavaScript (`comparaison.js`) gère l'interface de filtrage et envoie au serveur, via une requête `fetch` en POST, un objet JSON contenant les identifiants des formations sélectionnées. Côté serveur, Flask reçoit cette requête et orchestre deux types d'accès à la base de données PostgreSQL.

Pour charger la liste des formations et des établissements affichés dans le volet de filtres, le code utilise l'ORM SQLAlchemy via les modèles `Formation` et `Etablissement` déjà définis dans le projet. Ces modèles permettent d'écrire des requêtes en Python pur :

```python
Formation.query.filter_by(etablissement_id=etab.id).order_by(Formation.nom).all()
```

sans écrire de SQL, SQLAlchemy se chargeant de la traduction. Pour le calcul des indicateurs statistiques en revanche, la complexité des agrégations (sommes conditionnelles sur plusieurs colonnes, jointure entre les tables `candidatures` et `admissions`, filtre sur les années) rend le SQL brut plus lisible et plus précis. Ces requêtes sont donc écrites directement en SQL et exécutées via `db.session.execute(text(...))`, la session SQLAlchemy garantissant la sécurité des paramètres contre les injections SQL grâce aux paramètres nommés (`:formation_id`) :

```sql
SELECT
    ca.annee,
    SUM(ca.ec_b_nb_g + ca.ec_b_nb_t + ca.ec_b_nb) AS num_cand,
    SUM(ca.ec_nb_g + ca.ec_nb_t + ca.ec_nb_p)      AS den_cand,
    SUM(ad.ea_bn_b)                                 AS num_adm,
    SUM(ad.ea_nb_g + ad.ea_nb_t + ad.ea_nb_p)      AS den_adm
FROM "ParcourStat".candidatures ca
JOIN "ParcourStat".admissions ad
  ON ad.formation_id = ca.formation_id
 AND ad.annee = ca.annee
WHERE ca.formation_id = :formation_id
  AND ca.annee IN (2018, 2024)
GROUP BY ca.annee
```

Les résultats sont ensuite traités en Python pour calculer les pourcentages et construire les phrases de la synthèse textuelle, puis le graphique est généré avec **Matplotlib** et encodé en base64 pour être transmis au navigateur dans la réponse JSON. Le JavaScript n'a alors plus qu'à insérer l'image reçue dans un élément `<img>` et afficher les blocs de synthèse, sans aucune logique de calcul ou de visualisation du cote de l'utilisateur.
