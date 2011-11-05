#!/bin/env python

from pyx import *

c = canvas.canvas()

c.stroke(path.line(0, 0, 6, 0))
c.stroke(path.line(6, 0, 6, 4))
c.stroke(path.line(6, 4, 0, 4))
c.stroke(path.line(0, 4, 0, 0))


c.writeEPSfile("placeholder")
