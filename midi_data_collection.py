from MIDIGenerate import *
from MIDIAnalytic import *
import pandas as pd

folder_path = '/Users/putter/Putteror/Code/MIDIDataset'

def running_save_midi(key):

    time.sleep(1)

    now_time = int(time.time())

    file_path = folder_path + f'/{key}' + f'/{now_time}.mid'

    write_midi = MIDIInput(port_name='Digital Piano', bpm=120)
    write_midi.receive_running(filePath=file_path)

    read_midi = MIDIRead(filePath=file_path)
    summary_note_json = read_midi.summary_note_name()

    df = pd.read_csv(folder_path + '/MIDIData.csv')

    values = list(summary_note_json.values())
    total = sum(values)

    ratios = [value / total for value in values]

    keys = list(summary_note_json.keys())

    data = dict(zip(keys, ratios))

    data['key'] = key

    df = df.append(data, ignore_index=True)

    df.to_csv(folder_path + '/MIDIData.csv', index=False)



if __name__ == '__main__':

    while True:
    
        running_save_midi(key='B')