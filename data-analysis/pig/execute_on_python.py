#Passing PIG Script to PYTHON and RUN
#! /usr/bin/python

from org.apache.pig.scripting import Pig

P = Pig.compileFromFile("""myscript.pig""")

input = "original"
output = "output"

result = p.bind({'in':input, 'out':output}).runSingle()
if result.isSuccessful():
	print "Pig job succeeded"
else:
	raise "Pig job failed"
