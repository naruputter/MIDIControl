import mido

def convert_midi_value_to_mido_message(midi_value):

	time = midi_value[-1]
	midi_value.pop(-1)

	try:
		mido_message = mido.Message.from_bytes(midi_value)
		mido_message.time = time
	except:
		mido_message = None

	return mido_message

def convert_mido_message_to_midi_value(mido_message):

	midi_value = mido_message.bytes()
	midi_value.append(mido_message.time)

	return midi_value


def read_midi_file(filePath):

	midi_pack = []

	mido_message_pack = mido.MidiFile(filePath, clip=True)

	for mido_message in mido_message_pack :

		midi_value = convert_mido_message_to_midi_value(mido_message)

		midi_pack.append(midi_value)

	return midi_pack


def convert_midi_pack_to_mido_pack(midi_pack):

	mido_pack = mido.MidiFile()

	for midi_value in midi_pack :

		mido_message = convert_midi_value_to_mido_message(midi_value)

		if mido_message :

			mido_pack.tracks.append(mido_message)

	return mido_pack





	
if __name__ == '__main__':
	
	midi = read_midi_file('file/midi.mid')
	print(convert_midi_pack_to_mido_pack(midi))
