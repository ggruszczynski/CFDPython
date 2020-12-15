# -*- coding: utf-8 -*-


class Car:
    def __init__(self, m):
        self.__manufacturer = m

    @property
    def manufacturer(self):
        return self.__manufacturer

    @manufacturer.setter
    def manufacturer(self, value):
        if value in ("Audi", "BMW", "Mercedes", "Skoda", "Volvo"):
            self.__manufacturer = value
        else:
            raise ValueError("Incorrect manufacturer type.")

            

car = Car("BMW")
print(car.manufacturer)
car.manufacturer="Volvo"
print(car.manufacturer)