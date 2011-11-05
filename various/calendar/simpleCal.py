#
# DG Jan2010
#
# Purpose: create a simple 4x3 calendar to plan the work for the next few days
#
# works fine, but no matter what I do the final print size
# is slightly smaller than the sheet size.
# (I see other people complaining about this on the root forum...)
#

from datetime import date, datetime, timedelta
import ROOT


firstDay = datetime(2010, 01, 07)


ROOT.gROOT.SetStyle("Plain")

paperFormat = 0 # 0 = A4, 1 = USLetter

ROOT.gStyle.SetPaperSize(paperFormat)

letterWidth = 11.
letterHeight = 8.5
cmPerIn = 2.54
a4Width = 29.7/cmPerIn
a4Height = 21.0/cmPerIn


nRows = 3              #  
nCols = 4	       #
xOffset = +0.0	       # offsets used for the header
yOffset = -0.02	       #
headerHeight = 1./20.  # header height (in normalized units)

dpiResolution = 150
canWidth = 0.
canHeight = 0.
if paperFormat == 0:
	canWidth = a4Width
	canHeight = a4Height
if paperFormat == 1:
	canWidth = letterWidth
	canHeight = letterHeight

can = ROOT.TCanvas("can", "simple calendar", int(canWidth*dpiResolution), int(canHeight*dpiResolution))
can.cd()

text = ROOT.TLatex(0., 0., "")
text.SetTextAlign(22)
text.SetTextFont(132)
text.SetTextSize(0.02)

line = ROOT.TLine(0., 0., 1., 1.)

cellWidth = 1. / float(nCols)
cellHeight = 1. / float(nRows)

for iRow in xrange(nRows):
	for iCol in xrange(nCols):
		xPos =      (cellWidth*(iCol+0.5)) + xOffset
		yPos = 1. - (cellHeight*(iRow)) + yOffset
		label = "x(%d): %f, y(%d): %f" % (iCol, xPos, iRow, yPos)
		weekday = firstDay.strftime("%A")
		weekday = weekday[:3]
		month = firstDay.strftime("%B")
		month = month[:3]
		label = "%s, %s %s %s" % (weekday, firstDay.strftime("%d"), month, firstDay.strftime("%Y"))
		text.DrawTextNDC(xPos, yPos, label)
		# draw vertical lines
		if(iRow==0 and iCol<(nCols-1)):
			xPos = cellWidth * (1.+iCol)
			line.DrawLineNDC(xPos, 0., xPos, 1.)
		# draw horizontal lines
		if iCol==0 :
			# above text
			if iRow>0:
				yPos += 0.5 * headerHeight
				line.DrawLineNDC(0., yPos, 1., yPos)
				yPos -= 0.5 * headerHeight

			# below text
			yPos -= 0.5 * headerHeight
			line.DrawLineNDC(0., yPos, 1., yPos)
		firstDay += timedelta(days=1)

can.SaveAs("cal.pdf")
can.SaveAs("cal.ps")


reply = ''
while reply not in ['y','n']:
	reply = raw_input("wanna quit?")
