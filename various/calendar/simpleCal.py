#!/bin/env python
#
# davide.gerbaudo@gmail.com
#
# Version history
# Jan2010 : first version using the PyROOT library
# Nov2010 : switch to PyX library instead
# Nov2011 : add cmd-line options
#
# Usage:
# $ simpleCal.py -h
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
import datetime
import time
from pyx import *
from optparse import OptionParser
import sys


def printSimpleCal(firstDay, paperFormat,
		   printBleedsMarkers, printPdf, printPs,
		   verbose):
	#
	# Input parameters
	#
	#-- firstDay = datetime.datetime(2011, 11, 05)
	#-- printBleedsMarkers = False
	#-- #paperFormat = document.paperformat.Letter
	#-- paperFormat = document.paperformat.A4
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

	day = firstDay
	for iRow in xrange(nRows):
		for iCol in xrange(nCols):
			xPos =      (cellWidth*(iCol+0.5)) + xOffset
			#yPos = 1. - (cellHeight*(iRow)) + yOffset
			yPos = yMax - (0.5*headerHeight + cellHeight*(iRow)) + yOffset
			#label = "x(%d): %f, y(%d): %f" % (iCol, 1.*xPos, iRow, 1.*yPos)
			weekday = day.strftime("%A")
			weekday = weekday[:3]
			month = day.strftime("%B")
			month = month[:3]
			label = "%s, %s %s %s" % (weekday, day.strftime("%d"), month, day.strftime("%Y"))
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
			day += timedelta(days=1)

	outFileName="cal-%s" % firstDay.strftime("%Y-%m-%d")
	if verbose: print "saving output file %s.[ext]" % outFileName
	if printPs: c.writeEPSfile(outFileName)
	if printPdf: c.writePDFfile(outFileName)


if __name__=="__main__":
	validPaperFormat = ["A4", "Letter"]
	parser = OptionParser()
	parser.add_option("-f", "--first-day", dest="firstDay",
			  help="first day on the calendar",
			  metavar="FIRST_DAY(YYYY-MM-DD)")
	parser.add_option("-p", "--paper-format", dest="paperFormat",
			  help="paper format, %s"%validPaperFormat,
			  default="A4")
	parser.add_option ("-m","--markers",
			   help="Print also markers indicating some key coordinates",
			   dest="markers",
			   action="store_true",
			   default=False)
	parser.add_option ("--pdf",
			   help="Generate a pdf output (default)",
			   dest="pdf",
			   action="store_true",
			   default=True)
	parser.add_option ("--ps",
			   help="Generate a ps output",
			   dest="ps",
			   action="store_true",
			   default=False)
	parser.add_option ("-v","--verbose",
			   help="Turn on verbose printout",
			   dest="verbose",
			   action="store_true",
			   default=False)
	options,args = parser.parse_args()
	printBleedsMarkers = options.markers
	printPdf = options.pdf
	printPs = options.ps
	verbose = options.verbose
	# try validate the options
	firstDay = datetime.datetime.today()
	if options.firstDay:
		print options.firstDay
		try:
			firstDay =  time.strptime(options.firstDay, "%Y-%m-%d")
			firstDay = datetime.datetime(*firstDay[:6]) # convert time to datetime
			# the method above was lifted from:
			# http://stackoverflow.com/questions/2428746/datetime-command-line-argument-in-python-2-4
		except:
			print "Invalid date format %s; should be YYYY-MM-DD.\n%s" % (options.firstDay,sys.exc_info())
			sys.exit(1)

	paperFormat = document.paperformat.A4
	if options.paperFormat:
		paperFormat = options.paperFormat
		if not paperFormat in validPaperFormat:
			print "Invalid paper format %s; should be %s" % (paperFormat, validPaperFormat)
			syst.exit(1)
		if paperFormat=="A4": paperFormat = document.paperformat.A4
		if paperFormat=="Letter": paperFormat = document.paperformat.Letter
	# now actually do the job
	printSimpleCal(firstDay, paperFormat,
		       printBleedsMarkers, printPdf, printPs,
		       verbose)
	# end __main__

