import pyshark
import pandas as pd
import pickle
import sklearn
# import tensorflow as tf
from numpy import argmax
import time
# from mailBDD.mailing import send_mail

# load subtype_encoder, scaler and model
with open('subtype_encoder.pickle', 'rb') as f:
    subtype_encoder = pickle.load(f)
with open('scaler.pickle', 'rb') as f:
    scaler = pickle.load(f)
with open('model.pickle', 'rb') as f:
    model = pickle.load(f)

# Define the callback function to extract packet features and append to the list
def packet_callback(packet):
    packet_dict = {}
    packet_dict['length'] = packet.length
    try:
        packet_dict['header_length'] = packet.radiotap.length
        packet_dict['subtype'] = packet.wlan.fc_type_subtype
        packet_dict['duration'] = packet.wlan.duration
        packet_dict['datarate'] = packet.wlan_radio.data_rate
    except:
        for layer in packet.layers:
            print("###############", layer.layer_name, "###############")
            for field in layer.field_names:
                print(field, getattr(layer, field))
                break

    global packet_features
    packet_features.append(packet_dict)


# capture on interface Wi-Fi
capture = pyshark.LiveCapture(interface='Wi-Fi')

now = time.time()
temp = True
while temp:
    # Create an empty list to store the packet features
    packet_features = []

    # features = ['radiotap.length', 'wlan.fc_type_subtype', 'wlan.duration', 'wlan_radio.data_rate']
    features = []
    # Apply the packet callback function to each packet
    try :
        capture.apply_on_packets(packet_callback, timeout=5)
    except :
        pass

    print(f"capture over, time elpased {time.time() - now}, processing...")
    now = time.time()

    # Convert the list of dictionaries to a Pandas DataFrame
    df = pd.DataFrame(packet_features)

    # Save to csv
    df.to_csv("temp/capture_temp.csv", mode='w', header=True) ## to be removed
    df = pd.read_csv("temp/capture.csv", index_col=0) ## to be removed

    ### PREDICTION ###
    df = df[:df.shape[0]-df.shape[0]%100]

    X = df.drop('class', axis=1) ## to be removed

    X['subtype'] = subtype_encoder.transform(X['subtype'])
    X = scaler.transform(X)

    # X = X.reshape((-1, 100, X.shape[1]))

    predictions = model.predict(X)
    print(predictions)

    # predictions = predictions.reshape((-1, 4))

    # pred_normal = predictions[:, 0]
    # pred_brute = predictions[:, 1]
    # pred_slowloris = predictions[:, 2]
    # pred_mdk3 = predictions[:, 3]

    # # # compute rolling average
    # pred_normal = pd.Series(pred_normal).rolling(100).mean()
    # pred_brute = pd.Series(pred_brute).rolling(100).mean()
    # pred_slowloris = pd.Series(pred_slowloris).rolling(100).mean()
    # pred_mdk3 = pd.Series(pred_mdk3).rolling(100).mean()

    # # make final prediction by taking the most frequent class at each time step
    # # if proba of not normal is higher than 0.8, then make it the prediction
    # # else make the prediction normal
    # pred = []
    # for i in range(pred_brute.shape[0]):
    #     if max(pred_brute[i], pred_slowloris[i], pred_mdk3[i]) > 0.8:
    #         # print('max', max(pred_brute[i], pred_slowloris[i], pred_mdk3[i]))
    #         pred.append(argmax([pred_brute[i], pred_slowloris[i], pred_mdk3[i]]) + 1)
    #     else:
    #         pred.append(0)

    pred = pd.Series(predictions)
    pred = pred.replace({0: 'normal', 1: 'bruteforce', 2: 'slowloris', 3: 'mdk3'})

    # count ratio of each class
    ratio = pred.value_counts(normalize=True)

    # print the ratio
    print(f"prediction time: {time.time() - now}")
    print(ratio)
    # fill the ratio dict with 0 if the class is not present
    for i in ['normal', 'bruteforce', 'slowloris', 'mdk3']:
        if i not in ratio:
            ratio[i] = 0

    if ratio['mdk3'] > 0.1:
        print("mdk3 attack detected")
        # send_mail("Jean", "Neymar", "jean.neymar@gmail.com", "mdk3")
    elif ratio['slowloris'] > 0.1:
        print("slowloris attack detected")
        # send_mail("Jean", "Neymar", "jean.neymar@gmail.com", "slowloris")
    elif ratio['bruteforce'] > 0.1:
        print("bruteforce attack detected")
        # send_mail("Jean", "Neymar", "jean.neymar@gmail.com", "bruteforce")
    else:
        print("no attack detected")
