# 49 protocol only!

import socket, random, sys, time, hashlib, os, re, threading, argparse
from struct import pack
from queue import Queue, Empty

active_connections = 0
connections_lock = threading.Lock()

# Extract essek server ver number
def extract_server_number(byte_array):
    try:
        data_str = byte_array.decode('utf-8', errors="ignore")
    except UnicodeDecodeError:
        return None
    pattern = r"ver #(\d+)"
    match = re.search(pattern, data_str)
    if match:
        return int(match.group(1))
    else:
        return None

# Check names
def read_names(filename="names.txt"):
    try:
        with open(filename, 'r') as file:
            names = [line.strip() for line in file if line.strip()]
        return names
    except FileNotFoundError:
        return ["Player" + str(i) for i in range(1, 21)]
    except Exception as e:
        return ["Player" + str(i) for i in range(1, 21)]

# Check chat messages
def read_chat_messages(filename="chat.txt"):
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
            messages = [line.strip() for line in file if line.strip()]
        return messages
    except FileNotFoundError:
        return ["AAAAAA", "BBBBBB", "CCCCCC", "DDDDDD", "EEEEEE"]
    except Exception as e:
        return ["AAAAAA", "BBBBBB", "CCCCCC", "DDDDDD", "EEEEEE"]

# Try to parse server list
def parse_server_list(server_strings):
    servers = []
    for s in server_strings:
        if ':' in s:
            addr, port = s.rsplit(':', 1)
            servers.append((addr, int(port)))
        else:
            servers.append((s, 27015))
    return servers

# Try to parse essek build
def parse_build_version(build_arg):
    if '-' in build_arg:
        low, high = map(int, build_arg.split('-'))
        return ('randomB', low, high)
    else:
        return ('staticA', int(build_arg), None)

