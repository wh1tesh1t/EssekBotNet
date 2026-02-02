import socket, random, sys, time, hashlib, os, re
from struct import pack

def extract_server_number(byte_array):
    try:
        data_str = byte_array.decode('utf-8', errors="ignore")
    except UnicodeDecodeError:
        return None

    # TODO: Randomly we get a null in there
    pattern = r"ver #(\d+)"

    match = re.search(pattern, data_str)
    if match:
        return int(match.group(1))
    else:
        return None

def mainloop(addr, port, nick):
	sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	sock.settimeout(5)
	# getchallenge
	message = b'\xff\xff\xff\xff' + b'getchallenge\x20steam\x0a'
	sock.sendto(message, (addr, port))
	# connect
	chal = sock.recv(4096)
	chal = chal.split(b" ")[1]
	xashid = hashlib.md5(os.urandom(16)).hexdigest()
	cl_port = bytes(str(sock.getsockname()[1]), "utf8")
	cl_build = bytes(str(random.randint(3800, 3900)), "utf8")
	message = b'\xFF\xFF\xFF\xFFconnect\x2049\x20' + chal + b'\x20"\\d\\1\\v\\0.21\\b\\' + cl_build + b'\\o\\win32\\a\\i386\\uuid\\' + bytes(xashid, "utf8") + b'\\qport\\' + cl_port + b'\\ext\\1"' + b'\x20' + b'"\\cl_nopred\\0\\cl_lw\\0\\cl_lc\\0\\cl_autowepswitch\\0\\bottomcolor\\64\\cl_dlmax\\512\\cl_updaterate\\60\\model\\gordon\\rate\\25000\\topcolor\\128\\name\\' + bytes(nick, "utf8") + b'"'
	sock.sendto(message, (addr, port))

	connect2_exp = b'\xff\xff\xff\xffclient_connect \\ext\\1\\cheats\\0'
	connect2 = sock.recv(4096)
	cl_port = pack('H', int(cl_port) )
    
	if(connect2_exp in connect2):
		i = 1
		newpack = pack('!B', i) + bytes([0x00, 0x00, 0x80, 0x00, 0x00, 0x00, 0x00]) + cl_port +  bytes([0x03, 0x6E, 0x65, 0x77, 0x00, 0x01])
		sock.sendto(newpack, (addr, port))
		packet2 = sock.recv(4096)
		time.sleep(0.1)
		i = 2
		newpack2 = pack('!B', i) + bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]) + cl_port +  bytes([0x01, 0x01, 0x01, 0x01, 0x01, 0x01])
		sock.sendto(newpack2, (addr, port))
		packet3 = sock.recv(4096)
		i = 5
		newpack2 = pack('!B', i) + bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]) + cl_port +  bytes([0x01, 0x01, 0x01, 0x01, 0x01, 0x01])
		sock.sendto(newpack2, (addr, port))
		packet4 = sock.recv(4096)
		i = 6
		newpack2 = pack('!B', i) + bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]) + cl_port +  bytes([0x01, 0x01, 0x01, 0x01, 0x01, 0x01])
		sock.sendto(newpack2, (addr, port))
		packet5 = sock.recv(4096)
		i = 7
		newpack2 = pack('!B', i) + bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]) + cl_port +  bytes([0x01, 0x01, 0x01, 0x01, 0x01, 0x01])
		sock.sendto(newpack2, (addr, port))

		server_num = None
		# It should always be packet3 but just to be sure
		server_num = extract_server_number(packet2)
		if server_num is None:
			server_num = extract_server_number(packet3)
			if server_num is None:
				server_num = extract_server_number(packet4)
				if server_num is None:
					server_num = extract_server_number(packet5)
					if server_num is None:
						server_num = None
		i = 44
		n = 0
		m = None
		lets_gtfo = False
		max_cycles = 1 #random.randint(2, 5); # 254
		lactpacketid = 0
		while True:
			if(i == 256):
				i = 0
				n += 1
			print("CL ",str(i),"/",str(n)," ==> ")
			if( m is None ):
				newpack2 = pack('!B', int(i)) + pack('!B', int(n)) +  bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00]) + cl_port +  bytes([0x01, 0x01, 0x01, 0x01, 0x01, 0x01])
			else:
				newpack2 = pack('!B', int(i)) + pack('!B', int(n)) +  bytes([0x00, 0x00, 0x00, 0x00, 0x00]) + pack('!B', int(m)) + cl_port +  bytes([0x01, 0x01, 0x01, 0x01, 0x01, 0x01])

			newpack2 = newpack2[:4] + pack('!B', int(lactpacketid)) + newpack2[4+1:] 
			sock.sendto(newpack2, (addr, port))
			lactpacket = sock.recv(4096)
			# Fuckery for AMXX to get server number...
			if(b'* Privileges set' in lactpacket):
				m = lactpacket[7]

			# Try get the server number later if we failed with usual hello packets
			if server_num is None:
				server_num = extract_server_number(lactpacket)

			lactpacket_i = lactpacket[0]
			lactpacket_n = lactpacket[1]
			lactpacketid = lactpacket[4]
			if(lactpacket_i == 255 and lactpacket_n == 255):
				print("Server told us to fuck off...")
				return 2
			print("SV ",str(lactpacket_i),"/",str(lactpacket_n)," <== ")
