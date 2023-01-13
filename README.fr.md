
# osm-deleted-poi

[Version française.](README.fr.md)

Find deleted OpenStreetMap POI in a zone.

# Motivation

Lors d'un relevé des magasins du centre-ville de Grenoble j'ai constaté que certains avaient été suprimés d'OSM au lieu d'être taggés "shop=vacant".

Ce script permet d'identifier ces points d'intérêt (POI).

# Usage

## Obtenir les données

[Téléchargez](https://download.geofabrik.de/) le fichier pbf de la zone qui vous intéresse. Sélectionnez un fichier avec l'historique et les infos utilisateur (pour l'Europe, les fichiers sont disponibles sur le [serveur interne](https://osm-internal.download.geofabrik.de/), vous devez vous connecter avec votre compte OSM).

Exemple : Pour obtenir les données de Grenoble, sélectionnez [rhone-alpes-internal.osh.pbf](https://osm-internal.download.geofabrik.de/europe/france/rhone-alpes-internal.osh.pbf) sur la [page Rhône-Alpes](https://osm-internal.download.geofabrik.de/europe/france/rhone-alpes.html).   

Installez l'outil [Osmium en ligne de commande](https://osmcode.org/osmium-tool/). 

```bash
# Pour Debian et dérivées
apt install osmium 
```

Utilisateurs de MS Windows : il n'existe pas de version pré-compilée d'Osmium, faites-vous une faveur et [installez une distribution Linux](https://learn.microsoft.com/en-us/windows/wsl/install) dans le sous-système Windows pour Linux.

Sélectionnez la zone :

```bash
osmium extract --bbox 5.702591,45.147058,5.766106,45.200425 --with-history --overwrite -o grenoble.pbf  rhone-alpes-internal.osh.pbf
```

## Obtenir le programme

```bash
git clone https://github.com/JVillafruela/osm-deleted-poi.git

cd osm-deleted-poi
## Créez un environnement virtuel
python3 -m venv venv
source venv/bin/activate
#installer la bibliothèque PyOsmium dans venv
pip3 install osmium
```

## Exécuter le programme

```bash
python3 deleted_poi.py /mnt/e/OSM/extracts/grenoble.pbf >deleted.tsv
```

- Ouvrez le fichier deleted.tsv dans MS Excel ou Libre Office Calc (séparateurs : tabulation, encodage UTF-8). 
- Ajouter un filtre (LOC : Données / AutoFiltre) 
- Sélectionner colonne A "operation" = "3.Deleted

