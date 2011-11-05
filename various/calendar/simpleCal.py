#!/bin/env python
#
# davide.gerbaudo@gmail.com
#
# Version history
# Jan2010 : first version using the PyROOT library
# Nov2010 : switch to PyX library instead
#
# Usage:
# $ python simpleCal.py
# Purpose:
# Create a simple calendar with 4x3 cells to plan the work for the next few days.
# Input parameters:
# - firstDay, that will appear on the top left corner
# - printBleedsMarkers: turn on/off markers showing the edges and the centering of the text
# - paper format: see the documentation from the PyX package
#                 (document.paperformat --> http://pyx.sourceforge.net/manual/node21.html)
# Output:
# - pdf or eps calendar file
#

from datetime import date, datetime, timedelta
from pyx import *


#
# Input parameters
#
firstDay = datetime(2011, 10, 24)
printBleedsMarkers = False
#paperFormat = document.paperformat.Letter
paperFormat = document.paperformat.A4
# swap w and h so that we get landscape
xMax = paperFormat.height
yMax = paperFormat.width
#print "xMax ",xMax," yMax ",yMax

#
# Some tunable parameters
#
nRows = 3                #  
nCols = 4	         #
xOffset = +0.0	         # offsets used for the header
yOffset = +0.0	         #
headerHeight = yMax/25.  # cell header height (in normalized units: 1/25 of the page height)
cellWidth = xMax / float(nCols)
cellHeight = yMax / float(nRows)

# create the canvas that will contain everything
c = canvas.canvas()
# apply global TeX setting
text.preamble(r"\parindent=0pt")
w = 3.0 # an appropriate parbox width for a date like 'Aaa, Bb Ccc 20dd' (Wed, 02 Nov 2010)


# vertical alignments by margins
if printBleedsMarkers:
	c.stroke(path.line(0, 0.5*yMax, xMax, 0.5*yMax), [style.linewidth.THin])
	c.text(0, 0.5*yMax, "line half height")
	c.stroke(path.line(0.5*xMax, 0., 0.5*xMax, yMax), [style.linewidth.THin])
	c.text(0.5*xMax, 0.1*yMax, "line half width")

for iRow in xrange(nRows):
	for iCol in xrange(nCols):
		xPos =      (cellWidth*(iCol+0.5)) + xOffset
		#yPos = 1. - (cellHeight*(iRow)) + yOffset
		yPos = yMax - (0.5*headerHeight + cellHeight*(iRow)) + yOffset
		#label = "x(%d): %f, y(%d): %f" % (iCol, 1.*xPos, iRow, 1.*yPos)
		weekday = firstDay.strftime("%A")
		weekday = weekday[:3]
		month = firstDay.strftime("%B")
		month = month[:3]
		label = "%s, %s %s %s" % (weekday, firstDay.strftime("%d"), month, firstDay.strftime("%Y"))
		c.text(xPos, yPos,  label, [text.parbox(w), text.halign.boxcenter, text.halign.flushcenter, text.valign.middle])
		if printBleedsMarkers:
			c.stroke(path.line(xPos, yPos-0.5*headerHeight, xPos, yPos+0.5*headerHeight), [style.linewidth.THin])
			c.stroke(path.line(xPos-0.5*headerHeight, yPos, xPos+0.5*headerHeight, yPos), [style.linewidth.THin])
		# draw vertical lines
		if(iRow==0 and iCol<(nCols-1)):
			xPos = cellWidth * (1.+iCol)
			c.stroke(path.line(xPos, 0., xPos, yMax), [style.linewidth.THin])
		# draw horizontal lines
		if iCol==0 :
			# above text
			if iRow>0:
				yPos += 0.5 * headerHeight
				c.stroke(path.line(0., yPos, xMax, yPos), [style.linewidth.THin])
				yPos -= 0.5 * headerHeight
			# below text
			yPos -= 0.5 * headerHeight
			c.stroke(path.line(0., yPos, xMax, yPos), [style.linewidth.THin])
		firstDay += timedelta(days=1)


#c.writeEPSfile("simpleCal")
c.writePDFfile("simpleCal")