# General Loop
def mainloop(addr, port, nick, chat_queue, build_version, platform, arch, worker_id=0):
    global active_connections
    with connections_lock:
        active_connections += 1
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    sock.settimeout(5)
    try:
        message = b'\xff\xff\xff\xff' + b'getchallenge\x20steam\x0a'
        sock.sendto(message, (addr, port))
        chal = sock.recv(4096)
        chal = chal.split(b" ")[1]
        xashid = hashlib.md5(os.urandom(16)).hexdigest()
        cl_port = bytes(str(sock.getsockname()[1]), "utf8")
        
        # Generate Essek build
        mode, val1, val2 = build_version
        if mode == 'staticA':
            cl_build = bytes(str(val1), "utf8")
        else:
            cl_build = bytes(str(random.randint(val1, val2)), "utf8")
        
        message = b'\xFF\xFF\xFF\xFFconnect\x2049\x20' + chal + b'\x20"\\d\\1\\v\\0.21\\b\\' + cl_build + b'\\o\\' + bytes(platform, "utf8") + b'\\a\\' + bytes(arch, "utf8") + b'\\uuid\\' + bytes(xashid, "utf8") + b'\\qport\\' + cl_port + b'\\ext\\1"' + b'\x20' + b'"\\cl_nopred\\0\\cl_lw\\0\\cl_lc\\0\\cl_autowepswitch\\0\\bottomcolor\\64\\cl_dlmax\\512\\cl_updaterate\\60\\model\\gordon\\rate\\25000\\topcolor\\128\\name\\' + bytes(nick, "utf8") + b'"'
        sock.sendto(message, (addr, port))
        connect2_exp = b'\xff\xff\xff\xffclient_connect \\ext\\1\\cheats\\0'
        connect2 = sock.recv(4096)
        cl_port_packed = pack('H', int(cl_port))
        if(connect2_exp in connect2):
            i = 1
            newpack = pack('!B', i) + bytes([0x00, 0x00, 0x80, 0x00, 0x00, 0x00, 0x00]) + cl_port_packed +  bytes([0x03, 0x6E, 0x65, 0x77, 0x00, 0x01])
            sock.sendto(newpack, (addr, port))
            packet2 = sock.recv(4096)
            time.sleep(0.1)
            i = 2
            newpack2 = pack('!B', i) + bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]) + cl_port_packed +  bytes([0x01, 0x01, 0x01, 0x01, 0x01, 0x01])
            sock.sendto(newpack2, (addr, port))
            packet3 = sock.recv(4096)
            i = 5
            newpack2 = pack('!B', i) + bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]) + cl_port_packed +  bytes([0x01, 0x01, 0x01, 0x01, 0x01, 0x01])
            sock.sendto(newpack2, (addr, port))
            packet4 = sock.recv(4096)
            i = 6
            newpack2 = pack('!B', i) + bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]) + cl_port_packed +  bytes([0x01, 0x01, 0x01, 0x01, 0x01, 0x01])
            sock.sendto(newpack2, (addr, port))
            packet5 = sock.recv(4096)
            i = 7
            newpack2 = pack('!B', i) + bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]) + cl_port_packed +  bytes([0x01, 0x01, 0x01, 0x01, 0x01, 0x01])
            sock.sendto(newpack2, (addr, port))
            server_num = None
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
            max_cycles = 1
            lactpacketid = 0
            while True:
                if(i == 256):
                    i = 0
                    n += 1
                print(f"[{worker_id}] CL {i}/{n} ==> (Active: {active_connections})")
                if( m is None ):
                    newpack2 = pack('!B', int(i)) + pack('!B', int(n)) +  bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00]) + cl_port_packed +  bytes([0x01, 0x01, 0x01, 0x01, 0x01, 0x01])
                else:
                    newpack2 = pack('!B', int(i)) + pack('!B', int(n)) +  bytes([0x00, 0x00, 0x00, 0x00, 0x00]) + pack('!B', int(m)) + cl_port_packed +  bytes([0x01, 0x01, 0x01, 0x01, 0x01, 0x01])
                newpack2 = newpack2[:4] + pack('!B', int(lactpacketid)) + newpack2[4+1:] 
                sock.sendto(newpack2, (addr, port))
                lactpacket = sock.recv(4096)
                if(b'* Privileges set' in lactpacket):
                    m = lactpacket[7]
                if server_num is None:
                    server_num = extract_server_number(lactpacket)
                lactpacket_i = lactpacket[0]
                lactpacket_n = lactpacket[1]
                lactpacketid = lactpacket[4]
                print(f"[{worker_id}] SV {lactpacket_i}/{lactpacket_n} <== (Active: {active_connections})")
                if(lactpacket_i == 255 and lactpacket_n == 255):
                    return 2
                i += 1
                if(i == 80 and n == 0):
                    newpack2 = pack('!B', int(i)) + bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]) + cl_port_packed +  bytes([0x03, 0x6E, 0x65, 0x77, 0x00, 0x01])
                    newpack2 = newpack2[:4] + pack('!B', int(lactpacketid)) + newpack2[4+1:] 
                    sock.sendto(newpack2, (addr, port))
                    i += 1
                if(i == 100 and n == 0):
                    if server_num is None:
                        lets_gtfo = True
                        continue
                    paddin = ""
                    if server_num < 10:
                        paddin = " "
                    newpack2 = pack('!B', int(i)) + pack('!B', int(n)) + bytes([0x00, 0xC0, 0x21, 0x04, 0x00, 0x00]) + cl_port_packed +  bytes([0x01, 0x01, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x50, 0x00, 0x00, 0x00, 0x00, 0x03, 0x73, 0x70, 0x61, 0x77, 0x6E, 0x20])  + bytes(paddin+str(server_num), "utf8") + bytes([0x00])
                    newpack2 = newpack2[:4] + pack('!B', int(lactpacketid)) + newpack2[4+1:] 
                    sock.sendto(newpack2, (addr, port))
                    i += 1
                if(i == 120 and n == 0):
                    newpack2 = pack('!B', int(i)) + pack('!B', int(n)) + bytes([0x00, 0x80, 0x9F, 0x00, 0x00, 0x00]) + cl_port_packed +  bytes([0x03, 0x62, 0x65, 0x67, 0x69, 0x6E, 0x00])
                    newpack2 = newpack2[:4] + pack('!B', int(lactpacketid)) + newpack2[4+1:] 
                    sock.sendto(newpack2, (addr, port))
                    i += 1
                if(i == 32 and n == 1):
                    try:
                        chatmsg = chat_queue.get(timeout=0.5)
                        chat_queue.put(chatmsg)
                        chatmsg_bytes = chatmsg.encode('utf-8', errors='ignore')[:62]
                        padding = b'\x00' * (62 - len(chatmsg_bytes))
                        chatmsg62 = chatmsg_bytes + padding
                    except Empty:
                        chatmsg62 = b'A'*62
                    newpack2 = pack('!B', int(i)) + pack('!B', int(n)) + bytes([0x00, 0x80, 0xA9, 0x03, 0x00, 0x80]) + cl_port_packed +  bytes([0x03, 0x73 ,0x61, 0x79, 0x20]) + chatmsg62 + bytes([ 0x00, 0x02, 0x1D, 0x00, 0x0A, 0x06, 0xC9 ,0x3C, 0x48, 0x9F, 0x84, 0x25, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ,0x00, 0x00, 0x00, 0x00, 0x00, 0x88, 0x00, 0x00, 0x3C, 0x00, 0x00, 0x00 ,0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ,0x08, 0x52, 0x01])
                    newpack2 = newpack2[:4] + pack('!B', int(lactpacketid)) + newpack2[4+1:] 
                    sock.sendto(newpack2, (addr, port))
                    i += 1
                if(n > max_cycles or lets_gtfo):
                    discon = pack('!B', int(i)) + pack('!B', int(n)) + bytes([0x00, 0x00, 0xFF, 0x00, 0x00, 0x80]) + cl_port_packed +  bytes([ 0x03, 0x64, 0x69, 0x73, 0x63, 0x6F, 0x6E, 0x6E, 0x65, 0x63, 0x74, 0x00])
                    discon = discon[:4] + pack('!B', int(lactpacketid)) + discon[4+1:] 
                    sock.sendto(discon, (addr, port))
                    return 3
        else:
            return 1
    except socket.timeout:
        return 1
    except Exception:
        return 1
    finally:
        sock.close()
        with connections_lock:
            active_connections -= 1

