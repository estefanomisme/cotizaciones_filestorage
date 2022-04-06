#!/usr/bin/python3
""" holds class User"""
import models
from models.persona import Persona


class Cliente(Persona):
    """Representación de un cliente"""
    correo = ""

    __atributosObligatorios = ["nombre", "apellido"]
    __atributos = __atributosObligatorios + ["correo", "dni", "direccion", "telefono"]


    def __init__(self, *args, **kwargs):
        """inicializa el cliente"""
        super().__init__(*args, **kwargs)
    

    @property
    def cotizaciones(self):
        listaCotizaciones = []
        for cotizacion in models.storage.all("Cotizacion").values():
            if cotizacion.clienteId == self.id:
                listaCotizaciones.append(cotizacion)
        return listaCotizaciones


    def atributosObligatorios(self):
        return self.__atributosObligatorios


    def atributos(self):
        return self.__atributos
