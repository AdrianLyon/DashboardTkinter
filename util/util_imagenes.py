""" from PIL import ImageTk, Image

def leer_imagen( path, size): 
        return ImageTk.PhotoImage(Image.open(path).resize(size,  Image.ADAPTIVE))   """
from PIL import ImageTk, Image
import os
import sys

def resource_path(relative_path):
    """Obtiene la ruta de acceso al recurso en un ejecutable empaquetado con PyInstaller"""
    if getattr(sys, 'frozen', False):
        # Ejecutando como un ejecutable empaquetado
        base_path = sys._MEIPASS
    else:
        # Ejecutando desde el código fuente
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

def leer_imagen(path, size):
    # Usa resource_path para obtener la ruta correcta
    path = resource_path(path)
    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.Resampling.LANCZOS))
