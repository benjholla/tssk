import sys
import getopt
import subprocess
import StringIO

version = "0.1"

def main(argv):
	
	# set option defaults
	tshark = "tshark" # uses system variable as default tshark location
	deviceID = None
	deviceName = None
	pcap = None
	debug = False
	
	# parse command line options
	try:
		opts, args = getopt.getopt(argv, "hvd", ["help", "version", "tshark=", "device=", "pcap="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		if opt in ("-v", "--version"):
			print "tssk version " + version
			sys.exit()
		elif opt == '-d':
			debug = True
		elif opt in ("--tshark"):
			tshark = arg
		elif opt in ("--pcap"):
			pcap = arg
		elif opt in ("--device"):
			try:
				deviceID = int(arg)
			except ValueError:
				deviceName = arg.strip()
		args = "".join(args) # remaining arguments minus the option flags
	
	# options and arguments are parsed, perform operations
	if debug:
		print "tshark: " + tshark
	
	# if not parsing a pcap file make sure we have a valid capture device
	if not pcap:
		out,err = subprocess.Popen(['tshark', '-D'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
		deviceList = (err if out == "" else out).strip()
		if not deviceID and not deviceName:
			print "Specify a pcap file to parse with '--pcap=' argument or select a capture device with '--device=' argument:"
			print deviceList
			sys.exit()
		else:
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
			# start capturing traffic on selected device
	else:
		# start parsing the pcap file for sessions
		try:
			open(pcap) # ensure that the file exists
			
		except IOError:
			print "The specified pcap file does not exist."

def usage():
	print "Usage: tssk [options] ..."
	print "Configuration:"
	print "  --tshark                 sets the path to tshark"
	print "Processing:"
	print "  --pcap                   sets the path to the pcap file to parse"
	print "  --device <id or name>    sets the device on which to capture traffic"
	print "Miscellaneous:"
	print "  -h                       display this help and exit"
	print "  -v                       display version info and exit"
	print "  -d                       enable debug messages"

if __name__ == "__main__":
	main(sys.argv[1:])