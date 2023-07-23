import mido
import rtmidi
import matplotlib.pyplot as plt
import time


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

	def get_input_port(self):

		available_ports = midi_in.get_ports()


	def realtime_running(self):

		first_received = False

		midi_in = rtmidi.MidiIn()
		available_ports = midi_in.get_ports()

		if available_ports:

			midi_pack = receive_midi_realtime(port=0)

			return midi_pack

		else:
			print("No MIDI input ports found.")


### Realtime #####################

def receive_midi_realtime(port=0):

	### !!! all receive note is note_on !!! ####

	midi_pack = []

	first_received = False
	midi_in = rtmidi.MidiIn()

	midi_in.open_port(port)
	start_timestamp = time.time() 

	while True:
			
		rtmidi_message = midi_in.get_message()

		if rtmidi_message:

			receive_timstamp = time.time() 
			midi_value = rtmidi_message[0]

			if first_received :

				midi_value.append(rtmidi_message[1])

			else :

				first_note_time = receive_timstamp - start_timestamp
				midi_value.append( first_note_time )

				first_received = True

			midi_pack.append(midi_value)

			if midi_value[1] == 21 :

				break

		time.sleep(0.01)

	print(midi_pack)

	return midi_pack


### Manage MIDI Function #########


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
	
	midi = MIDI()

	midi_pack = midi.realtime_running()

	print(convert_midi_pack_to_mido_pack(midi_pack))
	# save_midi_file(midi_pack, 'cannon.mid')

	# receive_midi_realtime()

