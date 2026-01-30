# Rapport Projet LLM : conception d’un chatbot sur le portfolio

### Contexte :

L’objectif de ce projet est de créer un chatbot permettant de dialoguer avec un jumeau virtuel, capable de représenter fidèlement un profil professionnel. Ce chatbot est conçu pour connaître l’ensemble des informations issues d’un portfolio afin de répondre à des questions telles que :

    o	Qui es-tu ?
    o	Quelles sont tes compétences ?
    o	Sur quels projets as-tu travaillé ?
    o	...

Pour la réalisation de cet outil, le langage Python a été utilisé pour le développement, le framework Streamlit pour la création de l’interface du chatbot, ainsi que Upstash pour l’hébergement et le stockage des données. Le projet s’appuie également sur l’utilisation de l’API OpenAI, et plus précisément du modèle GPT-4.1-nano, afin d’alimenter l’agent conversationnel.

Dans la suite de ce rapport, les différentes étapes ayant permis la conception et le développement de ce chatbot seront présentées.


### Etape 1 : Préparation des données

Dans un premier temps, il a fallu récupérer un maximum d’informations issues du portfolio et les mettre dans des fichiers Markdown afin d’alimenter le chatbot. 

    o	« a-propos » : regroupe toutes les informations sur qui je suis, mes centres d’intérêts et mes compétences techniques et personnelles 
    o	« experiences » : contient les informations sur mon alternance, un bilan et mes perspectives professionnelles.
    o	« formation » : parle de mes formations (BAC et BUT) avec un bilan pour chaque année de BUT, ainsi que de mon organisation de travail.
    o	« projet » : section avec un résumé de chacun des projets que j’ai eu l’occasion de réalisé au sein de ma formation.

Il est important que ces fichiers soient bien organisés avec différentes sections (#) pour que l’agent récupère facilement certain mot clé pour formuler ses réponses.
Ensuite, j’ai écrit un programme « load.py » qui contient une fonction « load_file » qui permet de charger tous les fichiers.


### Etape 2 : Découpage des documents (chunking)

Une fois les fichiers Markdown créés et organisés, ceux-ci sont découpés en segments cohérents. Pour cela, un programme Python « chunk.py » a été développé. Il contient une fonction « chunk_file », dont le rôle est de générer une liste de sections à partir des fichiers Markdown en s’appuyant sur les différents niveaux de titres (#, ##, ###).


### Etape 3 : Indexation dans Upstash
Cette troisième étape consiste à indexer nos chunk et à les envoyer dans Upstash Vector. Pour ce faire, j’ai créé le programme « index.py » qui contient une fonction « index_chunks » qui permet d’effectuer l’envoi vers la plateforme de stockage. 


### Etape 4 : Création de l’agent IA

Pour le développement de l’agent, qui permettra de répondre aux questions, j’ai écrit le programme « agent.py ». Ce programme contient plusieurs fonctions :

    o  	« search_portfolio » : son rôle est d’effectuer des recherches dans le portfolio (les fcihiers Markdown). Elle utilise la recherche vectorielle grâce à l’indexation faite juste avant. Pour répondre à une question, elle recherche les 10 chunks les plus proches (ceux qui contiennent le plus de mots clés de la question) et si elle n’en trouve pas elle renvoi « Aucune information trouvée dans le portfolio. ».
    o	« ask_agent » : elle permet de soumettre une question à l’agent et utilise la fonction présentée précédemment pour obtenir un réponse.
    o	« get_agent » : elle sert juste a retourné l’agent configuré pour l’utiliser ailleurs.


### Etape 5 : Interface utilisateur (Streamlit)

L'interface de mon chatbot est assez simple, mais on y retrouve un titre, un bouton pour créer une nouvelle conversation, 3 boutons avec des questions prédéfinit et enfin la barre de saisie des questions. 

Pour créer cette interface, j’ai donc écrit le programme « app_ia.py », dans lequel, j’utilise le Framework Streamlit. 

Tout d’abord j’ai configuré le path, puis placé le titre. Ensuite, on retrouve le peu de style ajouté à mon outil qui me sert principalement pour le placement des boutons. Puis, l’initialisation de la session, la création du bouton « Nouvelle conversation » qui et l’affichage du chat (la partie questions / réponses). Enfin, on retrouve la fonction « process_question », son rôle est de traitée une question de l’utilisateur et de générer la réponse de l’agent. Pour plus de détail, voici exactement ce que fait la fonction :

    o	Ajoute la question à l'historique de la conversation
    o	Récupère le contexte des messages récents (4 derniers échanges)
    o	Construit un prompt enrichi avec l'historique pour maintenir la cohérence
    o	Interroge l'agent OpenAI qui utilise la recherche vectorielle Upstash
    o	Ajoute la réponse à l'historique et actualise l'interface

J’utilise cette fonction pour les questions posées par un message (la saisie de l’utilisateur) et aussi pour les boutons questions.


### Conclusion : 

Pour conclure, plusieurs améliorations pourraient être apportées à cet outil. Tout d’abord, en corrigeant certains bugs comme la fixation des boutons de questions ou bien lorsqu’il dit qu’il ne trouve pas de réponse à un bouton question alors que sur la conversation d’avant il en avait trouvé une. Je pourrais aussi ajouter une historisation des échanges, ainsi qu’un enrichissement de l’interface graphique afin qu’elle reflète davantage ma personnalité, par exemple en s’inspirant du style de mon portfolio. Il serait également possible d’apporter plus de précisions aux fichiers Markdown afin de fournir davantage d’informations à l’agent et ainsi améliorer la pertinence de ses réponses.

Enfin, la réalisation de ce projet a permis de découvrir l’utilisation de l’API OpenAI ainsi que le fonctionnement des bases de données vectorielles, notamment à travers les notions de chunking et d’indexation. Ce travail a également permis d’approfondir l’utilisation du langage Python et du framework Streamlit dans le cadre du développement d’une application complète.
