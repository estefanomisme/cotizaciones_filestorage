#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel
import pdb


class Producto(BaseModel):
    """Representación de un cliente"""
    codigo = ""
    nombre = ""
    proveedor = ""
    precioPorUnidad = 0.0
    tipoUnidad = "" # kg, platos, copas, ...
    capacidadPorUnidad = 0.0 # ¿para cuántas personas es cada unidad de medida del producto?
    publicoObjetivo = "" # adultos, jovenes o niños
    productoOservicio = ""
    categoria = "" # producto -> bebidas, entremeses, entradas, ...
                                                   # servicio -> reserva de espacios, música, personal externo, ...
    descripcion1 = "" # descripción para los usuarios de la plataforma
    descripcion2 = "" # descripción para los clientes
    enStock = 0.0 # unidades en stock
    enOrden = 0.0 # unidades en orden
    
    __atributosObligatorios = ["codigo", "nombre", "tipoUnidad", "publicoObjetivo", "productoOservicio", "categoria"]
    __atributos = __atributosObligatorios + ["proveedor", "precioPorUnidad", "capacidadPorUnidad",
                                             "descripcion1", "descripcion2", "enStock", "enOrden"]


    def __init__(self, *args, **kwargs):
        """inicializa el producto"""
        super().__init__(*args, **kwargs)


    @property
    def cotizaciones(self):
        listaCotizaciones = []
        for cotizacion in models.storage.all("Cotizacion").values():
            if self.id in cotizacion.cantidadProductos.keys():
                listaCotizaciones.append(cotizacion)
        return listaCotizaciones


    def atributosObligatorios(self):
        return self.__atributosObligatorios


    def atributos(self):
        return self.__atributos
