#!/bin/env python3

from Formes import Triangle
from Formes import carre
from Formes import cercle
import turtle


a = Triangle(g=(50,50),l=100,debug=True)
b = carre(g=(-50,-50),l=100,debug=True)
c = cercle(g=(-50,-50),l=100,debug=True)
turtle.Screen()
turtle.Screen().setup(640, 480, 100, 100)
a.trace()
c.trace()
b.trace()