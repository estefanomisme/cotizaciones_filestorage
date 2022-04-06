#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import os
import json
import models
from models.base_model import BaseModel
from models.cliente import Cliente
from models.cotizacion import Cotizacion
from models.persona import Persona
from models.producto import Producto
from models.usuario import Usuario
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import pdb

classes = {"Cliente": Cliente, "Cotizacion": Cotizacion,
           "Producto": Producto, "Usuario": Usuario}


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""
    __file_path = "file.json"
    __objects = {}


    def all(self, cls=None):
        """returns the dictionary __objects"""
        # pdb.set_trace()
        if cls:
            clsDict = {}
            for idObj, obj in self.__objects.items():
                if cls == obj.__class__ or cls == obj.__class__.__name__:
                    clsDict[idObj] = obj
            return clsDict
        return self.__objects


    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        # pdb.set_trace()
        if obj is not None:
            key = f'{obj.__class__.__name__}.{obj.id}'
            self.__objects[key] = obj


    def save(self):
        # pdb.set_trace()
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)


    def reload(self):
        """Deserialization:
        If 'file.json' exists, extracts all its dicts and converts them in
        objects to be read for the program
        """
        # pdb.set_trace()
        try:
            if os.stat(self.__file_path).st_size == 0:
                raise EOFError()
            with open(self.__file_path, 'r', encoding='UTF-8') as fp:
                obj = json.load(fp)
            # pdb.set_trace()
            for id, instance in obj.items():
                """Creates a instance of an object class from the dictionary
                Example:
                    ex = self.__allclasses[obj[idObj]['__class__']](**obj)
                        -> ex = BaseModel({'id': '98',
                                'created_at': '15-05-2019T17:30:46.15623',
                                ...})
                        -> ex = User(**kwargs)
                        -> ...etc
                """
                clsname = classes[id.split('.')[0]]
                initKwargs = obj[id]
                if initKwargs.get('contrasenia') is not None:
                    encryptedPasswd = initKwargs.get('contrasenia')
                    initKwargs['contrasenia'] = -1
                    objClass = clsname(**initKwargs)
                    setattr(objClass, 'contrasenia', encryptedPasswd)
                else:
                    objClass = clsname(**initKwargs)
                self.__objects[id] = objClass
        except FileNotFoundError:
            pass
        except EOFError:
            pass


    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = f'{obj.__class__.__name__}.{obj.id}'
            if key in self.__objects:
                del self.__objects[key]


    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()


    def get(self, cls, id):
        """A method to retrieve one object"""
        if id and type(id) == str:
            if cls in classes.keys():
                objects = self.all(eval(cls))
            elif cls in classes.values():
                objects = self.all(cls)
            for key, value in objects.items():
                if key.split(".")[1] == id:
                    return value
        return None


    def count(self, cls=None):
        """Count objects"""
        if cls in classes.keys() or cls in classes.values():
            objects = self.all(cls)
        else:
            objects = self.all()
        return len(objects)
