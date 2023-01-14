import argparse
from datetime import datetime
import osmium

class POI:
    def __init__(self,id,version,changeset,user,timestamp,name,poi_type,deleted):
        self.id=id
        self.version=version
        self.changeset=changeset
        self.first_edit=datetime.fromtimestamp(0)
        if version == 1:
            self.first_edit=timestamp
        self.last_edit=timestamp
        self.user=user 
        self.name=name   
        self.poi_type=poi_type 
        self.deleted=deleted

    #Update node, preserve infos if it is in deleted state to be able to print them later
    def set(self,version,changeset,user,timestamp,name,poi_type,deleted):
        self.changeset=changeset
        self.deleted=deleted
        if version == 1:
            self.first_edit=timestamp
        if version > self.version:    
            self.last_edit=timestamp   
        self.version=version         
        self.user=user 
        if not deleted: #deleted node has no name, preserve last recorded name
            self.name=name  
            self.poi_type=poi_type
    
    def history_url(self):
        return "https://www.openstreetmap.org/node/{id}/history".format(id=self.id)


    def to_tsv(self,operation):
        url=self.history_url()
        first_edit=self.first_edit.strftime("%d/%m/%Y")
        last_edit=self.last_edit.strftime("%d/%m/%Y")
        print(f"{operation}\t{self.id}\t{self.version}\t{self.changeset}\t{first_edit}\t{last_edit}\t{self.deleted}\t{self.poi_type}\t{self.name}\t{self.user}\t{url}")

    @classmethod
    def to_tsv_header(cls):
        print(f"Operation\tid\tversion\tchangeset\tfirst_edit\tlast_edit\tdeleted\tpoi_type\tname\tuser\turl")

    @classmethod
    def poi_type(cls,n):
        key=''
        value=''
        kv=''
        keys=('amenity','shop','tourism')
        for k in keys:
            if k in n.tags:
                key=k
                value=n.tags[key]
                break
        if key != '':
            kv = key + '=' + value
        return kv
        


class POIHandler(osmium.SimpleHandler):
    def __init__(self):
        super(POIHandler, self).__init__()
        self.poi = {} #POI dict indexed by node id

    #tell if the node is a POI we're interested in
    def is_POI(self,n):
        return ('amenity' in n.tags or 'shop' in n.tags or 'tourism' in n.tags) and 'name' in n.tags            

    def add_poi(self,n):
        # does not work if the deleted version is seen first
        # Q are versions seen in order ?
        name =''
        if 'name' in n.tags:
            name = n.tags['name'].replace('\n', ' ')
        poi_type = POI.poi_type(n)    
        if n.id in self.poi:
            if  self.poi[n.id].version > n.version:
                print(f"W version {n.version} seen after {self.poi[n.id].version} Node: id {n.id}  cs {n.changeset} deleted {n.deleted} user {n.user}")
            self.poi[n.id].set(n.version,n.changeset,n.user,n.timestamp,name,poi_type,n.deleted)
            self.poi[n.id].to_tsv("2.Update")
            return

        if self.is_POI(n): 
            self.poi[n.id]=POI(n.id,n.version,n.changeset,n.user,n.timestamp,name,poi_type,n.deleted)    
            self.poi[n.id].to_tsv("1.Add")

    def print_deleted(self):
        for id in self.poi:
            p=self.poi[id]
            if p.deleted:
                p.to_tsv("3.Deleted")

    def node(self, o):
        #print(f"DDD id {o.id}.{o.version} cs {o.changeset} deleted {o.deleted} user {o.user}")
        self.add_poi(o)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Find deleted POI in an OpenStreetMap data file.')
    parser.add_argument('file', type=argparse.FileType('r'),help='OpenStreetMap data file (.pbf) with history and user info.')
    args = parser.parse_args()
    filename= args.file.name 
    args.file.close()

    h = POIHandler()
    POI.to_tsv_header()

    h.apply_file(filename)

    h.print_deleted()
    

       


