#!/usr/bin/env python2.7

"""Resize and crop FITS image.

   Usage: imresize2 [inputimage] [outputimage] [pixsize_in_mas] [x_origin_in_pix] [y_origin_in_pix] [width_in_pix]
   
   """

_release = "rel1.1.1"

import sys
from math import *
import numpy as np
import astropy.io.fits as pyfits
import scipy.misc

def _main():
    """Main routine."""
    # Parse command line
    if len(sys.argv) == 7:
        inpfile = sys.argv[1]
        outfile = sys.argv[2]
        outpixsize = float(sys.argv[3])
        xorigin = float(sys.argv[4])
        yorigin = float(sys.argv[5])
        outwidth = float(sys.argv[6])
    else:
        # Print usage info
        print "%s %s\n" % (sys.argv[0], _release)
        print __doc__
        sys.exit(2)

    # Read image
    hlist = pyfits.open(inpfile)
    dims = hlist[0].data.shape
    pixsize = hlist[0].header['PIXSIZE']
    print 'Input PIXSIZE = %f mas' % pixsize
    try:
        width = hlist[0].header['WIDTH']
        if(dims[0] != width):
            raise ValueError, 'WIDTH keyword incorrect'
        print 'Input WIDTH = %f mas' % width
    except KeyError:
        pass

    # Resize
    if outpixsize != pixsize:
        sized = scipy.misc.imresize(hlist[0].data, pixsize/outpixsize,
                                    interp='bilinear')
    else:
        sized = hlist[0].data

    # Crop
    c = sized.shape[0]/2
    result = sized[xorigin:xorigin+outwidth,yorigin:yorigin+outwidth]
    
    # Write out new FITS file
    hdu = pyfits.PrimaryHDU(result)
    hdu.header['PIXSIZE'] = (outpixsize, 'Pixelation (mas')
    hdu.header['WIDTH'] = (outwidth, 'Size (pixels')
    hdu.header['HISTORY'] = 'imresize2 %s' % inpfile
    hdu.header['HISTORY'] = ' %s %f' % (outfile, outpixsize)
    hdu.header['HISTORY'] = ' %f %f %f' % (xorigin, yorigin, outwidth)
    hdu.writeto(outfile)


if __name__ == '__main__':
    _main()
