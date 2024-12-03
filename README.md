## 1 - Cloner le projet

git clone git@github.com:yohanherman/django_dataApp.git

## 2 - Créer un environnement virtuel (si nécessaire)
Cela créera un dossier venv dans ton projet contenant un environnement virtuel.

### sous windows
py -m venv venv

### sous mac
python3 -m venv venv

## 3 - Activer l'environnement virtuel

### sous windows
venv\Scripts\activate

source venv/Scripts/activate ( Git Bash)


### sous mac
source venv/bin/activate


## 4 - Installer les dépendances du projet Django ( si necéssaire)

pip install -r requirements.txt


## 5 - Accède au repertoire
cd mon-repertoire



## 6 - Appliquer les migrations de la base de données

python manage.py migrate

## 7- Démarrer le serveur de développement Django

python manage.py runserver


