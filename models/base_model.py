#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime, timezone
import models
import json
import uuid
import pdb


ftime = "%d-%m-%Y %H:%M:%S"


def utclocal():
    """Devuelve el momento actual en la hora local"""
    utcnow = datetime.utcnow()
    nowlocal = utcnow.replace(tzinfo=timezone.utc).astimezone(tz=None)
    localtime = datetime.strptime(nowlocal.strftime(ftime), ftime)
    return localtime


class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    __atributosObligatorios = []
    __atributos = []


    def __init__(self, **kwargs):
        """Initialization of the base model"""
        nullobj = False
        if kwargs:
            if kwargs.get('__class__') is not None:
                del kwargs['__class__']
            if kwargs.get('id') is None and kwargs.get('creado') is None and kwargs.get('actualizado') is None:
                self.id = id = str(uuid.uuid4())
                self.creado = utclocal()
                self.actualizado = self.creado
            else:
                self.id = kwargs['id']
                self.creado = kwargs['creado']
                self.actualizado = kwargs['actualizado']
                del kwargs['id']
                del kwargs['creado']
                del kwargs['actualizado']
            for attr in self.__atributosObligatorios:
                if attr not in kwargs.keys():
                    nullobj = True
                    break
            if nullobj is False:
                for attr in kwargs.keys():
                    if not hasattr(self, attr):
                        nullobj = True
                        break
                    elif type(kwargs[attr]) is not type(getattr(self, attr)):
                        if attr == 'contrasenia' and kwargs[attr] == -1:
                            continue
                        if type(getattr(self, attr)).__name__ == 'datetime':
                            kwargs[attr] = datetime.strptime(kwargs[attr], ftime)
                        else:
                            try:
                                float(kwargs[attr])
                            except:
                                nullobj = True
                                break
                for key, value in kwargs.items():
                    if type(value) is float and type(getattr(self, key)) is int:
                        nullobj = True
                        break
                    elif type(value) is int and type(getattr(self, key)) is float:
                        setattr(self, key, float(value))
                    else:
                        setattr(self, key, value)
        else:
            nullobj = True
        if nullobj is True:
            self = None


    def __str__(self):
        """String representation of the BaseModel class"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"


    def save(self):
        """updates the attribute 'actualizado' with the current datetime"""
        models.storage.new(self)
        models.storage.save()


    def registrar(self):
        """registra la instancia en la base de datos. Es otro nombre para el
        método 'save'"""
        self.save()


    def update(self, *args, **kwargs):
        """updates the instance based on the keyword passed arguments"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "id" and key != "__class__" and key != "creado" and key != "actualizado":
                    if not hasattr(self, key):
                        return -1
                    if type(value) is not type(getattr(self, key)):
                        return -1
                else:
                    return -1
            for key, value in kwargs.items():
                setattr(self, key, value)
        self.actualizado = utclocal()
        models.storage.save()
        return 0


    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance"""
        # pdb.set_trace()
        new_dict = self.__dict__.copy()
        new_dict['id'] = self.id
        if type(new_dict["creado"]).__name__ == 'datetime':
            new_dict["creado"] = self.creado.strftime(ftime)
        if type(new_dict["actualizado"]).__name__ == 'datetime':
            new_dict["actualizado"] = self.actualizado.strftime(ftime)
        new_dict["__class__"] = self.__class__.__name__
        if hasattr(self, "fechaEvento"):
            new_dict["fechaEvento"] = new_dict["fechaEvento"].strftime(ftime)
        return new_dict


    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
