#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel


class Persona(BaseModel):
    """Estos atributos estarán compartidos por las clases Usuario y Cliente"""
    nombre = ""
    apellido = ""
    dni = 0
    direccion = ""
    telefono = 0


    def __init__(self, *args, **kwargs):
        """inicializa el cliente"""
        super().__init__(*args, **kwargs)
