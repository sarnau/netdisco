"""Mobile Alerts device discovery."""
import socket
from datetime import timedelta
import logging
import struct


DISCOVERY_PORT = 8003
DISCOVERY_ADDRESS = '<broadcast>'
DISCOVERY_PAYLOAD = b"\x00\x01\x00\x00\x00\x00\x00\x00\x00\x0a"
DISCOVERY_TIMEOUT = timedelta(seconds=2)


class MobileAlerts:
    """Base class to discover Mobile Alerts gateways."""

    def __init__(self):
        """Initialize the Mobile Alerts discovery."""
        self.entries = []  # type: List[Tuple[str]]

    def scan(self):
        """Scan the network."""
        self.update()

    def all(self):
        """Scan and return all found entries."""
        self.scan()
        return self.entries

    def update(self):
        """Scan network for Mobile Alerts gateways."""
        entries = []

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(DISCOVERY_TIMEOUT.seconds)
        sock.sendto(DISCOVERY_PAYLOAD, (DISCOVERY_ADDRESS, DISCOVERY_PORT))

        while True:
            try:
                data, (address, _) = sock.recvfrom(1024)
                if len(data) != 0xba:
                    continue
                type,gatewayID0,gatewayID1,gatewayID2,gatewayID3,gatewayID4,gatewayID5,length = struct.unpack('>H6BH', data[:2+6+2])
                if type != 3 or length != 0xba:
                    continue
                deviceName = str(data[28:48], 'utf-8').rstrip('\x00')
                entry = [('%02x'*6) % (gatewayID0,gatewayID1,gatewayID2,gatewayID3,gatewayID4,gatewayID5),deviceName]
                entry.insert(0, address)
                entries.append(tuple(entry))

            except socket.timeout:
                break
            except UnicodeDecodeError:
                # Catch invalid responses
                logging.getLogger(__name__).debug(
                    'Ignoring invalid unicode response from %s', address)
                continue

            self.entries = entries

        sock.close()


def main():
    """Test Mobile Alerts discovery."""
    from pprint import pprint
    mobilealerts = MobileAlerts()
    pprint("Scanning for Mobile Alerts gateways..")
    mobilealerts.update()
    pprint(mobilealerts.entries)


if __name__ == "__main__":
    main()
