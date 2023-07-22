from MIDIManagement import *
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler



def running_save_midi(key):

    now_time = int(time.time())

    save_midi_folder = 'midi_collection/MIDIDataset' + f'/{key}'
    file_path = save_midi_folder + f'/{now_time}.mid'

    write_midi = MIDIReceive(portName='Digital Piano', BPM=120)
    write_midi.receive_running()

    # print(write_midi.midi_tracks)
    print(1)

    write_midi.save_midi_file('test.midi')


    # read_midi = MIDIRead(filePath=file_path)
    # summary_note_json = read_midi.summary_note_name()

    # df = pd.read_csv(folder_path + '/MIDIData.csv')

    # values = list(summary_note_json.values())
    # total = sum(values)

    # ratios = [value / total for value in values]

    # keys = list(summary_note_json.keys())

    # data = dict(zip(keys, ratios))

    # data['key'] = key

    # df = df.append(data, ignore_index=True)

    # df.to_csv(folder_path + '/MIDIData.csv', index=False)


def classify_key():

    df = pd.read_csv('midi_collection/MIDIDataset/MIDIData.csv')

    df = df[0:55]
    print(df)

    knn = KNeighborsClassifier(n_neighbors=5, p=2, metric='minkowski')

    X = df.drop('key', axis=1)  # Drop the target column
    y = df['key']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01)

    print(X_train)


    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    knn.fit(X_train_scaled, y_train)

    y_pred = knn.predict(X_test_scaled)

    print(y_test.values)
    print(y_pred)

    import joblib

    # Save the trained model to a file
    joblib.dump(knn, 'knn_model.pkl')




if __name__ == '__main__':

    # classify_key()

    import joblib

    df = pd.read_csv('midi_collection/MIDIDataset/MIDIData.csv')
    df = df

    train = df.drop('key', axis=1)

    print(df)

    # Load the saved model from a file
    knn_model = joblib.load('knn_model.pkl')

    predict = knn_model.predict(train)

    print(predict)
