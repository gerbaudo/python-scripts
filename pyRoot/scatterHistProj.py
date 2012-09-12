#
# Example script to draw a 2D histogram with its projections on X and Y
#
# For more discussions on the topic, search for 'hbar' on the root forum.
#
# davide.gerbaudo@gmail.com
# August 2012

import ROOT as r

r.gROOT.SetBatch(1)
r.gROOT.SetStyle('Plain')
r.gStyle.SetOptStat(0)
r.gStyle.SetOptTitle(0)
r.gStyle.SetPadTickX(1)
r.gStyle.SetPadTickY(1)

nEvents = 10000

h2d = r.TH2F('h2d','2d histo',100, -4.0, +4.0, 50, -3.0, +6.0)
x, y = r.Double(0.), r.Double(0.)
for i in xrange(nEvents) :
    r.gRandom.Rannor(x, y)
    h2d.Fill(x, 0.9*y)
    r.gRandom.Rannor(x, y)
    h2d.Fill(x, 0.6*y+4.)


nPxX = 600
nPxY = 600
epsilon = 0  #1.0/nPxX # mask defect on top frame (only visible interactively, not in resulting graphics)
xFrac = 0.80 # x fraction of the canvas allocated to the main pad
yFrac = 0.75 # y fraction of the canvas allocated to the main pad
c = r.TCanvas('c','side projections', nPxX, nPxY)
c.cd()
pad2d = r.TPad('pad2d', 'central pad', 0.0, 0.0, xFrac, yFrac, 0, 0, 0)
pad2d.SetRightMargin(0.0)
pad2d.SetTopMargin(0.0)
pad2d.SetFillStyle(0)
c.cd()
padX = r.TPad('padX', 'top pad', 0.0, yFrac, xFrac-epsilon, 1.0, 0, 0, 0)
padX.SetRightMargin(0.0+epsilon)
padX.SetBottomMargin(0.0)
padX.SetFillStyle(0)
c.cd()
padY = r.TPad('padY', 'right pad', xFrac, 0.0, 1.0, yFrac, 0, 0, 0)
padY.SetLeftMargin(0.0)
padY.SetTopMargin(0.0)
padY.SetFillStyle(0)

c.cd()
pad2d.Draw()
pad2d.cd()
h2d.Draw()

c.cd()
padX.Draw()
padX.cd()
pjx = h2d.ProjectionX()
pjx.GetYaxis().SetNdivisions(-202)
pjx.Draw()


c.cd()
padY.Draw()
padY.cd()
pjy = h2d.ProjectionY()
pjy.SetFillColor(r.kBlue-10)
pjy.GetYaxis().SetNdivisions(-202)
pjy.Draw('hbar') # you might want to use this even just to get the rotated frame

# if you want to draw anything other than the bar, you need to use a TGraphError
pgy = r.TGraphErrors(0)
pgy.SetName('pgy')
for b in range(1, pjy.GetNbinsX()+1) :
    pgy.SetPoint(pgy.GetN(), pjy.GetBinContent(b), pjy.GetBinCenter(b))
    pgy.SetPointError(pgy.GetN()-1, 0.5*pjy.GetBinError(b), 0.5*pjy.GetBinWidth(b))
pgy.SetMarkerStyle(r.kFullCircle)
pgy.SetMarkerColor(r.kBlue)
pgy.SetLineColor(r.kBlue)
pgy.Draw('p')


c.Update()
for ext in ['gif','png','eps','pdf'] : c.SaveAs('scatterHistProj.'+ext)

#answ = ''
#while answ not in ['q'] : answ = raw_input('quit?')
