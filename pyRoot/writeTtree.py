#!/bin/env python

# see http://wlav.web.cern.ch/wlav/pyroot/tpytree.html

import array
import ROOT as r

r.gROOT.SetBatch(1)
treeBefUnf = r.TTree("treeBefUnf", "ensemble bin contents before unfolding")
binContBefUnf = array.array( 'd', 10*[ 0. ] )
treeBefUnf.Branch('mynum', binContBefUnf, 'mynum[%d]/D'%len(binContBefUnf))

print binContBefUnf
for i in range(10) :
    for b in range(len(binContBefUnf)) : binContBefUnf[b] = i*10+b
    print binContBefUnf
    treeBefUnf.Fill()
treeBefUnf.Scan("mynum[0]:mynum[1]:mynum[9]")
    
# for t in [treeBefUnf, treeAftUnf] :
#     t.SetDirectory(outFile)

outFile = r.TFile.Open('example_tree.root', 'recreate')
outFile.cd()
treeBefUnf.Write()
outFile.Close()
