import socket, random, sys, time, hashlib, os
from struct import pack

def Killshit(addr, port, nick):
	sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	sock.settimeout(5)
	# getchallenge
	message = b'\xff\xff\xff\xff' + b'getchallenge'
	sock.sendto(message, (addr, port))
	# connect
	chal = sock.recv(4096)[14:]
	xashid = hashlib.md5(os.urandom(16)).hexdigest()
	cl_port = bytes(str(sock.getsockname()[1]), "utf8")
	message = b'\xFF\xFF\xFF\xFF\x63\x6F\x6E\x6E\x65\x63\x74\x20\x34\x38\x20' + cl_port + b'\x20' + chal + b' "\\cl_lc\\0\\cl_lw\\0\\cl_maxpacket\\100\\cl_maxpayload\\100\\cl_msglevel\\0\\cl_nopred\\1\\cl_predict\\1\\cl_updaterate\\30\\hltv\\0\\hud_classautokill\\1\\model\\hgrunt\\name\\'+ bytes(nick, "utf8") + b'\\rate\\25000\\topcolor\\0" 2 \\d\\2\\v\\0.19.2\\b\\1200\\o\\Android\\a\\arm\\i\\' + bytes(xashid, "utf8") 
	sock.sendto(message, (addr, port))
	connect2_exp = bytes([0xFF, 0xFF, 0xFF, 0xFF, 0x63, 0x6C, 0x69, 0x65, 0x6E, 0x74, 0x5F, 0x63, 0x6F, 0x6E, 0x6E, 0x65, 0x63, 0x74, 0x20, 0x32, 0x0A])
	connect2 = sock.recv(4096)
	cl_port = pack('H', int(cl_port) )
	if(connect2 == connect2_exp):
		i = 1
		newpack  = pack('!B', i) + bytes([0x00, 0x00, 0x80, 0x00, 0x00, 0x00, 0x00]) + cl_port +  bytes([0x03, 0x6E, 0x65, 0x77, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00])
		sock.sendto(newpack, (addr, port))
		time.sleep(0.1)
		i = 2
		newpack2 = pack('!B', i) + bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]) + cl_port +  bytes([0x02, 0x00, 0x00, 0x00, 0x00, 0x01])
		sock.sendto(newpack2, (addr, port))
		packet3 = sock.recv(4096)
		i = 5
		newpack2 = pack('!B', i) + bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]) + cl_port +  bytes([0x02, 0x00, 0x00, 0x00, 0x00, 0x01])
		sock.sendto(newpack2, (addr, port))
		packet4 = sock.recv(4096)
		i = 6
		newpack2 = pack('!B', i) + bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]) + cl_port +  bytes([0x02, 0x00, 0x00, 0x00, 0x00, 0x01])
		sock.sendto(newpack2, (addr, port))
		packet5 = sock.recv(4096)
		i = 7
		newpack2 = pack('!B', i) + bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]) + cl_port +  bytes([0x02, 0x00, 0x00, 0x00, 0x00, 0x01])
		sock.sendto(newpack2, (addr, port))
		print(packet3.hex()) # Hello1
		print(packet4.hex()) # Hello2
		print(packet5.hex()) # Hello3
		i = 8
		n = 0
		max_cycles = random.randint(20, 35); # 254
		lactpacketid = 0
		while True:
			if(i == 256):
				i = 0
				n += 1
			#print(f"CL {i}/{n} ==> ")
			newpack2 = pack('!B', int(i)) + pack('!B', int(n)) +  bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00]) + cl_port +  bytes([0x02, 0x00, 0x00, 0x00, 0x00, 0x01])
			newpack2 = newpack2[:4] + pack('!B', int(lactpacketid)) + newpack2[4+1:] 
			sock.sendto(newpack2, (addr, port))
			lactpacket = sock.recv(4096)
			lactpacket_i = lactpacket[0]
			lactpacket_n = lactpacket[1]
			lactpacketid = lactpacket[4]
			if(lactpacket_i == 255 and lactpacket_n == 255):
				print("Server told us to fuck off...")
				return 2
			#print(f"SV {lactpacket_i}/{lactpacket_n} <== ")
			time.sleep(0.2)
			i += 1
			if(i == 16):
				newpack2 = pack('!B', int(i)) + pack('!B', int(n)) + bytes([0x00, 0x80, 0xFF, 0x00, 0x00, 0x80]) + cl_port +  bytes([0x03, 0x67, 0x65, 0x74, 0x72, 0x65, 0x73, 0x6F, 0x75, 0x72, 0x63, 0x65, 0x6C, 0x69, 0x73, 0x74, 0x00, 0x02, 0xBF, 0x00, 0x00, 0x00])
				newpack2 = newpack2[:4] + pack('!B', int(lactpacketid)) + newpack2[4+1:] 
				sock.sendto(newpack2, (addr, port))
				i += 1
			if(n > max_cycles):
				print("Sending disconnect...")
				discon = pack('!B', int(i)) + pack('!B', int(n)) + bytes([0x00, 0x00, 0xFF, 0x00, 0x00, 0x80]) + cl_port +  bytes([ 0x03, 0x64, 0x69, 0x73, 0x63, 0x6F, 0x6E, 0x6E, 0x65, 0x63, 0x74, 0x00])
				discon = discon[:4] + pack('!B', int(lactpacketid)) + discon[4+1:] 
				sock.sendto(discon, (addr, port))
				return 3
	else:
		print("Connect failed (no client_connect received)")
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

time.sleep( random.randint(10,60) )
while True:
	print("Trying to connect")
	sleeptime = int(sys.argv[3])
	try:
		result = Killshit(sys.argv[1], int(sys.argv[2]), names[random.randint(0,len(names)-1)])
		if(result == 1):
			time.sleep( 30 ) # Connect fail
		if(result == 2):
			time.sleep( 30 ) # Kicked
		if(result == 3):
			time.sleep( 30 ) # Finished ok
	except Exception as ex:
		print("Caught exception: " + str(ex))
		time.sleep( 10 )