# Create essek client
def client_worker(servers, nick_queue, chat_queue, build_version, platform, arch, worker_id, stop_event):
    while not stop_event.is_set():
        try:
            nick = nick_queue.get(timeout=1.0)
            nick_queue.put(nick)
            server = random.choice(servers)
            addr, port = server
            result = mainloop(addr, port, nick, chat_queue, build_version, platform, arch, worker_id)
            if result == 1:
                time.sleep(random.uniform(15, 30))
            elif result == 2:
                time.sleep(random.uniform(10, 15))
            elif result == 3:
                time.sleep(random.uniform(5, 10))
        except Empty:
            continue
        except Exception:
            time.sleep(1.0)
        if stop_event.is_set():
            break

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('servers', nargs='+')
    parser.add_argument('-c', '--connections', type=int, default=5)
    parser.add_argument('-d', '--delay', type=float, default=0.2)
    parser.add_argument('-n', '--names-file', default='names.txt')
    parser.add_argument('-m', '--chat-file', default='chat.txt')
    parser.add_argument('-b', '--build', default='3800-3900', help='Essekbuild version: Example: 3555 or 3555-4000')
    parser.add_argument('-p', '--platform', default='win32', help='Essek platform: Example: win32, linux, android, etc.')
    parser.add_argument('-a', '--arch', default='i386', help='Essek arch: Example: i386, i686, arm64, etc.')
    args = parser.parse_args()
    servers = parse_server_list(args.servers)
    print(f"Loaded {len(servers)} servers:")
    for i, (addr, port) in enumerate(servers):
        print(f"  [{i}] {addr}:{port}")
    names = read_names(args.names_file)
    if not names:
        sys.exit(1)
    print(f"Loaded {len(names)} nicknames from '{args.names_file}'")
    chat_messages = read_chat_messages(args.chat_file)
    print(f"Loaded {len(chat_messages)} messages from '{args.chat_file}'")
    build_version = parse_build_version(args.build)
    print(f"EssekClient's build {args.build}")
    print(f"Platform: {args.platform} / Arch: {args.arch}")
    nick_queue = Queue()
    for name in names:
        nick_queue.put(name)
    chat_queue = Queue()
    for msg in chat_messages:
        chat_queue.put(msg)
    stop_event = threading.Event()
    workers = []
    for i in range(args.connections):
        worker = threading.Thread(target=client_worker, args=(servers, nick_queue, chat_queue, build_version, args.platform, args.arch, i, stop_event), daemon=True)
        worker.start()
        workers.append(worker)
        time.sleep(args.delay)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()
        for w in workers:
            w.join(timeout=3.0)
        sys.exit(0)

if __name__ == "__main__":
    main()
