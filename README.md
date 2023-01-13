# osm-deleted-poi

Find deleted OpenStreetMap POI in a zone.

# Motivation

During a survey of stores in downtown Grenoble I noticed that some had been deleted from OSM instead of being tagged "shop=vacant".

This script allows to identify these points of interest (POI).

# Usage

## Get the data

[Download](https://download.geofabrik.de/) the pbf file of the zone you are interested in. Select a file with history and user info (for Europe the files are avalaible on the [internal server](https://osm-internal.download.geofabrik.de/), you must log on with your OSM account)

Example : To get Grenoble data select [rhone-alpes-internal.osh.pbf](https://osm-internal.download.geofabrik.de/europe/france/rhone-alpes-internal.osh.pbf) on the [Rhône-Alpes page](https://osm-internal.download.geofabrik.de/europe/france/rhone-alpes.html).   

Install the [Osmium command line tool](https://osmcode.org/osmium-tool/). 

```bash
# On Debian and derivatives
apt install osmium 
```

MS Windows users : there are no pre-compiled versions of Osmium, do yourself a favor and [install a Linux distribution](https://learn.microsoft.com/en-us/windows/wsl/install) in the Windows Subsystem for Linux.

Select the zone :

```bash
osmium extract --bbox 5.702591,45.147058,5.766106,45.200425 --with-history --overwrite -o grenoble.pbf  rhone-alpes-internal.osh.pbf
```

## Get the program

```bash
git clone https://github.com/JVillafruela/osm-deleted-poi.git

cd osm-deleted-poi
#create a virtual environment
python3 -m venv venv
source venv/bin/activate
#install PyOsmium library in venv
pip3 install osmium
```

## Run the program

```bash
python3 deleted_poi.py /mnt/e/OSM/extracts/grenoble.pbf >deleted.tsv
```

- Open the deleted.tsv in MS Excel or Libre Office Calc (separators tab,encoding UTF-8). 
- Add a filter (LOC : Data / AutoFilter) 
- Select operation = "3.Deleted"
