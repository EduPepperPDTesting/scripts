from pymongo import Connection
import gridfs
from gridfs.errors import NoFile

import os.path

class MongoUserStore():
    def __init__(self, host, db, port=27017, user=None, password=None, bucket='fs', **kwargs):
        # logging.debug('Using MongoDB for static content serving at host={0} db={1}'.format(host, db))
        _db = Connection(host=host, port=port, **kwargs)[db]
        self.db=_db
        if user is not None and password is not None:
            _db.authenticate(user, password)
        self.fs = gridfs.GridFS(_db, bucket)
        self.fs_files = _db[bucket + ".files"]   # the underlying collection GridFS uses
        
    def save(self, _id, data):
        # Seems like with the GridFS we can't update existing ID's we have to do a delete/add pair
        if _id:
            self.delete(_id)
        
        with self.fs.new_file(_id=_id) as fp:
            if hasattr(data, '__iter__'):
                for chunk in data:
                    fp.write(chunk)
            else:
                fp.write(data)
    
    def delete(self, _id):
        if self.fs.exists({"_id": _id}):
            self.fs.delete(_id)
            
    def find_one(self,user_id,type):
        # self.find({"user_id":user_id,"type":type}) # New feature "find" in version gridfs 2.7?
        _id={"user_id":user_id,"type":type}
        doc=self.db["fs.files"].find_one({"_id":_id},["_id"])
        if doc:
            with self.fs.get(_id) as fp:
                return {"_id":_id, "data": fp.read(), "length":fp.length}



import MySQLdb
from MySQLdb.cursors import DictCursor

conn=MySQLdb.connect(host="mysql",
					 user="pepper",
					 passwd="lebbeb",
					 db="pepper",
					 charset="utf8",
					 cursorclass=DictCursor)

class Model:
	def fetchAllDict(self,cursor):
		ret=[]
		for row in cursor.fetchall(): # fetchAllDict
			try:
				ret.append(row)
			except BaseException,e:
				print e		
		return ret

class UserModel(Model):
    def getAllPic(self):
        cursor = conn.cursor()
        cursor.execute("select id,photo from auth_userprofile where photo<>'';")
        return self.fetchAllDict(cursor)

um=UserModel()
us=MongoUserStore('localhost','userstore')

# us=MongoUserStore('dfw-mongos0.objectrocket.com','userstore',17017,'pepper','lebbeb')

photos=um.getAllPic()
upload_path="/home/tahoe/edx_all/uploads/photos"

from PIL import Image
from StringIO import StringIO

def get_pic_data(name):
    path=upload_path + "/" + name
    print path
    if os.path.isfile(path):

        img = Image.open(path)

        # img.resize((110,110),Image.ANTIALIAS)
        img.thumbnail((110,110),Image.ANTIALIAS)

        file=StringIO()
        img.save(file, 'JPEG')
        file.seek(0)

        return file.getvalue()

        # f=open(path,'rb')
        # print path
        # data=f.read()
        # f.close()
        # return data

for p in photos:
    data=get_pic_data(p.get("photo"))
    if data:
        us.save({"user_id":p.get("id"), "type":"photo"},data)
        print "==========================="
        print(p.get("id"))

