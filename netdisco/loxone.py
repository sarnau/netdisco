"""Loxone Miniserver discovery."""
import socket
from datetime import timedelta
import logging


BROADCAST_SEND_PORT = 7070
BROADCAST_LSTN_PORT = 7071
BROADCAST_ADDR = '<broadcast>'
DISCOVERY_PAYLOAD = b"\x00"
DISCOVERY_TIMEOUT = timedelta(seconds=3)


class Loxone:
    """Base class to discover Loxone Miniserver."""

    def __init__(self):
        """Initialize the Loxone Miniserver discovery."""
        self.entries = []  # type: List[Tuple[str]]

    def scan(self):
        """Scan the network."""
        self.update()

    def all(self):
        """Scan and return all found entries."""
        self.scan()
        return self.entries

    def update(self):
        """Scan network for Loxone Miniserver."""
        entries = []

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(DISCOVERY_TIMEOUT.seconds)
        sock.bind(("", BROADCAST_LSTN_PORT))

        try:
            sock.sendto(DISCOVERY_PAYLOAD, (BROADCAST_ADDR, BROADCAST_SEND_PORT))

            while True:
                try:
                    data, (address, _) = sock.recvfrom(1024)
                    replyStr = str(data, 'utf-8')
                    if not replyStr.startswith('LoxLIVE:'): # header correct?
                        continue
                    name = replyStr[8:].split('%s' % address)[0].strip()
                    para = replyStr.split('%s' % address)[1].split(' ')
                    #print(address,replyStr)
                    entry = {'Address':address,
                             'Name':name,
                             'Port':int(para[0][1:]),
                             'Serial':para[1],
                             'Version':para[2],
                             'Prog':(para[3]+' '+para[4])[5:],
                             'Type':para[5][5:],
                             'HwId':para[6][5:],
                             'IPv6':para[7][5:]
                             }
                    entries.append(entry)

                except socket.timeout:
                    break
                except UnicodeDecodeError:
                    # Catch invalid responses
                    logging.getLogger(__name__).debug(
                        'Ignoring invalid unicode response from %s', address)
                    continue

        finally:
            sock.close()

        self.entries = entries

def main():
    """Test Loxone Miniserver discovery."""
    from pprint import pprint
    loxone = Loxone()
    pprint("Scanning for Loxone Miniserver..")
    loxone.update()
    pprint(loxone.entries)


if __name__ == "__main__":
    main()
