# Régression sur des données réelles

**Tags :** R, Excel, Word  
**Durée :** 2 semaines | **Groupe :** 2 personnes

## L'objectif
Déterminer le meilleur modèle de prédiction pour prédire le prix de vente des logements à Paris.

### La description du projet
Pour prédire la valeur foncière des biens immobiliers à Paris, nous disposions de 2 fichiers :  
- un fichier où il y avait les valeurs à prédire : "test"  
- un fichier d'entraînement, pour tester nos modèles : "train"  

Sur Excel, nous avons débuté ce projet en déterminant des catégories pour avoir un modèle par catégorie et tenter d'être le plus précis possible.  
Après avoir supprimé 10 % des biens les plus chers et les moins chers du fichier "train", nous avons séparé les maisons et les appartements, puis les appartements selon le nombre de pièces.  
Ensuite, nous avons subdivisé chaque catégorie en regroupant les logements par arrondissement et en calculant une moyenne des prix de vente.  
Nous avons testé les quatre modèles sur chaque catégorie pour déterminer le meilleur dans chaque cas.  
Notre conclusion a été que le modèle linéaire était le meilleur pour chaque catégorie.  

Pour appliquer nos modèles sur R et sur le fichier "test", nous avons reproduit la même répartition des logements et appliqué nos modèles pour prédire les valeurs foncières.  
Ensuite, nous avons rédigé un rapport détaillé expliquant notre démarche.

### L'évaluation
- La méthodologie utilisée pour élaborer le modèle et la profondeur des recherches menées  
- La complexité du modèle retenu  
- La qualité et la clarté du texte explicatif  
- La clarté et l'efficacité du code R permettant de créer le modèle retenu  
- La précision des prédictions, mesurée par la "somme des carrés des résidus" (SR²) et classement des meilleures prédictions

### Les compétences acquises
- Application des quatre modèles de régression simple  
- Application des modèles sur Excel et sur R  
- Expliquer sa démarche  

### Le bilan personnel
Ce projet m'a offert l'occasion de renforcer mes compétences en utilisant R.  
J'ai pu mettre en pratique l'application d'un modèle linéaire sur un cas concret et perfectionner mes capacités rédactionnelles pour exprimer clairement ma démarche et mes réflexions.  
Ce projet était une sorte de mini-compétition au sein de la promotion, visant à obtenir la plus faible somme des carrés des résidus (SR²), et c'est mon binôme qui a obtenu le score le plus bas.
