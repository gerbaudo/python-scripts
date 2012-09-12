#!/bin/env python

#
# http://en.wikipedia.org/wiki/Biorhythm
# from
# glowingpython

from datetime import date
import matplotlib.dates
from pylab import *
from numpy import array,sin,pi

t0 = date(1980,8,20).toordinal()
t1 = date.today().toordinal()
t = array(range((t1-15),(t1+15))) # range of 30 days

y = 100*[sin(2*pi*(t-t0)/23),  # Physical
         sin(2*pi*(t-t0)/28),  # Emotional
         sin(2*pi*(t-t0)/33)]; # Intellectual

# converting ordinals to date
label = []
for p in t:
 label.append(date.fromordinal(p))

fig = figure()
ax = fig.gca()
plot(label,y[0],label,y[1],label,y[2])
# adding a legend
legend(['Physical', 'Emotional', 'Intellectual'])
# formatting the dates on the x axis
ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%d/%b'))

show()
savefig('foo.png')
