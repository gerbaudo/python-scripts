#!/bin/env python

from pyx import *

c = canvas.canvas()

xDim, yDim = 8, 6
c.stroke(path.line(0, 0, xDim, 0))
c.stroke(path.line(xDim, 0, xDim, yDim))
c.stroke(path.line(xDim, yDim, 0, yDim))
c.stroke(path.line(0, yDim, 0, 0))


c.writeEPSfile("placeholder")
