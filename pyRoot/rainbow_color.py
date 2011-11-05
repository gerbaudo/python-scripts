#
# davide.gerbaudo@gmail.com, 2010
#
# A simple function to map a range of values to the "rainbow colors" used by ROOT.

from ROOT import TCanvas, TAttFill, TMarker
import ROOT as r

def rainbowColors(minVal, maxVal, curVal):
    """Given a range between minVal and maxVal, return the color of
    the visible spectrum proportional to the curVal"""
    # make sure we're daling with numbers
    minVal = float(minVal)
    maxVal = float(maxVal)
    curVal = float(curVal)
    if minVal >= maxVal:
        print "rainbowColors: %s <=%s  (invalid minVal >= maxVal)" % (minVal,maxVal)
        return r.kBlack
    if curVal<minVal or curVal>maxVal:
        print "rainbowColors: value %s out of range [%s,%s]" % (curVal, minVal, maxVal)
        return r.kBlack
    colLo = 51
    colHi = 101
    return colLo + int((colHi-colLo)*(curVal-minVal)/(maxVal-minVal)+0.5)

colLo = 51
colHi = 101


mark = TMarker()
mark.SetNDC()
mark.SetMarkerStyle(20)

nSteps = (colHi-colLo)+1
dx = 1./(nSteps)
xPos = 0.5*dx


can = TCanvas("can","")
can.cd()

for step in range(nSteps):
    col = rainbowColors(0,nSteps, step)
    print "%d" %int(col)
    mark.SetMarkerColor(int(col))
    mark.DrawMarker(xPos, 0.5)
    xPos += dx

answer = ""
while answer not in ["y"]:
    answer = raw_input("quit?")
