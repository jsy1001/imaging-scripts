#!/usr/bin/env python2.7

"""Scale OIFITS visibility data.

   Usage: oiscale [inputfile] [outputfile] [vis_amp_scale_factor]

   """

_release = "rel1.1.1"

import sys
import oifits

def _main():
    """Main routine."""
    # Parse command line
    if len(sys.argv) == 4:
        inpfile = sys.argv[1]
        outfile = sys.argv[2]
        vscale = float(sys.argv[3])
    else:
        # Print usage info
        print "%s %s\n" % (sys.argv[0], _release)
        print __doc__
        sys.exit(2)

    # Write output file
    o = oifits.OiFits(inpfile)
    vis2scale = vscale*vscale
    for vis2 in o.vis2List:
        for i in range(vis2.numrec):
            for j in range(vis2.nwave):
                vis2.record[i].vis2data[j] *= vis2scale
    o.write(outfile)

if __name__ == '__main__':
    _main()
