from pathlib import Path
import numpy
import matplotlib.pyplot as pplt
import bisect
import seaborn
import logging


#d = 3
#n = 7
#k = 4
#Al_known = numpy.array([1, 0, 0, 7, 7, 0, 0, 1], dtype=numpy.uint8)
#numSamples = 2**numpy.arange(4, 7)	# explicit word-for-word: 2**k
numChunks = 1
d = 5
n = 33
k = 13
Al_known = numpy.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 165, 201, 396, 528, 495, 1155, 1155, 1155, 1155, 495, 528, 396, 201, 165, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=numpy.uint32)

numSamples = 2**numpy.arange(k-5, k+1, 2)	# explicit word-for-word: 2**k

doSave = True
doShow = True
frame_off = True

pOnes = .95
#pOnes = numpy.arange(.75, .95, .05)
#pOnes = numpy.arange(.1, .25, .05)


allData = numpy.zeros((len(numSamples), 2**k))

dataPath = Path('./data')

settingsPath = Path.cwd()/ 'pplt_settings'


for ns in range(len(numSamples)):

	dataFile = 'BCH_n' + str(n) + '_d' + str(d) + '_po' +str(pOnes) + '_numX' + str(numSamples[ns]) +'.txt'

	with open(dataPath / dataFile, 'r') as fIn:
	
		allData[ns, :] = numpy.loadtxt(fIn, delimiter='\t')

# first row to 0 - the 0 word always happens

allData[:, 0] = 0

colours = []

with open(settingsPath / 'colours_Japan.txt') as f:
	for line in f:
		if line.strip():	# if line not empty
			colours.append( '#' + line.split('\t')[0] )
			
x = settingsPath / 'mplstyle_two_column.mplstyle'
pplt.style.use( str(x))

linewidth_data = 2
linewidth_model = 2
#fontsize_title = 20
#fontsize_axes = 20
#fontsize_ticks = 18
fontsize_legend = 16

inchX = 6
inchY = 4
#two-column APL format for single-column figures: 8.5cm width
#inchX = 3.4646
#inchY = 2.231


ygbd = seaborn.color_palette('YlGnBu_d', n_colors=len(numSamples))
yord = seaborn.color_palette('YlOrRd_d', n_colors=len(numSamples))
ygd = seaborn.color_palette('YlGn_d', n_colors=len(numSamples))
ygb = seaborn.color_palette('YlGnBu', n_colors=len(numSamples))

#ygbd_f = seaborn.color_palette('YlGnBu_d', n_colors=len(filtr))
#ygd_f = seaborn.color_palette('YlGn_d', n_colors=len(filtr))

colormapName = 'coolwarm'

fig1 = pplt.figure()
fig1.set_size_inches(inchX, inchY, forward=True)
ax1 = fig1.gca()
#ax1.tick_params(labelsize=fontsize_ticks)

#ax1.set_title(r'BCH({0},{1},{2}), $P(1)={3}$'.format(n, k, d, pOnes))
ax1.set_xlabel(r'$l$')
ax1.set_ylabel(r'$A_l$')

# plot the known distribution

ax1.plot(range(n+1), Al_known, alpha=.75, color=colours[2], label=r'$A_l$')

# transform to log base pOnes to see the actual estimated distribution

logData = allData

for ns in range(len(numSamples)):
	
	logData[ns,:] = numpy.log( numpy.abs(allData[ns,:] )) / numpy.log(numpy.abs(1-2*pOnes))

rlData = numpy.round(logData)
rlData[numpy.isinf(rlData)] = 0

barWidth = 1/4

for ns in range(len(numSamples)):
	
	rlDataRow = rlData[ns,:]
	rlDataRow = rlDataRow[~numpy.isnan(rlDataRow)]
	l = numpy.unique(rlDataRow)
	
	Al = numpy.zeros((len(l),))
	
	for v in range(len(l)):

		Al[v] = numpy.sum(rlDataRow==l[v])

	ax1.plot(l, Al, color=ygbd[ns], linewidth=1, linestyle='None', marker=pplt.matplotlib.markers.MarkerStyle.filled_markers[ns], markersize=9, label=r'$g={0}$'.format(k-int(numpy.log2(numSamples[ns]))))
	

lg1 = ax1.legend(loc=0, frameon=True)#, bbox_to_anchor=(.9,1))
ax1.set_xlim([9,n])
ax1.patch.set_facecolor('w')
ax1.grid(True, color='black', alpha=.1, which='both', linestyle='-')

if frame_off:
	for pos in ['right', 'top', 'bottom', 'left']:
		fig1.gca().spines[pos].set_visible(False)
    
if doSave:

	pplt.savefig( 'BCH_n' + str(n) + '_d' + str(d) + '_pOnes' + str(pOnes)  +'_gain_vs_known.pdf')
	
	
if doShow:
	
	pplt.show()
