### Description des fichiers

-	01_instantiate_model.ipynb : 

Ce notebook lance le chargement des données brutes (rains.csv), le process de nettoyage des données ainsi que l’entrainement des modèles.

L’objectif est d’enregistrer et exporter les modèles de machine learning que nous avions construit lors du projet1 pour nous permettre de construire l’API.

Les modèles conservés et qui seront accessibles côté API sont les modèles : 
- Decision Tree
- Logistic Regression
- Random Forest
- Support Vector Machine

Nous avons donc exporté : 
- Les fichiers joblib des modèles DecisionTree, LogisticRegression, RandomForest et SupportVectorMachine.
Cela nous permettra d’instancier les modèles sans avoir à recharger les données ni à entrainer le modèle
- Les fichiers de données train_features / train_labels / test_features / test_labels 
- Un fichier features_num_min_max qui contient pour l’ensemble des variables numériques, les valeurs min et max des données de train_features, qui correspond à l’échantillon qui a servi à entrainer les modèles. 
Ce fichier permettra à l’API de choisir des valeurs aléatoires pour les variables numériques. 
Les données min et max ont été calculées avant que la normalisation StandardScaler ait été appliquée

### Docker

3 images ont été construites : 
-	project2-ubuntu-python: cette image permet d’activer un container avec l’environnement Python nécessaire pour faire tourner l’API
-	project2-api-server : cette image installe les librairies Flask et Scikit Learn et contient l’API
-	project2-client-tester : cette image contient les tests qui permettent de valider le bon fonctionnement de l’API 

### Kubernetes : 
A COMPLETER


### L'API : 
L'API n'est accessible qu'avec les login/password disponibles dans le fichier credentials.csv

Pour accéder à l'API 
Créer un tunnel SSH du poste client
ssh -i "cle" user@IP_de_la_VM -fNL 5000:192.168.49.2:30457
l'API sera dans ce cas accessible via le port 5000

CURL -X GET http://localhost:5000/status
fournit un statut ok de l'application

{
    "api": "project #2 - déploiement",
    "authors": [
        "Christelle PATTYN",
        "David CHARLES-ELIE-NELSON"
    ],
    "context": "formation Data Engineer",
    "status": "ok"
}

CURL -X GET http://localhost:5000/models
Liste les 4 modèles disponibles, ainsi que leur ModelId

{
    "models": [
        {
            "available": true,
            "id": "db5f7fb6-8ddf-420c-a485-4517c3200a64",
            "type": "Decision Tree"
        },
        {
            "available": true,
            "id": "59fa8691-f141-4cd9-8c50-4dc7138950d5",
            "type": "Logistic Regression"
        },
        {
            "available": true,
            "id": "86fed39b-c93f-4d70-aa5c-fece6d8dcb53",
            "type": "Random Forest"
        },
        {
            "available": true,
            "id": "c4dff96c-d447-4e06-a0bc-a7d158afc856",
            "type": "Support Vector Machine"
        }
    ]
}

CURL -X GET http://localhost:5000/performance/models
Affiche le balanced accuracy score de chaque modèle, le ModelId

{
    "performances": [
        {
            "metric_name": "balanced_accuracy",
            "model_id": "db5f7fb6-8ddf-420c-a485-4517c3200a64",
            "model_score": 0.7080063652994556,
            "model_type": "Decision Tree"
        },
        {
            "metric_name": "balanced_accuracy",
            "model_id": "59fa8691-f141-4cd9-8c50-4dc7138950d5",
            "model_score": 0.7490167942540479,
            "model_type": "Logistic Regression"
        },
        {
            "metric_name": "balanced_accuracy",
            "model_id": "86fed39b-c93f-4d70-aa5c-fece6d8dcb53",
            "model_score": 0.7457221813453384,
            "model_type": "Random Forest"
        },
        {
            "metric_name": "balanced_accuracy",
            "model_id": "c4dff96c-d447-4e06-a0bc-a7d158afc856",
            "model_score": 0.6856670830634144,
            "model_type": "Support Vector Machine"
        }
    ]
}

CURL -X GET http://localhost:5000/performance/model/ModelId
par exemple : 
CURL -X GET http://localhost:5000/performance/model/db5f7fb6-8ddf-420c-a485-4517c3200a64

fournit le score balanced accuracy de ce modèle spécifique

{
    "performance": {
        "metric_name": "balanced_accuracy",
        "model_id": "db5f7fb6-8ddf-420c-a485-4517c3200a64",
        "model_score": 0.7080063652994556,
        "model_type": "Decision Tree"
    }
}

!!! ça n'a pas marché sur ma VM !!!
!!! je n'ai réussi à le lancer que via Postman
CURL -X GET http://localhost:5000/performance/prediction/ -H 'Content-Type: application/json' - d /
{'model_id': 'db5f7fb6-8ddf-420c-a485-4517c3200a64',  'features': /
{'mintemp': 10,'maxtemp':20,'location':'Sydney','raintoday':'yes'},/  'Authentication': 'UmhpYW5ub246MzU0NQ==' }

CURL -X GET http://localhost:5000/performance/prediction/ -H 'Content-Type: application/json' -d {'model_id': 'db5f7fb6-8ddf-420c-a485-4517c3200a64', 
'features':{'mintemp': 10,'maxtemp':20,'location':'Sydney','raintoday':'yes'}, 
'Authentication': 'UmhpYW5ub246MzU0NQ==' }

Résultat : 
{
    "classes": [
        "no_rain",
        "rain"
    ],
    "classesProba": [
        0.26610723226281896,
        0.733892767737181
    ],
    "msg": "Le modèle prédit de la pluie pour demain avec une certitude de: 73.39 %"
}
