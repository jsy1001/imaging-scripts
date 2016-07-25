#!/usr/bin/env python

"""Add WCS coordinates to FITS image.

   Usage: add_wcs_geo [inputimage]
   
   """

_release = "rel1.1.1"

import sys
from math import *
import astropy.io.fits as pyfits
import os.path

def _main():
    """Main routine."""
    # Parse command line
    if len(sys.argv) == 2:
        inpfile = sys.argv[1]
        outfile = os.path.splitext(inpfile)[0]+'_wcs.fits'
    else:
        # Print usage info
        print "%s %s\n" % (sys.argv[0], _release)
        print __doc__
        sys.exit(2)

    # Read image
    hlist = pyfits.open(inpfile)
    dims = hlist[0].data.shape
    hdr = hlist[0].header
    try:
        # Output from BSMEM
        pixSize = hdr['PIXSIZE']
        raSign = -1
    except:
        pixSize = hdr['PIXEL']
        raSign = +1
    print '%f mas/pix' % pixSize

    # Flip image if necessary
    if raSign == -1:
        hlist[0].data = hlist[0].data[:,::-1]
        raSign = -raSign

    # Add WCS keywords
    mas2rad = pi/180./3600./1000.
    geoPixSize = pixSize*mas2rad*36000000
    print '%f m/pix' % geoPixSize
    hdr['CTYPE1'] = 'RELATIVE RA'
    hdr['CTYPE2'] = 'RELATIVE DEC'
    hdr['CUNIT1'] = 'm'
    hdr['CUNIT2'] = 'm'
    hdr['CDELT1'] = (raSign*geoPixSize, 'm/pix at GEO')
    hdr['CDELT2'] = (geoPixSize, 'm/pix at GEO')
    hdr['CRPIX1'] = dims[0]/2
    hdr['CRPIX2'] = dims[1]/2
    hdr['CRVAL1'] = 0.0
    hdr['CRVAL2'] = 0.0

    # Write out new FITS file
    hlist.writeto(outfile)


if __name__ == '__main__':
    _main()
