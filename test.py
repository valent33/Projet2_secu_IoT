import asyncio
import pyshark
import threading

def capture_packets():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    cap = pyshark.FileCapture('Données\mdk3_1h20.pcap')
    for packet in cap:
        print(packet)
        break

if __name__ == '__main__':
    t = threading.Thread(target=capture_packets)
    t.start()
    t.join()
