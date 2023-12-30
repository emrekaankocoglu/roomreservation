import xmlrpc.client
import datetime
import pickle
s = xmlrpc.client.ServerProxy('http://localhost:9000')
print(pickle.loads(s.Catalogue().listobject().data))
room = pickle.loads(s.getid(5).data)
print(room)
print(type(room))