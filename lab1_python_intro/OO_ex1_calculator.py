#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 14:26:46 2020

@author: grzegorz
"""

class Calculator:

    def __init__(self):
        self.history = []

    def add_numbers(self, x1, x2):
        result = x1 + x2
        self.history.append(f'added {x1} to {x2} got {result}')
        return result

    def multiply_numbers(self, x1, x2):
        result = x1*x2
        self.history.append(f'multiplied {x1} by {x2} got {result}')
        return result

    def print_history(self):
        print('drukuje historie:')
        for h in self.history:
            print(h)



print('---- pierwszy kalkulator ----')
c1 = Calculator()
c1.add_numbers(10, 15)
c1.multiply_numbers(4, 4)
c1.print_history()


print('---- drugi kalkulator ----')
c2 = Calculator()
c2.add_numbers(1, 2)
c2.add_numbers(3, 4)
c2.print_history()

print('---- trzeci kalkulator ----')
c3 = c1
c3.add_numbers(10,10)
c1.print_history()
print('---- adres w pamieci ----')
print(c1)
print(c2)
print(c3)


