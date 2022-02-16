
---

# Projet 2 : Déploiement d'une API de Machine Learning
## Formation: Data Engineer

> **Auteurs**: 
> 
> * Christelle PATTYN
> * David CHARLES-ELIE-NELSON

---

<a name='cell-toc'></a>
## Sommaire:

   1. [Description du projet](#section-project-desc)

      1.1. [Contenu du projet](#section-project-content)  
      1.2. [Fonctionnalités de l'API](#section-api-functionality)  

   2. [Installation](#section-install)




   
   2. [Travail réalisé](#section-work-done)  
   
      2.1. [Architecture du projet](#section-architecture)  
      2.2. [Technologies utilisées](#section-techno)  
      2.3. [Description du contenu du projet](#section-desc-content)  

   3. [Et après...](#section-after)

   4. [Procédures annexes](#section-annexe-procs)

   5. [Liens externers](#section-external-links)

---

## 1. Description du projet <a name='section-project-desc'></a>
[Back to top](#cell-toc)

<br/>

### 1.1. Contenu du projet <a name='section-project-content'></a>
[Back to top](#cell-toc)

Ce projet consiste au déploiement des modèles de Machine Learning créés dans le cadre du projet #1.  
Il s'agit de quatre modèles permettant de prédire s'il va pleuvoir ou non demain dans l'une des cinq plus grandes villes d'Australie.

Ces modèles sont enregistrés et ne sont pas ré-entrainés.

Une API a été construite permettant d'interroger ces modèles sans être ré-entrainés.  
Celle ci a été développée via la librairie Flask de Python.

Les modèles conservés et qui seront accessibles côté API sont les modèles: 
   - Decision Tree
   - Logistic Regression
   - Random Forest
   - Support Vector Machine

L'API permet : 
   - de vérifier qu'elle bien active via son statut
   - de lister les modèles disponibles
   - de consulter les performances obtenues pour chacun des modèles sur les jeux de tests
   - d'effectuer un test de prédiction par modèle

Le test de prédiction n'est possible que pour les personnes authentifiées, ie dont les informations de connexion sont présentes dans le fichier credentials.csv

Pour réaliser cela, plusieurs containers ont été créés: 
   - un container Docker avec un serveur Ubuntu
   - un container Docker contenant l'API
   - plusieurs containers de tests pour valider l'API

L'API est déployé sur 3 Pods via une configuration Kubernetes.

<br/>


### 1.2. Fonctionnalités de l'API <a name='section-api-functionality'></a>
[Back to top](#cell-toc)

Voici les routes, statuts et fonctionnalités associées de l'API :  

<br/>

| Type | Route | Fonctionnalité | Paramètres |  
| :--- | :--- | :--- | :--- |  
| GET  | /status | permet de vérifier que l'application est bien active | - |  
| GET  | /models | liste les modèles de ML et le model_id qui peuvent être utilisés pour effectuer une prédiction : va-t-il pleuvoir demain  | - |  
| GET  | /performance/models | liste les performance de chaque modèle entrainés initialement sur un jeu de tests afin d'effectuer une prédiction : va-t-il pleuvoir demain  | - |  
| POST | /prediction | fournit la probabilité de pleuvoir ou non demain selon les données prévues par le modèle  | header : Authentication, body : model_id,features |          

Un export de workspace Postman est disponible (depuis le répertoire "Postman" à la racine du projet) avec un exemple de chaque appel.

<br/>

<br/>

## 2. Installation <a name='section-install'></a>

Vous trouverez ci-dessous une procédure décrivant comment:

   - installer et démarrer l'API du projet
   - instancier et lancer les containers de test de l'API

La procédure d'installation qui est décrite ci-dessous suppose que nous disposions de deux machines:

   - <u>une machine server</u>  
     (qui contiendra l'API)  
     Dans notre cas, nous avons pris la VM mise à disposition par datascientest pour héberger l'API.  
     Pour l'équipe datascientest, n'importe quelle machine (Linux de préférence) disposant des prérequis suivants 
     devraient convenir:
     
      - docker version >= 20.10.12 installé et démon Docker démarré            
      - minikube installé et démarré
      - la commande kubectl doit également être disponible sur la machine

   - <u>une machine cliente</u>  
     (machine depuis laquelle les clients de l'API initieront leurs requêtes vers l'API)  
     C'est la limitation en ressources disque de la VM (par rapport aux tailles de nos images Docker et aux nombres de 
     containers à instancier qui nous a fait choisir ce type d'architecture ; à savoir dissocier la partie serveur de la 
     partie cliente).  
     Nous concernant, nous avons pris notre machine personnelle pour héberger les containers de tests de l'API.  
     Pour l'équipe datatascientest, n'importe quelle machine (Linux de préférence) ayant accès à la machine qui 
     hébergera l'API fera l'affaire.  
     A noter qu'il faudra tout de même que les pré-requis suivants soient respectés sur le poste client:
        - docker version >= 20.10.12 installé et démon Docker démarré
        - docker-compose doit également être installé (version >= 2.2.3)
        - il faudra de plus veiller à ce qu'une connexion ssh soit possible entre le poste client et la machine server (celle qui contiendra l'API).  
          Cette condition est nécessaire pour permettre la mise en place d'une redirection de port via ssh entre ces deux machines.

La procédure décrite ci-dessous permettra le déploiement et la mise en service de l'API sur la machine server 

---

<u>Procédure de déploiement et démarrage de l'API</u>:

**1. Connectez vous sur la machine server**  

**2. Rendez vous dans un répertoire dans lequel nous allons récupérer le projet**  

**3. Suivez la procédure suivante pour récupérer le projet**  
  
     [procédure de récupération du projet](#sect-annexe-get-project)
     
**4. Pré-requis pour l'utilisation d'ingress**  
  
     Nous devons à présent exécuter la commande suivante car l'environnement kubernetes cible mis en place dans le cadre 
     de ce projet fait usage d'un ingress.  
     Pour que tout fonctionne avec minikube, nous devons au préalable activer le controlleur Ingress à l'aide de la commande suivante:  

```bash
minikube addons enable ingress
```

**5. Création de l'environnement kubernetes**  

   Les commandes suivantes vont permettre de déployer l'environnement kubernetes et d'instancier l'API dans un replicaset de taille: 3     

```bash
cd project/build/kubernetes
./create.sh
```

Vous devriez obtenir le résultat suivant au niveau du terminal:  

> deployment.apps/project2-deployment created  
> service/project2-service created  
> ingress.networking.k8s.io/project2-ingress created  

Désormais l'API devrait être démarrée au sein d'un container lui-même hébergé dans un Pod au sein d'un environnement kubernetes et plus précisément au sein d'un replicaset de taille 3.

**6. Info sur le service**  
  
Exécutez la commande suivante pour afficher les informations sur le service kubernetes qui a été créé pour l'API:

```bash
kubectl get service project2-service
```

Si tout c'est bien passé vous devriez obtenir quelque chose comme suit:  
>   NAME               TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE  
>   project2-service   NodePort   10.98.199.16   <none>        5001:32616/TCP   4m41s  

L'adresse IP (cluster-ip) et le numéro de port (32616) pourront être éventuellement différent sur votre affichage.

**7. Service URL**  

Nous allons ici récupérer les informations qui nous permettrons d'accéder à l'API via le service kubernetes.  
Pour cela exécutez la commande suivante:

```bash
minikube service project2-service --url
```

Vous devriez obtenir un résultat similaire à celui-ci:
>   http://192.168.49.2:32616  

Une nouvelle fois vous pouvez obtenir une adresse IP différente de celle affichée et même chose pour le numéro de port.

**8. Test manuel de l'API**  

Nous allons à présent faire un test manuel pour vérifier que l'API est bien joignable via le service kubernetes.  
Pour cela exécutez la commande suivante:  

```bash
curl -X GET http://192.168.49.2:32616/status
```

Le début de l'URL à utiliser pour joindre l'API est celle qui a été retourné par la commande de l'étape précédente.  
Vous devrez utiliser l'IP et le port qui a été affiché.  
Le résultat attendu est le suivant:

```json
     {  
         "api":"project #2 - d\u00e9ploiement"  
       , "authors":["Christelle PATTYN","David CHARLES-ELIE-NELSON"]  
       , "context":"formation Data Engineer"  
       , "status":"ok"  
     }  
```  

Ici nous voyons que nous avons bien reçu un retour de l'API: l'API est donc parfaitement joignable depuis la machine server (celle qui héberge l'environnement kubernetes qui contient l'API).  
Il nous reste cependant à vérifier le bon fonctionnement de l'API depuis une machine cliente (différente de celle sur laquelle nous sommes en ce moment).  
Pour cela, nous allons déployer les containers de tests qui auront la tâche de lancer plusieurs requêtes à l'API et d'en vérifier que le résultat onbtenu est bien celui attendu pour chacune des requêtes.  
Reportez-vous sur la procédure "Lancer les tests de bon fonctionnement de l'API" ci-dessous.  

































## 2. Travail réalisé <a name='section-work-done'></a>
[Back to top](#cell-toc)

<br/>


Le projet a été traité dans son intégralité et les différents tests que nous avons réalisés ont tous été exécutés avec succès.

Nous allons commencer ci-dessous par décrire brièvement l'architecture du projet ainsi que le contenu de ce qui a été livré.

<br/>

### [2.1] Architecture du projet <a name='section-architecture'></a>
[Back to top](#cell-toc)

L'architecture du projet est composée des éléments suivants:

   * **VM**  
   
     Il s'agit ici d'une machine virtuelle (mise à notre disposition par datascientest).  
     Cette machine aura pour rôle d'hébergée <u>minikube</u> (un environnement de test pour kubernetes permettant de simuler plusieurs noeuds depuis une même machine).  


   * **API**  

     Ce que nous nommerons par API correspond en fait à une API REST dont l'objectif est la mise à disposition des modèles de Machine Learning qui ont été préparés dans le cadre du projet 1.  
     Nous concernant, ces modèles de machine learning doivent prédire s'il pleuvra ou non le lendemain dans une des villes d'Australie (parmi une liste prédéfinie).  
     Par respect des consignes du projet, l'API REST sera hébergée dans un environnement kubernetes composé d'un replicaset de taille 3.  
     A noter que pour des raisons de ressources depuis la VM, nous nous sommes limités lors de nos tests à un réplicaset de taille 1 au lieu de 3 ... en effet notre VM avait des ressources disques qui ne nous permettaient pas d'aller au-delà (considérant nos tailles d'images Docker).


   * **CLIENT**  

     Il s'agit ici d'une machine physique que nous nommeront CLIENT.    
     Cette machine servira au déploiement d'un ensemble de containers Docker clients pour notre API.  
     L'objectif de ces containers sera de tester les différentes fonctionnalités de l'API.  
     A noter que ces containers (chargés de tester l'API) ont été hébergés sur une machine différente de la VM pour des raisons de ressources disque.

Cette architecture a été mise en place par le biais des moyens techniques qui vous sont présentés ci-dessous...

<br/>

### [2.2] Technologies utilisées <a name='section-techno'></a>
[Back to top](#cell-toc)

Dans le cadre de ce projet nous avons utilisés les différentes briques techniques suivantes:

   * **DOCKER**  
   
     Docker est la technologie de containerisation qui a été utilisée pour créer les containers de:  
     
     * l'API  
     * des clients chargés de tester l'API


   * **KUBERNETES**  
 
     Kubernetes est l'outil de gestion des containers qui nous permet d'instancier des containers sur différentes machines.  
     Dans le cadre de ce projet les différentes machines ont été simulées par le biais de "minikube".  
     Seule l'API sera hébergée dans l'environnement kubernetes. Les clients seront eux disponibles dans des containers instanciés directement au niveau de la machine CLIENT.


   * **MACHINE LEARNING**  
  
     L'API qui a été développée dans le cadre de ce projet dispose de 4 modèles (prédisant la pluie en Australie):
         * Decision Tree
         * Logistic Regression
         * Random Forest
         * Support Vector Machine

<br/>


### [2.3] Description du contenu du projet <a name='section-desc-content'></a>
[Back to top](#cell-toc)

> Vous trouverez ci-dessous un descriptif du contenu du travail rendu:

   * **GitHub**  
  
     L'intégralité du projet a été mis à disposition au sein du compte Github suivant: [dav-chris](https://github.com/dav-chris)  
     
     <u>ATTENTION</u>:  
     A noter que les fichiers les plus volumineux n'ont volontairement pas été inclus au niveau de GitHub (pour respecter le principe de GitHub qui n'est d'héberger que du code source).  
     Les fichiers seront par cont
     Parmi les fichiers volumineux en question, nous avons:
     
        * Le fichier csv (correspondant à la partie DATA du projet)  
          Ce fichier csv est le fichier dont nous sommes partis pour construire nos modèles dans le cadre d'un apprentissage supervisé.

        * Les modèles de machine learning



> Le compte GitHub ainsi que l'archive qui sera rendue contiennent donc les éléments suivants:

   * <span style='color:darkgreen;'>build</span>  
     répertoire contenant tous les éléments nécessaires à la construction des images Docker ainsi que l'environnement kubernetes.   
     Les sous répertoires sont les suivants:

     * <span style='color:darkgreen;'>build/docker</span>  
       répertoire qui contient tous les fichiers nécessaires à la création des images Docker et l'instanciation des containers clients.


     * <span style='color:darkgreen;'>build/docker/compose</span>  
       répertoire contenant le fichier docker-compose qui sera utilisé pour instancier les containers clients chargés de tester l'API.


     * <span style='color:darkgreen;'>build/docker/images</span>  
       répertoire contenant un sous-répertoire par image Docker utilisée dans le cadre du projet.        

          * <span style='color:darkcyan;'>ubuntu-python</span>  
            répertoire correspondant à l'image project2-ubuntu-python.
            Cette image servira de base pour créer les images Docker pour l'API (project2-api-server) et pour les clients (project2-client-tester).  
            L'image Docker correspondant à l'API avait une recommandation forte:  
            celle d'avoir la même version (ou éventuellement supérieure) de scikit-learn que celle qui a été utilisée depuis Google colab pour exporter les modèles dans des fichiers *.joblib. Cette restriction était nécessaire pour que le code Python utilisé côté API soit en mesure d'ouvrir les fichiers des modèles.  
            Scikit learn ayant des pré-requis sur la version de Python, nous avons porté notre choix sur la version 3.8.5 de Python pour respecter les conditions d'installation de scikit learn v1.0.2 nous sommes fixés sur la version 3.8.5 de Python. Nous avons donc préparé une image (basée sur ubuntu) pour consolider un socle d'environnement Python avec une compatibilité complète la version de scikit learn de Google Colab.  
            Nous avons ensuite décidé d'utiliser cette même image comme image de base pour la construction de l'image des containers clients (pour des raisons de facilité). Puisque l'image project2-ubuntu-python est construite en partie grâce à l'installation de Python depuis le code source, sa construction est assez longue (plusieurs longues minutes). Ainsi consolider ce socle Python dans une image dédiée, nous évite d'avoir à réinstaller constamment Python dans l'image Docker de l'API à chaque fois que le code de l'API change et que la reconstruction de l'image est nécessaire. Ce choix nous garantit un gain de temps énorme. 

          * <span style='color:darkcyan;'>api-server</span>
            répertoire correspondant à l'image project2-api-server.  
            Cette image contient l'API  et écoute par défaut sur le port 5000 et sur l'ip 0.0.0.0.  
            Il est possible de configurer l'IP et le port d'écoute de l'API soit au niveau de la ligne de commande du programme Python exécuté ou par le biais de variables d'environnement.

          * <span style='color:darkcyan;'>api-server</span>  
            répertoire correspondant à l'image project2-client-tester.  
            Cette image contient le code Python qui sera exécuté côté client pour tester les différents points de terminaison de l'API.  
            La particularité côté client est qu'il y aura plusieurs containers instanciés pour réaliser les tests. Tous ces containers étant créés sur la même machine (CLIENT), c'est via Docker-compose que cette partie sera gérée. Les fichiers de configuration Docker-compose correspondant sont situés dans: build > docker > compose.

     * <span style='color:darkgreen;'>build/kubernetes</span>  
       répertoire contenant les fichiers de configuration de l'environnement kubernetes (qui contiendra l'API).  
       Les fichiers de configuration de kubernetes sont les suivants:  
        * deployment.yml  
        * service.yml  
        * ingress.yml  
        
   * <span style='color:darkgreen;'>data</span>  
     répertoire contenant les fichiers en lien avec la partie Machine Learning du projet.  
     On y trouvera notamment les fichiers suivants:  

     <table border='1'>
        <tr>
           <th>Fichier</th>
           <th>Description</th>
        </tr>
        <tr>
           <td>rains.csv</td>
           <td>
              fichier de données qui nous a servi à entrainer les modèles dans le cadre d'un apprentissage   
              supervisé.
           </td>
        </tr>
        <tr>
           <td>numFeatures_min_max.csv</td>
           <td>
              fichier qui contient les valeurs maximales et minimales des variables numériques utilisées par le 
              modèle.
              Nous avons calculé, ces valeurs min et max depuis le jeu d'entrainement afin d'être en mesure de reproduire la transformation des valeurs numériques de la même façon qu'elles l'ont été lors de l'apprentissage.
           </td>
        </tr>
     </table>

     * <span style='color:darkgreen;'>data/train_test</span>  
       nous avons conservé dans ce répertoire la répartition du fichier rains.csv en deux jeux de données:

         <table border='1'>
            <tr>
               <th>Fichier</th>
               <th>Fonction</th>
               <th>Description</th>
            </tr>
            <tr>
               <td>train_features.csv</td>
               <td>jeu de données d'entrainement ne contenant que les variables explicatives.</td>
               <td rowspan=2>jeu de données d'entrainement</td>
            </tr>
            <tr>
               <td>train_labels.csv</td>
               <td>jeu de données d'entrainement ne contenant que les variables cibles.</td>
            </tr>
            <tr>
               <td>test_features.csv</td>
               <td>jeu de données de validation ne contenant que les variables explicatives.</td>
               <td rowspan=2>jeu de données de validation</td>
            </tr>
            <tr>
               <td>test_labels.csv</td>
               <td>jeu de données de validation ne contenant que les variables cibles.</td>
            </tr>
            <tr>
               <td>numFeatures_min_max.csv</td>
               <td>
                  fichier qui contient les valeurs maximales et minimales des variables numériques utilisées par le modèle.  
Les différents modèles disponibles par l'API ont besoin de données en entrée (features) pour être en mesure de nous fournir une prédiction. S'il manque des valeurs le modèle ne pourra pas nous fournir de résultat. Cependant nous ne souhaitions pas apporter une contrainte trop forte sur la nécessité de fournir toutes les données puisque nous ne disposons pas d'appareils de mesure susceptibles de nous fournir des métriques telles que la pression atmosphérique ou encore la vitesse du vent.  
Nous avons donc incorporé au sein de l'API un générateur de valeurs aléatoires pour les variables numériques et catégorielles. Autant pour les variables catégorielles nous connaissant la liste de valeurs possibles par variable, autant pour les variables numériques nous ne pouvons raisonner que par bornes (pour la génération de valeurs aléatoires). Nous avons donc choisi de considérer comme borne les valeurs minimales et maximales par variable telles qu'observées dans le jeu d'entrainement. Nous avons donc sauvegardé ces valeurs afin d'être en capacité de produire des valeurs aléatoires sans proposer de valeurs complètement aberrantes.
               </td>
               <td rowspan=2>valeurs de référence pour aider à produire des données aléatoires non aberrantes</td>
            </tr>
         </table>


   * <span style='color:darkgreen;'>data</span>  
     ce réperoire représente la base de données de notre API.  
     Pour fonctionner notre API a besoin de:
      - modèles de prédiction de pluie  
        Les modèles seront tous accessibles depuis le sous-répertoire <span style='color:darkgreen;'>models</span>
        De plus, le fichier *api_models.json* contient la liste des modèles disponibles pour l'API avec quelques caractéristiques par modèle. 
      - un scaler (objet de standardisation des variables explicatives ; paramétré avec le jeu d'entrainement)
      - une base de données 




   * **docs**
     répertoire contenant les fichiers suivants:
      * <span style='color:darkgreen;'>doc1</span>
          


      * <span style='color:darkgreen;'>installation_guide.md</span>
        une procédure d'installation


      * <span style='color:darkgreen;'>test_guide.md</span>
        une procédure pour démarrer l'API et les clients testeurs.


   * **src**


<br/>


<br/>

## 3. Et après... <a name='section-and-after'></a>
[Back to top](#cell-toc)

<br/>

   * Vous avez accès au guide d'installation dans le fichier:
     <span style='color:darkgreen;'>docs/installation_guide.md</span>


   * Une fois l'installation faite, vous pouvez suivre la documentation ci-dessous pour mettre en route l'API et lancer les clients testeurs:
     <span style='color:darkgreen;'>docs/run_guide.md</span>



<br/>

## . Lancer les tests de bon fonctionnement de l'API <a name='section-test-run-api'></a>
[Back to top](#cell-toc)

La procédure décrite ci-dessous permettra de valider le bon fonctionnement de l'API en réalisant des requêtes de test 
prédéfinies. Ces requêtes seront exécutées par des containers Docker qui contienne la partie cliente du projet et qui réaliseront des requêtes sur l'API depuis un code Python. Les retours fait par l'API seront analysés par les containers qui nous avertiront si des erreurs sont détectées.

<u>Procédure de lancement des tests de l'API</u>:

> 1. Connectez vous sur la machine cliente (machine Linux différente de celle ou tourne l'API)

> 2. Rendez vous dans un répertoire dans lequel nous allons récupérer le projet

> 3. Suivez la procédure suivante pour récupérer le projet  
     [procédure de récupération du projet](#sect-annexe-get-project)
     
> 4. Lancement d'une redirection de port  
     Pour que la machine cliente puisse joindre l'API, nous allons dans un premier temps devoir faire une redirection de port. Pour cela, exécutez la commande suivante en prenant soin de remplacer:
     - <key.pem\>  
       par le nom du fichier correspondant à la clé permettant de se connecter à la machine server
     - <username\>  
       par le nom du compte utilisateur permettant de se connecter à la machine server depuis la machine cliente       
     - <machine_server_ip\>  
       par l'adresse IP de la machine qui contient l'API
     - <service_id\>  
       par l'adresse du service kubernetes (cette adresse est celle qui a été retournée à l'étape "Service URL" dans la procédure "Procédure de déploiement et démarrage de l'API")
     - <service_port\>  
       par le port du service kubernetes (ce port est celui qui a été retourné à l'étape "Service URL" dans la procédure "Procédure de déploiement et démarrage de l'API")  
>>
>>   `ssh -i <key.pem\> <username\>@<machine_server_ip\> -fNL 5000:<service_id\>:<service_port\>`
>
     Exemple:
>>
>>   `ssh -i "data_enginering_machine.pem" ubuntu@34.244.189.52 -fNL 5000:192.168.49.2:32616`

> 5. Lancement des containers de tests
     Nous allons dans un premier temps nous positionner dans le répertoire comportant les fichiers de configuration de docker-compose à l'aide de la commande suivante:
>>
     `cd project/build/docker/compose`
>    
     Une fois positionné dans ce répertoire, lancer docker compose avec la commande:  
>>
>>   `docker-compose up`
>
     Il ne restera plus qu'à analyser l'affichage pour vérifier que tous les tests se sont bien passés.




<br/>

## *. Procédures annexes <a name='section-annexe-procs'></a>
[Back to top](#cell-toc)


**[\*] Récupération du projet depuis Github** <a name='sect-annexe-get-project'></a>
>>
Connectez-vous sur la machine cible (celle sur laquelle vous souhaitez récupérer le projet) et rendez vous dans un répertoire au sein duquel nous allons récupérer l'ensemble du projet.  
Exécutez ensuite la commande suivante:
>>
>>```
>>git clone https://github.com/dav-chris/project2.git ./project
>>```
>>
Le résultat de cette devrait être le suivant:  
un répertoire nommé "project2" devrait avoir été créé contenant tout le projet.
>>
Si pour quelque raison que ce soit des difficultés étaient rencontrées lors de cette étape, il serait alors possible d'extraire le projet depuis l'archive qui a été fournie à DataScientest à l'aide de la commande suivante (en ayant pris soin préalablement d'être positionné dans le répertoire devant contenir le projet):
>>
>>```
>>tar xvfz project2-deploiement.tgz
>>```
>>
Désormais avec l'une des deux commandes présentées ci-dessus nous devrions avoir le répertoire "project" présent dans le répertoire courant.





<br/>

## *. Liens externes <a name='section-external-links'></a>
[Back to top](#cell-toc)

* [Doc installation Docker Engine](https://docs.docker.com/engine/install/)
* [Doc installation Docker-compose](https://docs.docker.com/compose/install/)

<br/>



END