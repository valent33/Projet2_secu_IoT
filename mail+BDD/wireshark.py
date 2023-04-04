import pyshark
import pandas as pd

# Define the callback function to extract packet features and append to the list
def packet_callback(packet):
    packet_dict = {feature: packet[feature].showname.split(': ', 1)[1] for feature in features}
    packet_dict['length'] = packet.length
    global packet_features
    packet_features.append(packet_dict)

    # global packet_count
    # packet_count += 1
    # print(packet_count)

# packet_count = 0
# packet_limit = 100

# Create an empty list to store the packet features
packet_features = []

# features = ['radiotap.length', 'wlan.fc_type_subtype', 'wlan.duration', 'wlan_radio.data_rate']
features = []

# capture on interface Wi-Fi
capture = pyshark.LiveCapture(interface='Wi-Fi')

# Apply the packet callback function to each packet
try :
    capture.apply_on_packets(packet_callback, timeout=10)
except :
    pass

# Convert the list of dictionaries to a Pandas DataFrame
df = pd.DataFrame(packet_features)

# Save to csv
df.to_csv("capture.csv", mode='w', header=True)


