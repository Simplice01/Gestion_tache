Cette application web, développée avec Django, permet de gérer des projets et les tâches associées dans un environnement structuré. Elle offre des fonctionnalités de suivi, d’attribution et de contrôle de l’avancement des travaux, adaptées à un usage individuel ou collaboratif de base.

Description

L’application repose sur une organisation simple : chaque projet regroupe un ensemble de tâches pouvant être assignées à différents utilisateurs. Elle permet de suivre l’état d’avancement des activités et de centraliser les interactions autour des tâches via un système de commentaires.

L’objectif est de proposer une base fonctionnelle claire pour la gestion de projets, tout en restant suffisamment flexible pour évoluer vers des besoins plus complexes.

Fonctionnalités
Création et gestion de projets
Ajout et organisation de tâches par projet
Attribution des tâches aux utilisateurs
Suivi du statut des tâches (à faire, en cours, terminé)
Affichage des utilisateurs impliqués dans un projet à partir des tâches assignées
Système de commentaires sur les tâches
Gestion des accès basée sur l’utilisateur connecté
Architecture technique

L’application est construite selon l’architecture classique de Django, en séparant clairement les modèles, les vues et les templates.

Les principales entités sont :

Projet : contient les informations générales (nom, date limite, statut, créateur)
Tâche : liée à un projet, avec un statut et un utilisateur assigné
Commentaire : associé à une tâche pour faciliter les échanges
Règles de gestion
Un projet ne peut être considéré comme terminé que si toutes les tâches associées sont complétées
Les utilisateurs visibles dans un projet sont déterminés à partir des tâches qui leur sont assignées
L’accès à un projet est limité aux utilisateurs autorisés selon les règles définies dans l’application
Installation
Cloner le dépôt :
git clone <url-du-repo>
cd gestion_de_tache
Créer un environnement virtuel :
python -m venv env
source env/bin/activate (Linux/Mac)
env\Scripts\activate (Windows)
Installer les dépendances :
pip install -r requirements.txt
Appliquer les migrations :
python manage.py migrate
Lancer le serveur :
python manage.py runserver
Perspectives d’évolution

Plusieurs améliorations peuvent être envisagées pour renforcer l’application :

Mise en place d’un système de rôles et de permissions avancées
Ajout de tableaux de bord et de statistiques
Exposition d’une API pour intégration avec d’autres services
Amélioration de la gestion collaborative (équipes, invitations, notifications)
Préparation au déploiement en environnement de production
Conclusion

Ce projet constitue une base solide pour la gestion de tâches et de projets avec Django. Il peut servir de support d’apprentissage ou de point de départ pour le développement d’une application plus complète, orientée vers des usages professionnels.
