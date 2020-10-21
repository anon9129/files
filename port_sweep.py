import subprocess
from subprocess import PIPE
import socket
import sys

if len(sys.argv) < 2:
	print("Missing Port argument!")
	sys.exit()
	
# Globals, run command
port = sys.argv[1]
iprange = "192.168.15.0/24" if len(sys.argv) < 2 else sys.argv[2]

hosts = []
good_hosts = []
cmd = "nmap -sn -oG - " + iprange
print("[SCAN] Scanning", iprange, "...", end="")
o = subprocess.run(cmd.split(" "), stdout=PIPE, stdin=PIPE, stderr=PIPE, text=True).stdout
print("done.")
for line in o.split('\n'):
	if "Up" in line:
		hosts.append(line.split(" ")[1])
print("[SCAN] Scanning up hosts(" + str(len(hosts)) + ") ...")
# Check if port is open
for host in hosts:
	s = socket.socket()
	s.settimeout(1000)
	try:
		s.connect((host, int(port)))
		good_hosts.append(host)
		s.close()
	except socket.error:
		pass
if len(good_hosts) == 0:
	print("Port", port, "Is closed on all hosts!")
print("[OPEN]Port", port, "open on", len(good_hosts), "hosts!")
for host in good_hosts:
	print("-->", host)
	

