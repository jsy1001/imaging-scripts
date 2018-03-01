#!/usr/bin/env python2.7

"""Edit OIFITS error bars.

   Usage: oierror [inputfile] [outputfile] [v2a] [v2b] [t3ampa] [t3ampb] [t3phia] [t3phib]

   """

_release = "rel1.1.1"

import sys
import oifits

def _main():
    """Main routine."""
    # Parse command line
    if len(sys.argv) == 9:
        inpfile = sys.argv[1]
        outfile = sys.argv[2]
        v2a = float(sys.argv[3])
        v2b = float(sys.argv[4])
        t3ampa = float(sys.argv[5])
        t3ampb = float(sys.argv[6])
        t3phia = float(sys.argv[7])
        t3phib = float(sys.argv[8])
    else:
        # Print usage info
        print "%s %s\n" % (sys.argv[0], _release)
        print __doc__
        sys.exit(2)

    # Write output file
    o = oifits.OiFits(inpfile)
    for vis2 in o.vis2List:
        for i in range(vis2.numrec):
            for j in range(vis2.nwave):
                v2e = vis2.record[i].vis2err[j]
                vis2.record[i].vis2err[j] = v2a*v2e + v2b
    for t3 in o.t3List:
        for i in range(t3.numrec):
            for j in range(t3.nwave):
                t3ampe = t3.record[i].t3amperr[j]
                t3.record[i].t3amperr[j] = t3ampa*t3ampe + t3ampb
                t3phie = t3.record[i].t3phierr[j]
                t3.record[i].t3phierr[j] = t3phia*t3phie + t3phib
    o.write(outfile)

if __name__ == '__main__':
    _main()
