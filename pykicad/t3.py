#! /usr/bin/env python3

import sch
import sys

fname = 'example.kicad_sch'

if len(sys.argv) > 1:
    fname = sys.argv[1]

val = sch.Sch.from_file(fname)
print('have val')
print(val)


