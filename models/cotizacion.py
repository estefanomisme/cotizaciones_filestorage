#!/usr/bin/python3
""" holds class User"""
from datetime import datetime
import models
from models.base_model import BaseModel, ftime, utclocal
import pdb


class Cotizacion(BaseModel):
    """Representación de un cliente"""
    clienteId = ""
    numAdultos = 0
    numJovenes = 0
    numNinos = 0
    fechaEvento = utclocal()
    tipoEvento = ""
    estadoSolicitud = ""

    descuento = 0.0
    cantidadProductos = {}

    __atributosObligatorios = ["clienteId", "tipoEvento", "estadoSolicitud", "cantidadProductos"]
    __atributos = __atributosObligatorios + ["numAdultos", "numJovenes", "numNinos", "fechaEvento", "descuento"]


    def actualizarProductos(self, string="", **cantProductos):
        if type(cantProductos) is dict:
            productos = models.storage.all("Producto")
            for prodId in cantProductos.keys():
                if models.storage.get("Producto", prodId) is None:
                    return -1
            self.cantidadProductos = cantProductos
            if string != "fromInit":
                super().update()
            return 0
        return -1


    def __init__(self, *args, **kwargs):
        nullobj = False
        if kwargs:
            if type(kwargs.get('cantidadProductos')) is dict:
                cantProductos = kwargs['cantidadProductos']
                del kwargs['cantidadProductos']
                if self.actualizarProductos("fromInit", **cantProductos) == -1:
                    nullobj = True
            else:
                nullobj = True
            if type(kwargs.get('fechaEvento')) is str:
                try:
                    self.fechaEvento = datetime.strptime(kwargs['fechaEvento'], ftime)
                    del kwargs['fechaEvento']
                except:
                    nullobj = True
            else:
                nullobj = True
        else:
            nullobj = True
        if nullobj is True:
            self = None
        else:
            super().__init__(**kwargs)

    
    def update(self, **kwargs):
        if kwargs is not None and kwargs.get('clienteId') is None:
            if type(kwargs.get('cantidadProductos')) is dict:
                cantProductos = kwargs['cantidadProductos']
                del kwargs['cantidadProductos']
                if self.actualizarProductos(**cantProductos) == -1:
                    return -1
            if type(kwargs.get('fechaEvento')) is str:
                try:
                    self.fechaEvento = datetime.strptime(kwargs['fechaEvento'], ftime)
                    del kwargs['fechaEvento']
                except:
                    return -1
            super().update(**kwargs)


    @property
    def productos(self):
        listaProductos = []
        for prodId in self.cantidadProductos.keys():
            producto = models.storage.get("Producto", prodId)
            if producto is None:
                del self.cantidadProductos[prodId]
            else:
                listaProductos.append(producto)
        return listaProductos


    def precioTotalProducto(self, productoId):
        producto = models.storage.get("Producto", productoId)
        if producto is not None:
            cantidad = self.cantidadProductos.get(producto.id)
            if cantidad is not None:
                return producto.precioPorUnidad * cantidad
        return -1


    def precioTotal(self):
        total = 0
        for prodId in self.cantidadProductos.keys():
            total += self.precioTotalProducto(prodId)
        return total * (1 - self.descuento)


    def totalComensales(self):
        return self.numAdultos + self.numJovenes + self.numNinos


    def cambiarEstadoSolicitud(self, nuevoEstado):
        if type(nuevoEstado) is str:
            self.estadoSolicitud = nuevoEstado


    def atributosObligatorios(self):
        return self.__atributosObligatorios


    def atributos(self):
        return self.__atributos
