import tensorflow as tf
import pandas as pd
import pickle
from keras.utils import to_categorical
from numpy import argmax
import plotly.express as px
import sys

# load model and scaler
model = tf.keras.models.load_model('model_LSTM.h5')
subtype_encoder = pickle.load(open('subtype_encoder.pickle', 'rb'))
scaler = pickle.load(open('scaler.pickle', 'rb'))


def prediction(file_path, test=False):
    """makes prediction on a csv file

    Args:
        file_path (str): file path to the csv file
        test (bool, optional): set to True if the csv contains a class column. Defaults to False.

    Returns:
        (predictions, target): returns (predictions and target if test is True)
    """
    df_test = pd.read_csv(file_path, index_col=0)
    if test:
        X_test = df_test.drop('class', axis=1)
        y_test = df_test['class']
        y_test = y_test.replace(
            {'normal': 0, 'bruteforce': 1, 'slowloris': 2, 'mdk3': 3})
        y_test = to_categorical(y_test)
        y_test = y_test[:y_test.shape[0]-y_test.shape[0] % 100]
        y_test = y_test.reshape((-1, y_test.shape[1]))
    else:
        X_test = df_test
        y_test = None

    X_test['subtype'] = subtype_encoder.transform(X_test['subtype'])

    try:
        X_test = scaler.transform(X_test)
    except ValueError:
        print("file has a class column so please use the -test parameter")
        exit()

    X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

    X_test = X_test[:X_test.shape[0]-X_test.shape[0] % 100]

    X_test = X_test.reshape((-1, 100, X_test.shape[2]))

    predictions = model.predict(X_test)

    predictions = predictions.reshape((-1, 4))

    return predictions, y_test


def pred_final(file_path, test=False):
    """handle prediction data so that it can be plotted

    Args:
        file_path (str): file path to the csv file
        test (bool, optional): set to True if the csv contains a class column. Defaults to False.

    Returns:
        (predictions, target): returns predictions (and target if test is True)
    """
    pred, y_test = prediction(file_path, test)

    pred_normal = pred[:, 0]
    pred_brute = pred[:, 1]
    pred_slowloris = pred[:, 2]
    pred_mdk3 = pred[:, 3]

    # # compute rolling average
    pred_normal = pd.Series(pred_normal).rolling(100).mean()
    pred_brute = pd.Series(pred_brute).rolling(100).mean()
    pred_slowloris = pd.Series(pred_slowloris).rolling(100).mean()
    pred_mdk3 = pd.Series(pred_mdk3).rolling(100).mean()

    # make final prediction by taking the most frequent class at each time step
    # if proba of not normal is higher than 0.8, then make it the prediction
    # else make the prediction normal
    pred = []
    for i in range(pred_brute.shape[0]):
        if max(pred_brute[i], pred_slowloris[i], pred_mdk3[i]) > 0.8:
            # print('max', max(pred_brute[i], pred_slowloris[i], pred_mdk3[i]))
            pred.append(
                argmax([pred_brute[i], pred_slowloris[i], pred_mdk3[i]]) + 1)
        else:
            pred.append(0)

    pred = pd.Series(pred)
    pred = pred.replace(
        {0: 'normal', 1: 'bruteforce', 2: 'slowloris', 3: 'mdk3'})
    if test:
        y_test = argmax(y_test, axis=1)
        y_test = pd.Series(y_test)
        y_test = y_test.replace(
            {0: 'normal', 1: 'bruteforce', 2: 'slowloris', 3: 'mdk3'})

    return pred, y_test


def precision(pred, y_test, classe):
    """compute precision metric for a given class against all other classes : TP / (TP + FP)

    Args:
        pred (array): predictions array (shape = (n, 1))
        y_test (array): targets array (shape = (n, 1))
        classe (str): classe to compute precision against all other classes, one of ['normal', 'bruteforce', 'slowloris', 'mdk3']

    Returns:
        float: precision metric
    """
    TP = 0
    FP = 0
    for i in range(pred.shape[0]):
        if pred[i] == classe and y_test[i] == classe:
            TP += 1
        elif pred[i] == classe and y_test[i] != classe:
            FP += 1
    try:
        precision = TP / (TP + FP)
    except ZeroDivisionError:
        precision = 0
    return precision


