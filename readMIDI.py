import mido
import matplotlib.pyplot as plt


class MIDI :

	def __init__(self, tick=480, bpm=30, filePath=None):

		if filePath :

			midiPack = read_midi_file(filePath)

		else :

			midiPack = []

		self.file_path = filePath
		self.midi_pack = midiPack
		self.tick = tick
		self.bpm = bpm




### Manage Function #########


def read_midi_file(filePath):

	mido_message_pack = mido.MidiFile(filePath, clip=True)

	midi_pack = convert_mido_pack_to_midi_pack(mido_message_pack)

	return midi_pack


def save_midi_file(midiPack, filePath):

	mido_pack = None

	if type(midiPack) == list :

		mido_pack = convert_midi_pack_to_mido_pack(midiPack)

	elif type(midiPack) == mido.midifiles.midifiles.MidiFile :

		mido_pack = midiPack


	if mido_pack :

		mido_pack.save(filePath)

		return f"sve file to {filePath} succesfull"

	else :

		return "value is not match to save midi"



### Convert Function ########


def convert_time_to_mido_format(time ,tick=480, bpm=30):

	constant = ( tick * 60 ) / bpm 
	mido_time = round(time*constant)

	return mido_time


def convert_midi_value_to_mido_message(midiValue, tick=480, bpm=30):

	time = midiValue[-1]
	midiValue.pop(-1)

	try:
		mido_message = mido.Message.from_bytes(midiValue)
		mido_time = convert_time_to_mido_format(time, tick, bpm)
		mido_message.time = mido_time 
	except:
		mido_message = None

	return mido_message


def convert_mido_message_to_midi_value(midoMessage):

	midi_value = midoMessage.bytes()
	midi_value.append(midoMessage.time)

	return midi_value


def convert_midi_pack_to_mido_pack(midiPack, tick=480, bpm=30):

	mido_pack = mido.MidiFile()
	mido_track = mido.MidiTrack()

	for midi_value in midiPack :

		mido_message = convert_midi_value_to_mido_message(midi_value, tick, bpm)

		if mido_message :

			mido_track.append(mido_message)

	mido_pack.tracks.append(mido_track)

	return mido_pack


def convert_mido_pack_to_midi_pack(midoPack):

	midi_pack = []

	for mido_message in midoPack :

		midi_value = convert_mido_message_to_midi_value(mido_message)

		midi_pack.append(midi_value)

	return midi_pack




	
if __name__ == '__main__':
	
	midi = MIDI(filePath='test.mid')

	print(midi.midi_pack)

	print(convert_midi_pack_to_mido_pack(midi.midi_pack))

