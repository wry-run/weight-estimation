#!/usr/bin/sage -python

from sage.all import *
import numpy
from scipy.linalg import hadamard
import time
import logging
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d:%H:%M:%S', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def estimate_characteristic_function(n, d, pOnes, numSamples):

	logging.debug(f'Time now: {time.asctime(time.localtime())}')
	start_time = time.time()

	# TODO: Since 2**k vectors of size n could be a rather large amount of data,
	# considering that the algorithm doesn't need to process it all at once,
	# we could split the computation into chunks, if necessary

	numColumns = numSamples
	numChunks = 1	#int(numpy.floor(byteCount/chunkSize))
	#chunkSize = numColumns*n
	#numSamples = numColumns*numChunks	#len(data_all)

	# initialize the code generator matrix

	F = GF(2)
	C = codes.BCHCode(F, n, d, b=1)
	G = C.generator_matrix() # C.generator_matrix_systematic() #.numpy().astype(numpy.uint8)
	k = C.dimension()

	logging.info(f'Code generator matrix: {C}')
	logging.info(f'k = {k}')
	logging.info(f'Weight distribution: {C.weight_distribution()}')

	twos = (2**numpy.arange(k)*numpy.ones([8*numColumns, k], dtype=numpy.uint64)).transpose()

	counts = numpy.zeros([numChunks, 2**k], dtype=numpy.uint64)

	for c in range(numChunks):

		# generate random x
		data = Matrix(F, n, 8*numColumns, lambda i,j: (numpy.random.uniform()<pOnes))
		
		# compute y = Gx
		out = G*data
		
		# map each y to an integer

		outInt = numpy.sum(out.numpy(dtype=numpy.uint64)*twos, axis=0, dtype=numpy.uint64)
		
		# check which unique integers appeared in the result
		u = numpy.unique(outInt)

		# count the number of times each integer appeared 

		for ui in range(len(u)):
			
			counts[c, u[ui]] = numpy.sum(outInt == u[ui])

	logging.debug(f'Run time (s): {time.time() - start_time}')

	# probability density function

	pdf_Y = numpy.sum( counts, axis=0) / (numChunks*8*numColumns)

	H = hadamard(2**k)

	# characteristic function

	char_Y = H.dot(pdf_Y)

	return char_Y
