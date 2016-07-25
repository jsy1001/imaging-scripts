#!/usr/bin/env python

"""Apply Gaussian taper to FITS image.

   Usage: taper [inputimage] [outputimage] [taper_fwhm_in_mas]
   
   """

_release = "rel1.1.1"

import sys
from math import *
import numpy as np
import astropy.io.fits as pyfits

def _main():
    """Main routine."""
    # Parse command line
    if len(sys.argv) == 4:
        inpfile = sys.argv[1]
        outfile = sys.argv[2]
        fwhm = float(sys.argv[3]) # in mas
    else:
        # Print usage info
        print "%s %s\n" % (sys.argv[0], _release)
        print __doc__
        sys.exit(2)

    # Read image
    hlist = pyfits.open(inpfile)
    dims = hlist[0].data.shape
    pixsize = hlist[0].header['PIXSIZE']
    print 'PIXSIZE = %f mas' % pixsize
    try:
        width = hlist[0].header['WIDTH']
        if(dims[0] != width):
            raise ValueError, 'WIDTH keyword incorrect'
        print 'WIDTH = %f mas' % width
    except KeyError:
        pass

    # Parameters:
    sigma = fwhm/pixsize/2.3548

    # Generate Gaussian
    taper = np.zeros(dims, np.float)
    tw = dims[0]
    for i in range(tw):
        for j in range(tw):
            taper[i,j] = exp(-((i-tw/2)**2+(j-tw/2)**2)/(2*sigma*sigma))

    # Taper
    print 'Tapering with sigma=%f pix...' % sigma
    result = hlist[0].data*taper
    print 'done'
    
    # Write out new FITS file
    hdu = pyfits.PrimaryHDU(result)
    hdu.header['PIXSIZE'] = (pixsize, 'Pixelation (mas')
    hdu.header['WIDTH'] = (dims[0], 'Size (pixels')
    hdu.header['HISTORY'] = 'taper %s' % inpfile
    hdu.header['HISTORY'] = ' %s %f' % (outfile, fwhm)
    hdu.writeto(outfile)


if __name__ == '__main__':
    _main()
