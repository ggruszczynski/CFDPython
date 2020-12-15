#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 11:29:53 2020

@author: grzegorz
"""


x = 2


class Zwierze:
    def __init__(self, nazwa):
        self._nazwa = nazwa
        
    def drukuj_nazwe(self):
        print(self._nazwa)
        
        

z1 = Zwierze("Pies")


z1.drukuj_nazwe()


z2 = Zwierze("Inny Pies")
z2.drukuj_nazwe()