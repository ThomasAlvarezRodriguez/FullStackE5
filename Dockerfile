# Utiliser une image de base Python officielle
FROM python:3.12

# Définir le répertoire de travail dans le conteneur
WORKDIR /App_Checklist

# Copier les fichiers de dépendances et les installer
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copier le reste du code de l'application dans le conteneur
COPY . .

# Exposer le port sur lequel l'application va tourner
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "BackList.wsgi"]
