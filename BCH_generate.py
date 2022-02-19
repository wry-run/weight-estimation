from estimate_characteristic_function import *
from pathlib import Path
import numpy
import logging
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d:%H:%M:%S', level=logging.DEBUG)
logger = logging.getLogger(__name__)

doShow = True

d = 5
n = 33
k = 13
#d = 3
#n = 7
#k = 4

# .95, .99, .999, .9994, .9995, .9997, .9998, .9999, .99994, .99995, .99996, .99997, .99999
pOnes = [.8, .9, .95, .98, .99, .991, .992, .993, .994, .995, .996, .997, .998, .999]
# pOnes = [1-.999]

# Choose how many random samples to compress.
# Each sample consists of a column vector x of n i.i.d. random numbers,
# compressed to y=Gx
# An explicit word-for-word computation of each codeword would involve
# iterating through each of the 2**k possible values of y and computing (y^T) G
# so 2**k samples is break-even effort with brute force, in a probabilistic sense

#numSamples = [2**(k-4)]
numSamples = 2**numpy.arange(k-5, k+2, 2)

# working directory
dataFolder = Path('./data')
if not dataFolder.exists():
	dataFolder.mkdir()
	
for ns in numSamples:

	for p1 in pOnes:
		
		# estimate characteristic function

		char_Y = estimate_characteristic_function(n, d, p1, ns)

		# save output data to file

		dataFile = 'BCH_n' + str(n) + '_d' + str(d) + '_po' +str(p1) + '_numX' + str(ns) +'.txt'

		with open(dataFolder / dataFile, 'w') as fOut:

			numpy.savetxt(fOut, char_Y, delimiter='\t')
			fOut.write('\n')
		






