from sys import argv
#from os.path import exists

script, from_file, to_file = argv

#print "Copying from %s to %s " % (from_file,to_file)

#We could do these two on one line too, how?
in_file = open(from_file).read()
#indata = in_file.read()

#print "The input file is %d bytes long " %len(indata)

#print "Does the output file exists? %r" % exists(to_file)
#print "Ready, hit RETURN to continue,CRTRL-C to about."
#raw_input()

out_file = open(to_file,'w').write(in_file)
#out_file.write(indata)

#print "Alright.all done."

#out_file.close()
#in_file.close()