import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import show
from pylab import setp

# ----------------------------------------------------

def adjust_spines(ax,spines):
    for loc, spine in ax.spines.iteritems():
        if loc in spines:
            spine.set_position(('outward',10)) # outward by 10 points
            spine.set_smart_bounds(True)
        else:
            spine.set_color('none') # don't draw spine

    # turn off ticks where there is no spine
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    else:
        # no yaxis ticks
        ax.yaxis.set_ticks([])

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    else:
        # no xaxis ticks
        ax.xaxis.set_ticks([])
# ----------------------------------------------------

fig = plt.figure()

x = np.linspace(0,2*np.pi,50)
y = np.sin(x)
#y2 = y + 0.1*np.random.normal( size=x.shape )
y2 =  np.linspace(0,0,50)

# plot data
ax = fig.add_subplot(1,1,1)
#line1,=ax.plot(x,y,'--')
line1,=ax.plot(x,y,'')
#line2,=ax.plot(x,y2,'bo')
line2,=ax.plot(x,y2,'')
setp(line2, linestyle='--', color='r')

# adjust the spines
adjust_spines(ax,['left','bottom'])

# set ticks and tick labels
#   x
ax.set_xlim((0,2*np.pi))
ax.set_xticks([0,np.pi,2*np.pi])
pichr = unichr(0x03C0)
ax.set_xticklabels(['0',pichr,'2 '+pichr])

#   y
ax.set_yticks([-1,0,1])

# disable clipping of data points by axes range
# for artist in (line1,line2):
#     artist.set_clip_on(False)

# adjust spine to be within ticks
ax.spines['left'].set_bounds( -1, 1 )

show()
fig.savefig("foo.png")
