import asyncio
import pyshark
import threading
import pandas as pd

df = pd.DataFrame(columns=["packet_length", "header_length", "subtype", "duration", "datarate", "class"])

def capture_packets():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    cap = pyshark.FileCapture('Données\mdk3_1h20.pcap')#, display_filter='frame.number > 170000')
    
    # frame 177229 attack started
    start_frame = 177229
    # frame 184365 attack terminated
    end_frame = 184365
    
    # cap = pyshark.FileCapture('Données\\bruteforce_12min.pcap')

    # # frame  attack started
    # start_frame = 1
    # # frame  attack terminated
    # end_frame = 1

    global df

    for i, p in enumerate(cap):
        # print("############# PACKET n°", i, " #############")
        # for layer in p.layers:
        #     print("###############", layer.layer_name, "###############")
        #     for field in layer.field_names:
        #         print(field, getattr(layer, field))

        # print(p)

        df.loc[i, "packet_length"] = p.length #
        df.loc[i, "header_length"] = p.radiotap.length # bytes
        df.loc[i, "subtype"] = p.wlan.fc_type_subtype # to categorical
        df.loc[i, "duration"] = p.wlan.duration # microseconds
        df.loc[i, "datarate"] = p.wlan_radio.data_rate # Mbps
        
        if i >= start_frame and i <= end_frame:
            df.loc[i, "class"] = "mdk3"
        else:
            df.loc[i, "class"] = "normal"

        if i % 10000 == 0:
            print("Packet n°", i, "done")

    # Close the capture object
    cap.close()

if __name__ == '__main__':
    t = threading.Thread(target=capture_packets)
    t.start()
    t.join()
    df.to_csv("Données\mdk3_1h20.csv")
    # df.to_csv("Données\\bruteforce_20min.csv")