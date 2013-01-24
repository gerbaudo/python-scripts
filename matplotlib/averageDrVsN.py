#!/bin/env python

# Generate N objects uniformly distributed in (eta,phi), and look at the avg minimum separation
#
# Requires pyroot and pylab
#
# davide.gerbaudo@gmail.com
# Jan 2013

import itertools, numpy as np
import pylab as P
import ROOT as r

# configuration parameters [begin]
nEvents = 10000
possibleNobjects = [2, 4, 6, 8]
etaRange, phiRange = [-2., +2.], [0., r.TMath.TwoPi()]
etaMin, etaMax = etaRange[0], etaRange[1]
phiMin, phiMax = phiRange[0], phiRange[1]
# configuration parameters [end]

allMinDists = []
allAvgDists = []
allMeanMinDists = []
allMeanAvgDists = []

for nObj in possibleNobjects :
    objects = [r.TLorentzVector() for i in range(nObj)]
    avgDistances, minDistances = [], []
    for iEv in xrange(nEvents) :
        [o.SetPtEtaPhiE(10., e, p, 10.) for o, e,p in zip(objects,
                                                        np.random.uniform(etaMin, etaMax, nObj),
                                                        np.random.uniform(phiMin, phiMax, nObj))]
        dists = [o1.DeltaR(o2) for o1,o2 in itertools.combinations(objects, 2)]
        minDistances.append(min(dists))
        avgDistances.append(sum(dists)/float(len(dists)))
    meanMin = sum(minDistances)/float(len(minDistances))
    meanAvg = sum(avgDistances)/float(len(avgDistances))
    allMinDists.append(minDistances)
    allAvgDists.append(avgDistances)
    allMeanMinDists.append(meanMin)
    allMeanAvgDists.append(meanAvg)
    print "%d objects/evt : <minDist>=%.2f, <avgDist>=%.2f" % (nObj, meanMin, meanAvg)

# plot distributions
P.figure()
P.title('Minimum distance')
n, bins, patches = P.hist( allMinDists, 25, histtype='step',
                           label=["%d obj, <d>=%.2f"%(i,m) for i,m in zip(possibleNobjects, allMeanMinDists)])
P.legend()
P.show()
P.savefig('minDist.png')

P.figure()
P.title('Average distance')
n, bins, patches = P.hist( allAvgDists, 25, histtype='step',
                           label=["%d obj, <d>=%.2f"%(i,m) for i,m in zip(possibleNobjects, allMeanAvgDists)])
P.legend()
P.show()
P.savefig('avgDist.png')
