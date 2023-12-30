from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from catalogue.catalogue import Catalogue
from event.event import Event
from room.room import Room
from user.user import User
from organization.organization import Organization
from view.view import View
from threading import Thread
from catalogue.object import Object
import pickle
import traceback

cat = Catalogue()
cat = Object.load("Catalogue.pickle")

class ServiceWrapper:
    def __init__(self, service_class):
        self._service_class = service_class

    def __getattribute__(self, name):
        # Avoid infinite recursion by using object's __getattribute__
        service_class = object.__getattribute__(self, '_service_class')

        try:
            # Try to get the attribute from the service class
            attr = getattr(service_class, name)
        except AttributeError:
            # If the attribute doesn't exist, let the error propagate
            raise

        if callable(attr):
            def wrapper(*args, **kwargs):
                # Code to execute before each method call
                
                return pickle.loads(attr(*args, **kwargs))
            return wrapper
        else:
            return attr
        
catalogue_wrapper = ServiceWrapper(Catalogue)
    



with SimpleXMLRPCServer(('localhost', 9000)) as server:
    server.register_introspection_functions()

    server.register_instance(catalogue_wrapper)

    # server.register_function(lambda : pickle.dumps(cat.listobject()), "listObject")
    # server.register_function(lambda x: pickle.dumps(cat.getid(x)), "getid")
    server.register_function(Catalogue().registerEvent, "registerEvent")
    server.register_function(Catalogue().registerRoom, "registerRoom")
    server.register_function(Catalogue().registerOrganization, "registerOrganization")
    server.register_function(User.login, "login")
    server.register_function(User.createUser, "createUser")


    server.serve_forever()

