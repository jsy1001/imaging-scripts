#!/usr/bin/env python

"""Flip image L-R.

   Usage: flip [inputimage] [outputimage]
   
   """

_release = "rel1.1.1"

import sys
from math import *
import pyfits
import os.path

def _main():
    """Main routine."""
    # Parse command line
    if len(sys.argv) == 3:
        inpfile = sys.argv[1]
        outfile = sys.argv[2]
    else:
        # Print usage info
        print "%s %s\n" % (sys.argv[0], _release)
        print __doc__
        sys.exit(2)

    # Read image
    hlist = pyfits.open(inpfile)

    # Flip
    hlist[0].data = hlist[0].data[:,::-1]

    # Write out new FITS file
    hlist.writeto(outfile)


if __name__ == '__main__':
    _main()
