import sys
import getopt
import subprocess
import StringIO

# http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html
def main(argv):
	# set option defaults
	tshark = "tshark" # uses system variable as default tshark location
	deviceID = None
	deviceName = None
	debug = False
	
	# parse command line options
	try:
		opts, args = getopt.getopt(argv, "ht:d", ["help", "tshark=", "device="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt == '-d':
			debug = True
		elif opt in ("-t", "--tshark"):
			tshark = arg
		elif opt in ("--device"):
			try:
				deviceID = int(arg)
			except ValueError:
				deviceName = arg.strip()
		args = "".join(args) # remaining arguments minus the option flags
	
	# options and arguments are parsed, perform operations
	if debug:
		print "tshark: " + tshark
	
	# make sure we have a valid capture device
	if not deviceID and not deviceName:
		print "Select a capture device with '--device=' argument:"
		print subprocess.Popen(tshark + " -D", stdout=subprocess.PIPE, shell=True).stdout.read()
	else:
		out,err = subprocess.Popen(['tshark', '-D'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
		deviceList = (err if out == "" else out)
		for line in StringIO.StringIO(deviceList).readlines():
			deviceEntry = line.split(" ")
			deviceEntryID = int(deviceEntry[0].replace(".","").strip())
			deviceEntryName = deviceEntry[1].strip()
			if(deviceName == deviceEntryName):
				break
			if(deviceID == deviceEntryID):
				deviceName = deviceEntryName
				break
		if debug:
			print "device: " + deviceName

def usage():
	print "TODO"

if __name__ == "__main__":
	main(sys.argv[1:])