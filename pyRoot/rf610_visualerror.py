
import ROOT as r

r.gSystem.Load( "libRooFit" )

x = r.RooRealVar("x","x",-10,10)
  
m = r.RooRealVar("m","m",0,-10,10)
s = r.RooRealVar("s","s",2,1,50)
sig = r.RooGaussian("sig","sig",x,m,s)

m2 = r.RooRealVar("m2","m2",-1,-10,10)
s2 = r.RooRealVar("s2","s2",6,1,50)
bkg = r.RooGaussian("bkg","bkg",x,m2,s2)

fsig = r.RooRealVar("fsig","fsig",0.33,0,1)
model = r.RooAddPdf("model","model",r.RooArgList(sig,bkg), r.RooArgList(fsig))

x.setBins(25)
d = model.generateBinned(r.RooArgSet(x),1000)

fr = model.fitTo(d,r.RooFit.Save())


frame = x.frame(r.RooFit.Bins(40),r.RooFit.Title("P.d.f with visualized 1-sigma error band"))
d.plotOn(frame)

VisualizeError = r.RooFit.VisualizeError
FillColor = r.RooFit.FillColor
LineWidth = r.RooFit.LineWidth
LineColor = r.RooFit.LineColor
LineStyle = r.RooFit.LineStyle
Components = r.RooFit.Components
DrawOption = r.RooFit.DrawOption

model.plotOn(frame,VisualizeError(fr,1),FillColor(r.kOrange))


model.plotOn(frame,VisualizeError(fr,1,r.kFALSE), DrawOption("L"), LineWidth(2), LineColor(r.kRed)) ;
model.plotOn(frame,VisualizeError(fr,1), FillColor(r.kOrange), Components("bkg")) ;
model.plotOn(frame,VisualizeError(fr,1, r.kFALSE), DrawOption("L"), LineWidth(2), LineColor(r.kRed), Components("bkg"), LineStyle(r.kDashed)) ;

model.plotOn(frame)
model.plotOn(frame, Components("bkg"), LineStyle(r.kDashed))
d.plotOn(frame)
frame.SetMinimum(0)

#
#
#  // V i s u a l i z e   p a r t i a l   f i t   e r r o r 
#  // ------------------------------------------------------
#
#  // Make plot frame
#  RooPlot* frame2 = x.frame(Bins(40),Title("Visualization of 2-sigma partial error from (m,m2)")) ;
#  
#  // Visualize partial error. For partial error visualization the covariance matrix is first reduced as follows
#  //        ___                   -1
#  // Vred = V22  = V11 - V12 * V22   * V21
#  //
#  // Where V11,V12,V21,V22 represent a block decomposition of the covariance matrix into observables that
#  // are propagated (labeled by index '1') and that are not propagated (labeled by index '2'), and V22bar
#  // is the Shur complement of V22, calculated as shown above  
#  //
#  // (Note that Vred is _not_ a simple sub-matrix of V)
#
#  // Propagate partial error due to shape parameters (m,m2) using linear and sampling method
#  model.plotOn(frame2,VisualizeError(*r,RooArgSet(m,m2),2),FillColor(kCyan)) ;
#  model.plotOn(frame2,Components("bkg"),VisualizeError(*r,RooArgSet(m,m2),2),FillColor(kCyan)) ;
#  
#  model.plotOn(frame2) ;
#  model.plotOn(frame2,Components("bkg"),LineStyle(kDashed)) ;
#  frame2->SetMinimum(0) ;
# 
#
#  // Make plot frame
#  RooPlot* frame3 = x.frame(Bins(40),Title("Visualization of 2-sigma partial error from (s,s2)")) ;
#  
#  // Propagate partial error due to yield parameter using linear and sampling method
#  model.plotOn(frame3,VisualizeError(*r,RooArgSet(s,s2),2),FillColor(kGreen)) ;
#  model.plotOn(frame3,Components("bkg"),VisualizeError(*r,RooArgSet(s,s2),2),FillColor(kGreen)) ;
#  
#  model.plotOn(frame3) ;
#  model.plotOn(frame3,Components("bkg"),LineStyle(kDashed)) ;
#  frame3->SetMinimum(0) ;
#
#
#  // Make plot frame
#  RooPlot* frame4 = x.frame(Bins(40),Title("Visualization of 2-sigma partial error from fsig")) ;
#  
#  // Propagate partial error due to yield parameter using linear and sampling method
#  model.plotOn(frame4,VisualizeError(*r,RooArgSet(fsig),2),FillColor(kMagenta)) ;
#  model.plotOn(frame4,Components("bkg"),VisualizeError(*r,RooArgSet(fsig),2),FillColor(kMagenta)) ;
#  
#  model.plotOn(frame4) ;
#  model.plotOn(frame4,Components("bkg"),LineStyle(kDashed)) ;
#  frame4->SetMinimum(0) ;
#
#
  
c = r.TCanvas("rf610_visualerror","rf610_visualerror",800,800)
c.Divide(2,2)
c.cd(1) ; r.gPad.SetLeftMargin(0.15) ; frame.GetYaxis().SetTitleOffset(1.4)  ; frame.Draw()
#c.cd(2) ; r.gPad.SetLeftMargin(0.15) ; frame2.GetYaxis().SetTitleOffset(1.6) ; frame2.Draw()
#c.cd(3) ; r.gPad.SetLeftMargin(0.15) ; frame3.GetYaxis().SetTitleOffset(1.6) ; frame3.Draw()
#c.cd(4) ; r.gPad.SetLeftMargin(0.15) ; frame4.GetYaxis().SetTitleOffset(1.6) ; frame4.Draw()
answ = ''
while answ not in ['y'] : answ = raw_input("quit?")
