import sys
import getopt
from subprocess import Popen, PIPE
import StringIO

# tssk version number
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
		args = "".join(args) # remaining arguments minus the declared options
	
	# options and arguments are parsed, perform operations
	if debug:
		print "tshark: " + tshark
		
	# if not parsing a pcap file make sure we have a valid capture device
	if not pcap:
		out,err = Popen(['tshark', '-D'], shell=False, stdout=PIPE, stderr=PIPE).communicate()
		deviceList = (err if out == "" else out).strip()
		if not deviceID and not deviceName:
			print "Specify a pcap file to parse with '--pcap=' argument or select a capture device with '--device=' argument:"
			print deviceList
			sys.exit()
		else:
			if "no interfaces" in deviceList:
				print "No capture devices available."
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
					print "capture device: " + deviceName
				
				# build a tshark capture command for capture device <deviceID>
				command = [tshark]
				command += ['-i', str(deviceID)] 
				# add libpcap capture filter
				command += ['-f', 'tcp dst port 80 or udp src port 5353 or udp src port 138']
				
				# start parsing capture traffic for sessions
				parseCapture(command, debug)
	else:
		try:
			open(pcap) # ensure that the pcap file exists
			
			if debug:
				print "capture file (pcap): " + pcap
				
			# build a tshark parser command for capture file <pcap>
			command = ['tshark']
			command += ['-r', pcap] 
			
			# start parsing the pcap file for sessions
			parseCapture(command, debug)
		except IOError:
			print "The specified pcap file does not exist."

def parseCapture(command, debug):
	# add tab seperated fields formatting
	command += ['-T', 'fields']
	command += ['-E', 'separator=/t']
	# add fields to print
	command += ['-e', 'eth.src']
	command += ['-e', 'wlan.sa']
	command += ['-e', 'ip.src']
	command += ['-e', 'ipv6.src'] 
	command += ['-e', 'tcp.srcport']
	command += ['-e', 'udp.srcport']
	command += ['-e', 'tcp.dstport']
	command += ['-e', 'udp.dstport']
	command += ['-e', 'browser.command']
	command += ['-e', 'browser.server']
	command += ['-e', 'dns.resp.name']
	command += ['-e', 'http.host']
	command += ['-e', 'http.request.uri']
	command += ['-e', 'http.accept']
	command += ['-e', 'http.accept_encoding']
	command += ['-e', 'http.user_agent']
	command += ['-e', 'http.referer']
	command += ['-e', 'http.cookie']
	command += ['-e', 'http.authorization']
	command += ['-e', 'http.authbasic']
	
	if debug:
		print "command: " + str(command)
		
	proc = None
	if debug:
		# letting error stream pass through to user, its output is good feedback
		proc = Popen(command, shell=False, stdout=PIPE)
	else:
		proc = Popen(command, shell=False, stdout=PIPE, stderr=PIPE)
		
	while True:
		data = proc.stdout.readline()
		
		# parse out data variables
		if "\t" in data:
			columns = data.split("\t")
			if len(columns) == 20:
				values = {}
				values['eth.src'] = str(columns[0])
				values['wlan.sa'] = str(columns[1])
				values['ip.src'] = str(columns[2])
				values['ipv6.src'] = str(columns[3])
				values['tcp.srcport'] = str(columns[4])
				values['udp.srcport'] = str(columns[5])
				values['tcp.dstport'] = str(columns[6])
				values['udp.dstport'] = str(columns[7])
				values['browser.command'] = str(columns[8])
				values['browser.server'] = str(columns[9])
				values['dns.resp.name'] = str(columns[10])
				values['http.host'] = str(columns[11])
				values['http.request.uri'] = str(columns[12])
				values['http.accept'] = str(columns[13])
				values['http.accept_encoding'] = str(columns[14])
				values['http.user_agent'] = str(columns[15])
				values['http.referer'] = str(columns[16])
				values['http.cookie'] = str(columns[17])
				values['http.authorization'] = str(columns[18])
				values['http.authbasic'] = str(columns[19])
				detectSession(values, debug)
				
		# end of stream
		if len(data) == 0:
			break

def detectSession(values, debug):
	print str(values)

def usage():
	print "Usage: tssk [options] ..."
	print "Configuration:"
	print "  --tshark <filepath>      sets the path to tshark"
	print "Processing:"
	print "  --pcap <filepath>        sets the path to the pcap file to parse"
	print "  --device <id or name>    sets the device on which to capture traffic"
	print "Miscellaneous:"
	print "  -h                       display this help and exit"
	print "  -v                       display version info and exit"
	print "  -d                       enable debug messages (verbose mode)"

if __name__ == "__main__":
	main(sys.argv[1:])