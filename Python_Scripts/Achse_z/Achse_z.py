# -*- coding: utf-8 -*-
"""
Created on Mon May 19 13:04:02 2025

@author: julia
"""
import pyvisa
import PyOwisDC500 as z # Oder einfach direkt ausführen, wenn alles in einer Datei ist
# rm = pyvisa.ResourceManager()
# print(rm.list_resources())
#Parameter
Achse = 2
Position = 101 # Zwischen 101 mm und 0 mm
z.achsez(Achse, Position)

