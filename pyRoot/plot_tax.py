#!/usr/bin/env python 

# davide.gerbaudo@gmail.com, Jan2009
#
# Just a simple script to visualize the canadian tax rate vs. income
# (don't remember the source of the data right now)

from ROOT import TGraphErrors, TF1

def canadianTax( x ):
    if x[0] <= 0.:
        return 0.
    steps = [38832., 38832., 48600.]
    tax = 0.
    if x[0] < steps[0]:
        tax = 0.15*x[0]
    elif x[0] < (steps[0]+steps[1]):
        tax = 0.15*steps[0] + 0.22*(x[0]-steps[0])
    elif x[0] < (steps[0]+steps[1]+steps[2]):
        tax = 0.15*steps[0] + 0.22*steps[1] + 0.26*(x[0]-steps[0]-steps[1])
    else :
        tax = 0.15*steps[0] + 0.22*steps[1] + 0.26*steps[1] + 0.29*(x[0]-steps[0]-steps[1]-steps[2])
    return tax/x[0]*100.
 

data = []
data.append( [ 10 , [      0 ,   8025] ] )
data.append( [ 15 , [   8025 ,  32550] ] )
data.append( [ 25 , [  32550 ,  78850] ] )
data.append( [ 28 , [  78850 , 164550] ] )
data.append( [ 33 , [ 164550 , 357700] ] )
data.append( [ 35 , [ 357700 ,1000000] ] )

gr = TGraphErrors(0)
for dd in data:
    yVal = dd[0]
    xVal = dd[1]
    xAve = (xVal[0]+xVal[1])/2.
    xErr = (xVal[1]-xVal[0])/2.
    gr.SetPoint( gr.GetN(), xAve, yVal)
    gr.SetPointError( gr.GetN()-1, xErr, 0.)

gr.Draw("alp")

canTax = TF1("canTax",canadianTax, 0., 1000000., 0)
 
canTax.Draw("same")

yy = raw_input("wanna quit?")
if yy == "n":
    print "ok"
