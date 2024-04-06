# Script to pre-process the name of a window

import sys
import re

window_name = sys.argv[1].strip('"').strip()

# Example of the input
#window_name = 'LIVE FACEBOOK - YouTube — Mozilla Firefox'

# We're assuming that the input has the following format
# title - program

x0 = 0
x1 = len(window_name)
y0 = 0
y1 = 0

p = re.compile('[\w\s]*$')
m = p.search(window_name)

if m != None:
	x0, x1 = m.span()

program = window_name[x0:x1].strip()

y0 = x0
y1 = x0
m = re.search('[\W\s]*$', window_name[0:x0])
if m != None:
	y0, y1 = m.span()
	
title = window_name[0:y0].strip()

# The information is sent on the stdout
print(program)
print(title)





