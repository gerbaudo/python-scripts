#!/bin/env python


#
# Reproduce the directory structure and contents from an input file into an output file.
#
# davide.gerbaudo@gmail.com
# May2012

import ROOT as r

class CopiableObj :
    "A class to perform recursive copies of TObjects"
    def __init__(self, original, parent=None) :
        if not original : return
        if not original.Class().InheritsFrom(r.TDirectory.Class()) :
            if parent : parent.cd()
            clone = None
            if original.Class().InheritsFrom(r.TTree.Class()) :
                clone  = original.CloneTree()
            else : clone  = original.Clone()
            if hasattr(clone, "SetDirectory") : clone.SetDirectory(parent)
            clone.Write()
        else :
            if not parent : print "Cannot create a directory without parent"
            parent.mkdir(original.GetName())
            dest = parent.Get(original.GetName())
            dest.cd()
            objects = [CopiableObj(original.Get(k.GetName()), dest) for k in original.GetListOfKeys()]
            parent.cd()

#___________________________________________________________

inputFileName = "/tmp/Datamu_MUON_OutputHisto.root"
outputFileName = inputFileName.replace(".root", "_copy.root")

inputFile = r.TFile.Open(inputFileName)
outputFile = r.TFile.Open(outputFileName, "recreate")
outputFile.cd()

for k in inputFile.GetListOfKeys() :
    CopiableObj(inputFile.Get(k.GetName()), outputFile)
outputFile.Write()
outputFile.Close()
