from pathlib import Path
import numpy
import matplotlib.pyplot as pplt
#from scipy.stats import r
import bisect
import seaborn


#d = 3
#n = 7
#k = 4
#Al_known = numpy.array([1, 0, 0, 7, 7, 0, 0, 1], dtype=numpy.uint8)
#numSamples = 2**numpy.arange(4, 7)	# explicit word-for-word: numWords
numChunks = 1
d = 5
n = 33
k = 13
Al_known = numpy.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 165, 201, 396, 528, 495, 1155, 1155, 1155, 1155, 495, 528, 396, 201, 165, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=numpy.int32)

numSamples = 2**numpy.arange(k-5, k+2, 2)	# explicit word-for-word: numWords

doSave = True	
doShow = True
frame_off = True

# 1-
#pOnesRange = numpy.array([.95, .99, .999, .9994, .9995, .9997, .9998, .9999, .99994, .99995, .99996, .99997, .99998, .99999, .999991, .999992, .999993, .999994])
pOnesRange = numpy.array([.8, .9, .95, .98, .99, .991, .992, .993, .994, .995, .996, .997, .998, .999])
betaRange = 1-2*pOnesRange

#pOnes = numpy.arange(.75, .95, .05)
#pOnes = numpy.arange(.1, .25, .05)


numWords = 2**k

allData = numpy.zeros((len(numSamples), numWords))

dataPath = Path('./data')

settingsPath = Path.cwd()/ 'pplt_settings'


TVD = numpy.zeros((len(pOnesRange), len(numSamples)))

for p in range(len(pOnesRange)):

	pOnes = pOnesRange[p]

	for ns in range(len(numSamples)):

		dataFile = 'BCH_n' + str(n) + '_d' + str(d) + '_po' +str(pOnes) + '_numX' + str(numSamples[ns]) +'.txt'

		with open(dataPath / dataFile, 'r') as fIn:
	
			allData[ns, :] = numpy.loadtxt(fIn, delimiter='\t')

	# first row to 0 - the 0 word always happens

	allData[:, 0] = 0


	logData = allData

	for ns in range(len(numSamples)):
	
		logData[ns,:] = numpy.log( numpy.abs(allData[ns,:] )) / numpy.log(numpy.abs(1-2*pOnes))

	rlData = numpy.rint(logData).astype(numpy.dtype('uint64'))
	rlData[numpy.isinf(rlData)] = 0


	for ns in range(len(numSamples)):
	
		Al_estimate = numpy.zeros((len(Al_known),), dtype=numpy.int32)

		rlDataRow = rlData[ns,:]
		rlDataRow = rlDataRow[~numpy.isnan(rlDataRow)]
		l = numpy.unique(rlDataRow)
		
		#l = l[~numpy.isnan(l)]
		#l = l[~numpy.isinf(l)]
	
		#l[numpy.isinf(l)] = 0

		Al = numpy.zeros((len(l),), dtype=numpy.int32)
		
		for v in range(len(l)):
			if l[v] <= n:
				
				Al[v] = int(numpy.sum(rlDataRow==l[v]))

				Al_estimate[l[v]] = Al[v]

		#print 'p ' + str(p)
		#print Al_known - Al_estimate
		#print numWords - sum(Al_estimate)
		TVD[p, ns] = numpy.sum(numpy.abs(Al_known - Al_estimate))/(2*numWords)

	#print TVD[p,:]*2*numWords

colours = []

with open(settingsPath / 'colours_Japan.txt') as f:
	for line in f:
		if line.strip():	# if line not empty
			colours.append( '#' + line.split('\t')[0] )
			

pplt.style.use(str(settingsPath / 'mplstyle_two_column.mplstyle'))

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

greens = seaborn.color_palette('Greens_d', n_colors=len(pOnesRange))

#ygbd_f = seaborn.color_palette('YlGnBu_d', n_colors=len(filtr))
#ygd_f = seaborn.color_palette('YlGn_d', n_colors=len(filtr))

colormapName = 'coolwarm'

fig1 = pplt.figure()
fig1.set_size_inches(inchX, inchY, forward=True)
ax1 = fig1.gca()
#ax1.tick_params(labelsize=fontsize_ticks)

#ax1.set_title(r'BCH({0},{1},{2})'.format(n, k, d))
ax1.set_xlabel(r'$\log(1-\mathbb{P}(1))$')
ax1.set_ylabel(r'$TVD(W_l,\hat{W_l})$')

#reference = numpy.zeros((len(pOnes), n+1))

#for j in range(n+1):

#	reference[:, j] = (1-2*pOnes)**j #(-1)**j

#	reference[:, 0] = 0
	
#	ax1.plot(pOnes, reference[:, j], linewidth=linewidth_model, linestyle='', marker='o', color=colours[ numpy.mod(j, len(colours))], label=r'$\chi^{0}$'.format(j))#, cmap=pplt.get_cmap(colormapName))

#ax1.plot(range(n+1), Al_known, alpha=.75, color=colours[2], label=r'expected')
#ax1.plot(numpy.arange(n+1)[Al_known>0], Al_known[Al_known>0], alpha=.75, color=colours[7], label=r'expected')


for ns in range(len(numSamples)):

	#, linestyle='None'
	ax1.semilogx(1-pOnesRange, TVD[:,ns], color=ygbd[ns], linewidth=linewidth_data, linestyle='-', marker=pplt.matplotlib.markers.MarkerStyle.filled_markers[ns], markersize=9, label=r'$g={0}$'.format(k-int(numpy.log2(numSamples[ns]))))
	
	#for r in range(len(l)):
	
		#ax1.plot(l, Al[r], linewidth=linewidth_data, color=colours[ numpy.mod(r, len(colours))] , label=r'$\beta^{0}$'.format(r))#, cmap=pplt.get_cmap(colormapName))
	
lg1 = ax1.legend(loc=0, frameon=True)#, bbox_to_anchor=(.9,1))
#lg1.get_frame().set_alpha(1)
#ax1.set_xlim([4,25])
ax1.set_xlim([min(1-pOnesRange),max(1-pOnesRange)])
ax1.patch.set_facecolor('w')
ax1.grid(True, color='black', alpha=.1, which='both', linestyle='-')

if frame_off:
	for pos in ['right', 'top', 'bottom', 'left']:
		fig1.gca().spines[pos].set_visible(False)
		
if doSave:

	pplt.savefig( 'BCH_n' + str(n) + '_d' + str(d) + '_TVD.pdf')
	
	
if doShow:
	
	pplt.show()
