#!/bin/env python

from pyx import *

c = canvas.canvas()

xDim, yDim = 8, 6
c.stroke(path.line(0, 0, xDim, 0))
c.stroke(path.line(xDim, 0, xDim, yDim))
c.stroke(path.line(xDim, yDim, 0, yDim))
c.stroke(path.line(0, yDim, 0, 0))
c.text(0.275*xDim, 0.275*yDim, "Placeholder", [text.halign.center,text.valign.middle,trafo.rotate(40), text.size.Huge])
c.text(0.575*xDim, 0.575*yDim, "(%dx%d)"%(xDim,yDim), [text.halign.center,text.valign.middle,trafo.rotate(40), text.size.Large])

c.writeEPSfile("placeholder")
