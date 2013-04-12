#!/bin/env python

# Script to print the list of branches for a tree
#
# davide.gerbaudo@gmail.com
# April 2013

import optparse
import re
import string
import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True # don't let root steal your cmd-line options
r.gROOT.SetBatch(1)                        # go batch!
r.gErrorIgnoreLevel = 9999                 # suppress messages about missing dict
                                           # (can't get rid of the 'duplicate' ones?)

usage = ("Usage : %prog [options] treename filename"
                  "\n Examples :"
                  "\n %prog  -r '*genJet*' susy d3pd.root"
                  )

parser = optparse.OptionParser(usage = usage)
parser.add_option("--ls-file", dest="lsfile", default=False, action='store_true')
parser.add_option("-p", "--print-values", dest="printvalues", default=False, action='store_true',help='print also the values for N entries')
parser.add_option("-r", "--regex", dest="regex", default=None)
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true")

(options, args) = parser.parse_args()
assert len(args)==2, 'Invalid usage (run with -h)'
treeName, fileName = args[0], args[1]
lsfile          = options.lsfile
printvalues     = options.printvalues
regex           = options.regex
verbose         = options.verbose
if verbose :
    print "Using the following options:"
    print '\n'.join(["%s : %s"%(s, eval(s)) for s in ['treeName','fileName','lsfile','regex','verbose','printvalues']])
            
file = r.TFile.Open(fileName)
if lsfile : file.ls()
tree = file.Get(treeName)
branches = [b.GetName() for b in tree.GetListOfBranches()]
branches = sorted([b for b in branches if ((not regex) or re.search(regex, b))])
print '\n'.join(branches)

nEntriesToPrint = 4 if printvalues else 0
maxBrLen = min([60, max([len(b) for b in branches])])
line = '%'+str(maxBrLen)+'s' + ' : %s'
for iEntry in range(nEntriesToPrint) :
    print '-'*4+" entry %d "%iEntry + '-'*4
    tree.GetEntry(iEntry)
    def formatAttr(a) : return [e for e in a] if 'vector' in str(a) else a
#     print '\n'.join([line%(b, formatAttr(getattr(tree, b))) for b in branches])
    print '\n'.join([string.ljust(b, maxBrLen)+' : '+str(formatAttr(getattr(tree, b))) for b in branches])