#			time.sleep(0.005)
			i += 1
			if(i == 80 and n == 0):
				newpack2 = pack('!B', int(i)) + bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]) + cl_port +  bytes([0x03, 0x6E, 0x65, 0x77, 0x00, 0x01])
				newpack2 = newpack2[:4] + pack('!B', int(lactpacketid)) + newpack2[4+1:] 
				sock.sendto(newpack2, (addr, port))
				i += 1
			# spawn
			if(i == 100 and n == 0):
				# We filed to get server number from banner, trigger disconnect
				if server_num is None:
					print("We didnt get a server number, time to GTFO")
					lets_gtfo = True
					continue
				paddin = ""
				if server_num < 10:
					paddin = " "
				newpack2 = pack('!B', int(i)) + pack('!B', int(n)) + bytes([0x00, 0xC0, 0x21, 0x04, 0x00, 0x00]) + cl_port +  bytes([0x01, 0x01, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x50, 0x00, 0x00, 0x00, 0x00, 0x03, 0x73, 0x70, 0x61, 0x77, 0x6E, 0x20])  + bytes(paddin+str(server_num), "utf8") + bytes([0x00])
				newpack2 = newpack2[:4] + pack('!B', int(lactpacketid)) + newpack2[4+1:] 
				sock.sendto(newpack2, (addr, port))
				i += 1
			# begin
			if(i == 120 and n == 0):
				newpack2 = pack('!B', int(i)) + pack('!B', int(n)) + bytes([0x00, 0x80, 0x9F, 0x00, 0x00, 0x00]) + cl_port +  bytes([0x03, 0x62, 0x65, 0x67, 0x69, 0x6E, 0x00])
				newpack2 = newpack2[:4] + pack('!B', int(lactpacketid)) + newpack2[4+1:] 
				sock.sendto(newpack2, (addr, port))
				i += 1
			# Scream in chat
			if(i == 32 and n == 1):
				donkey = bytes([0x45, 0x73, 0x65, 0x6B, 0x20, 0x33, 0x31, 0x20, 0x6F, 0x79, 0x75, 0x6E, 0x63, 0x75, 0x79, 0x75, 0x20, 0x64, 0x6F, 0x6C, 0x64, 0x75, 0x72, 0x64, 0x75, 0x20, 0x76, 0x65, 0x20, 0x79, 0x65, 0x64, 0x69, 0x20])
				chatmsg62 = b'A'
				newpack2 = pack('!B', int(i)) + pack('!B', int(n)) + bytes([0x00, 0x80, 0xA9, 0x03, 0x00, 0x80]) + cl_port +  bytes([0x03, 0x73 ,0x61, 0x79, 0x20]) + chatmsg62 + bytes([ 0x00, 0x02, 0x1D, 0x00, 0x0A, 0x06, 0xC9 ,0x3C, 0x48, 0x9F, 0x84, 0x25, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ,0x00, 0x00, 0x00, 0x00, 0x00, 0x88, 0x00, 0x00, 0x3C, 0x00, 0x00, 0x00 ,0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ,0x08, 0x52, 0x01])
				newpack2 = newpack2[:4] + pack('!B', int(lactpacketid)) + newpack2[4+1:] 
				sock.sendto(newpack2, (addr, port))
				i += 1
			# my work is done here, *leaves*
			if(n > max_cycles or lets_gtfo):
				print("Sending disconnect...")
				discon = pack('!B', int(i)) + pack('!B', int(n)) + bytes([0x00, 0x00, 0xFF, 0x00, 0x00, 0x80]) + cl_port +  bytes([ 0x03, 0x64, 0x69, 0x73, 0x63, 0x6F, 0x6E, 0x6E, 0x65, 0x63, 0x74, 0x00])
				discon = discon[:4] + pack('!B', int(lactpacketid)) + discon[4+1:] 
				sock.sendto(discon, (addr, port))
				return 3
	else:
		print("Connect failed (no client_connect received)")
		print(connect2)
		return 1

def read_names(filename="names.txt"):
    try:
        with open(filename, 'r') as file:
            # read lines and remove trailing whitespace
            names = [line.strip() for line in file]
        return names
    except FileNotFoundError:
        print("Error: The file " +filename+" was not found.")
        return []
    except Exception as e:
        print("An error occurred: " + str(e))
        return []

names = read_names()
while True:
	print("Trying to connect")
	try:
		result = mainloop(sys.argv[1], int(sys.argv[2]), names[random.randint(0,len(names)-1)])
		if(result == 1):		# We didnt get client_connect, server full or we are blocked
			time.sleep( random.randint(15, 30) )
		if(result == 2):		# We got kicked
			time.sleep( random.randint(10, 15) )
		if(result == 3):		# Work finished ok
			time.sleep( random.randint(5, 10) )
	except Exception as ex:
		print("Caught exception: " + str(ex))
		time.sleep( 1 )

