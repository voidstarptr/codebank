#!/usr/bin/env python3

import sys, os, re;

dTs = 0
oldTs=-1

for l in sys.stdin:
	l2=l.rstrip()
	t = l2.split(' ')
	if len(t) < 2:
		continue

	try:
		ts = t[1].split(':')
		if len(ts) != 3:
			continue

		tsInMs = (int(ts[0])*3600 + int(ts[1])*60 + float(ts[2]))*1000
	except (ValueError, IndexError):
		continue

	#print '%f -- %s ffffffffffffff\n' % ( tsInMs, t[1])
	if (oldTs > 0):
		dTs = tsInMs - oldTs

	#t[0]=tsInMs
	oline = "%f %f %s" % (dTs, tsInMs, " ".join(t))

	print(oline)
	oldTs = tsInMs