def recall(pred, y_test, classe):
    """compute recall metric for a given class against all other classes : TP / (TP + FN)

    Args:
        pred (array): predictions array (shape = (n, 1))
        y_test (array): targets array (shape = (n, 1))
        classe (str): classe to compute recall against all other classes, one of ['normal', 'bruteforce', 'slowloris', 'mdk3']

    Returns:
        float: recall metric
    """
    TP = 0
    FN = 0
    for i in range(pred.shape[0]):
        if pred[i] == classe and y_test[i] == classe:
            TP += 1
        elif pred[i] != classe and y_test[i] == classe:
            FN += 1
    try:
        recall = TP / (TP + FN)
    except ZeroDivisionError:
        recall = 0
    return recall


def f1_score(pred, y_test, classe):
    """compute f1 score metric for a given class against all other classes : 2 * (precision * recall) / (precision + recall)

    Args:
        pred (array): predictions array (shape = (n, 1))
        y_test (array): targets array (shape = (n, 1))
        classe (str): classe to compute f1 score against all other classes, one of ['normal', 'bruteforce', 'slowloris', 'mdk3']

    Returns:
        float: f1 score metric
    """
    prec = precision(pred, y_test, classe)
    reca = recall(pred, y_test, classe)
    try:
        f1_score = 2 * (prec * reca) / (prec + reca)
    except ZeroDivisionError:
        f1_score = 0
    return f1_score


def plot_prediction(file_path, test=False):
    """plots predictions

    Args:
        file_path (str): file path to the csv file
        test (bool, optional): set to True to plot target on same plot. Defaults to False.
    """
    pred, y_test = pred_final(file_path, test)
    if test:
        for classe in ['bruteforce', 'slowloris', 'mdk3']:
            prec = precision(pred, y_test, classe)
            reca = recall(pred, y_test, classe)
            f1 = f1_score(pred, y_test, classe)
            print(
                f'Prediction de {classe}: precision = {prec:.2f}, recall = {reca:.2f}, f1-score = {f1:.2f}')
    fig = px.line(pred, title="Prediction", width=1000, height=300)
    fig.data[0].name = 'Prediction'
    if test:
        fig.add_scatter(y=y_test, name='True class', line=dict(width=5))
    else:
        # make a decision about potential type of attack
        pred = pd.Series(pred)
        pred = pred.replace({0: 'normal', 1: 'bruteforce', 2: 'slowloris', 3: 'mdk3'})

        # count ratio of each class
        ratio = pred.value_counts(normalize=True)
        for i in ['normal', 'bruteforce', 'slowloris', 'mdk3']:
            if i not in ratio:
                ratio[i] = 0
        print(ratio)
        for i in ['normal', 'bruteforce', 'slowloris', 'mdk3']:
            if ratio['mdk3'] > 0.1:
                fig.add_annotation(x=0, y=0.7, text="mdk3 attack detected", showarrow=False)
            elif ratio['slowloris'] > 0.1:
                fig.add_annotation(x=0, y=0.7, text="slowloris attack detected", showarrow=False)
            elif ratio['bruteforce'] > 0.1:
                fig.add_annotation(x=0, y=0.7, text="bruteforce attack detected", showarrow=False)
            else:
                fig.add_annotation(x=0, y=0.7, text="no attack detected", showarrow=False)

    fig.update_yaxes(title_text='Class')
    fig.update_xaxes(title_text='Packets')
    fig.show()


if __name__ == '__main__':
    try:
        file_path = sys.argv[1]
        if not isinstance(file_path, str):
            print('Usage: python analyse_LSTM.py <file_path> "test" (optional)')
            exit()
    except IndexError:
        print('Usage: python analyse_LSTM.py <file_path> "test" (optional)')
        exit()

    try:
        testmode = sys.argv[2]
        if testmode == '-test':
            testmode = True
        else:
            testmode = False
    except IndexError:
        testmode = False

    try:
        plot_prediction(file_path, testmode)
    except FileNotFoundError:
        print('File not found')
        exit()
