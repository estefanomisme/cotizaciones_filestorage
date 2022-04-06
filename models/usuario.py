#!/usr/bin/python3
""" holds class User"""
import models
from models.persona import Persona
import hashlib
import pdb


class Usuario(Persona):
    """Representación de un usuario de la plataforma"""
    correo = ""
    contrasenia = ""
    rol = ""
    estado = ""
    

    __atributosObligatorios = ["nombre", "apellido", "correo", "contrasenia", "rol", "estado"]
    __atributos = __atributosObligatorios + ["dni", "direccion", "telefono"]


    def definirContrasena(self, _contrasenia):
        """encripta la contraseña pasada y la guarda en la instancia del
        usuario actual"""
        # pdb.set_trace()
        encrypt = hashlib.md5()
        encrypt.update(_contrasenia.encode("utf-8"))
        encrypt = encrypt.hexdigest()
        setattr(self, "contrasenia", encrypt)


    def __init__(self, *args, **kwargs):
        """inicializa el usuario"""
        if kwargs:
            if kwargs.get('loggedIn') is None:
                self.loggedIn = False
            else:
                self.loggedIn = kwargs['loggedIn']
            if type(kwargs.get('contrasenia')) is str:
                clave = kwargs['contrasenia']
                del kwargs['contrasenia']
                super().__init__(*args, **kwargs)
                self.definirContrasena(clave)
            elif kwargs.get('contrasenia') == -1:
                super().__init__(*args, **kwargs)
        else:
            self = None


    def update(self, **kwargs):
        if kwargs.get('contrasenia') is not None:
            _passwd = kwargs.get('contrasenia')
            del kwargs['contrasenia']
            self.definirContrasena(_passwd)
        super().update(**kwargs)


    def atributosObligatorios(self):
        return self.__atributosObligatorios


    def atributos(self):
        return self.__atributos
