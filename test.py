import asyncio
import pyshark
import threading

def capture_packets():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    cap = pyshark.FileCapture('Données\mdk3_1h20.pcap')
    for i, p in enumerate(cap):
        for layer in p.layers:
            print("###############", layer.layer_name, "###############")
            for field in layer.field_names:
                print(field, getattr(layer, field))
        
        # print(p)
        print(i)
        break

    # Close the capture object
    cap.close()

if __name__ == '__main__':
    t = threading.Thread(target=capture_packets)
    t.start()
    t.join()
