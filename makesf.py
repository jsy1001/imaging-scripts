#!/usr/bin/env python

"""Blur and threshold FITS image for use as BSMEM prior model (-sf option).

   Usage: makesf [inputimage] [outputimage] [blur_fwhm_in_mas] [threshold/max]
   
   """

_release = "rel1.1.1"

import sys
from math import *
import numpy as np
import astropy.io.fits as pyfits
import scipy.signal

def _main():
    """Main routine."""
    # Parse command line
    if len(sys.argv) == 5:
        inpfile = sys.argv[1]
        outfile = sys.argv[2]
        fwhm = float(sys.argv[3]) # in mas
        frac = float(sys.argv[4])
    else:
        # Print usage info
        print "%s %s\n" % (sys.argv[0], _release)
        print __doc__
        sys.exit(2)

    # Read image
    hlist = pyfits.open(inpfile)
    dims = hlist[0].data.shape
    try:
        pixsize = hlist[0].header['PIXSIZE']
    except KeyError:
        pixsize = hlist[0].header['PIXEL']
    print 'PIXSIZE = %f mas' % pixsize
    try:
        width = hlist[0].header['WIDTH']
        if(dims[0] != width):
            raise ValueError, 'WIDTH keyword incorrect'
        print 'WIDTH = %f mas' % width
    except KeyError:
        pass
    minvalue = hlist[0].data.min()
    maxvalue = hlist[0].data.max()
    print 'min = %g' % minvalue
    print 'max = %g' % maxvalue

    # Parameters:
    sigma = fwhm/pixsize/2.3548
    threshold = frac*maxvalue
    blank = 1e-8

    # Generate Gaussian
    bw = int(6*sigma)
    blur = np.zeros((bw,bw), np.float)
    for i in range(bw):
        for j in range(bw):
            blur[i,j] = exp(-((i-bw/2)**2+(j-bw/2)**2)/(2*sigma*sigma))

    # Convolve
    print 'Blurring with sigma=%f pix...' % sigma
    result = scipy.signal.convolve(hlist[0].data, blur, 'same')
    print 'done'

    # Threshold
    print 'Thresholding at %f...' % threshold
    for i in range(dims[0]):
        for j in range(dims[1]):
            if result[i,j] < threshold:
                result[i,j] = blank
    print 'done'
    
    # Write out new FITS file
    hdu = pyfits.PrimaryHDU(result)
    hdu.header['PIXSIZE'] = (pixsize, 'Pixelation (mas')
    hdu.header['WIDTH'] = (dims[0], 'Size (pixels')
    hdu.header['HISTORY'] = 'makesf %s' % inpfile
    hdu.header['HISTORY'] = ' %s %f %f' % (outfile, fwhm, frac)
    hdu.writeto(outfile)


if __name__ == '__main__':
    _main()
