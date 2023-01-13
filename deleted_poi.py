import argparse
import osmium

class POI:
    def __init__(self,id,version,changeset,user,name,poi_type,deleted):
        self.id=id
        self.version=version
        self.changeset=changeset
        self.user=user 
        self.name=name   
        self.poi_type=poi_type 
        self.deleted=deleted

    #Update node, preserve infos if it is in deleted state to be able to print them later
    def set(self,version,changeset,user,name,poi_type,deleted):
        if self.deleted:
            return
        self.version=version
        self.changeset=changeset
        self.deleted=deleted
        self.user=user 
        if not deleted: #deleted node has no name, preserve last recorded name
            self.name=name  
            self.poi_type=poi_type
    
    def url(self):
        return "https://www.openstreetmap.org/node/{id}/history".format(id=self.id)

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
            print(f"2.Update\t{n.id}\t{n.version}\t{n.changeset}\t{n.deleted}\t{poi_type}\t{name}\t{n.user}")
            if  self.poi[n.id].version > n.version:
                print(f"W version {n.version} seen after {self.poi[n.id].version} Node: id {n.id}  cs {n.changeset} deleted {n.deleted} user {n.user}")
            self.poi[n.id].set(n.version,n.changeset,n.user,name,poi_type,n.deleted)
            return

        if self.is_POI(n): 
            print(f"1.Add\t{n.id}\t{n.version}\t{n.changeset}\t{n.deleted}\t{poi_type}\t{name}\t{n.user}")
            self.poi[n.id]=POI(n.id,n.version,n.changeset,n.user,name,poi_type,n.deleted)    

    def print_deleted(self):
        for id in self.poi:
            p=self.poi[id]
            if p.deleted:
                url=p.url()
                print(f"3.Deleted\t{p.id}\t{p.version}\t{p.changeset}\t{p.deleted}\t{p.poi_type}\t{p.name}\t{p.user}\t{url}")

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
    print(f"Operation\tid\tversion\tchangeset\tdeleted\tpoi_type\tname\tuser\turl")

    h.apply_file(filename)

    h.print_deleted()
    

       


