# HUB de Checklist pour Jeux Vidéo

## Description
Ce site HUB est conçu pour permettre aux joueurs de gérer des checklists personnalisées pour leurs jeux vidéo favoris. Utilisant Django et PostgreSQL, le site offre une interface intuitive pour une expérience utilisateur optimale.

## Technologies Utilisées
- **Django** : Framework web pour le backend.
- **PostgreSQL** : Système de gestion de base de données.
- **Heroku** : Plateforme de déploiement en cloud.

## Docker
Pour lancer le projet avec Docker, suivez ces étapes :

1. Clonez le dépôt :
```bash
git clone https://github.com/ThomasAlvarezRodriguez/FullStackE5.git
```
2. Modifier le docker-compose.yml en fonction de votre configuration :

3. Lancez le projet :
```bash
docker-compose up
```
4. Rendez-vous sur http://localhost:8000/ pour accéder au site.

5. Si vous ne voulez pas utiliser Docker, vous pouvez suivre les instructions ci-dessous.

## Installation et Configuration
Pour installer et configurer ce projet localement, suivez ces étapes :

1. Clonez le dépôt :
```bash
git clone https://github.com/ThomasAlvarezRodriguez/FullStackE5.git
```
2. Créez un environnement virtuel :
```bash
python -m venv env
```
3. Activez l'environnement virtuel :
```bash
.\env\Scripts\activate
```
4. Installez les dépendances :
```bash
pip install -r requirements.txt
```
5. Créez un fichier .env à la racine du projet et ajoutez-y les variables d'environnement suivantes :
```bash
SECRET_KEY=your_secret_key
```
6. Créez une base de données PostgreSQL et ajoutez-y les variables d'environnement suivantes :
```bash
DATABASE_NAME=your_database_name
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password
DATABASE_HOST=your_database_host
DATABASE_PORT=your_database_port
```
7. Appliquez les migrations :
```bash
python manage.py migrate
```
8. Créez un super utilisateur :
```bash
python manage.py createsuperuser
```
9. Lancez le serveur :
```bash
python manage.py runserver
```
10. Rendez-vous sur http://localhost:8000/ pour accéder au site.

Assurez-vous d'avoir installé PostgreSQL et d'avoir créé une base de données avant de lancer le serveur. Pour plus d'informations, consultez la documentation de Django : https://docs.djangoproject.com/en/3.2/ref/databases/#postgresql-notes

Le site est configuré pour utiliser une base de données PostgreSQL hébergée sur Heroku. Pour utiliser une base de données locale, il faudra modifier le fichier settings.py en conséquence.

## Heroku
Le site est déployé sur Heroku à l'adresse suivante : https://checkliste5-b41e5aa2e648.herokuapp.com

## Utilisation
Une fois le site installé, vous pouvez :
- Créer un compte utilisateur.
- Ajouter de nouveaux jeux à votre liste de favoris.
- Gérer vos checklists pour chaque jeu.

## Auteur
Thomas Alvarez Rodriguez
Alexande Dias

