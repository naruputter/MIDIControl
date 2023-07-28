import mido
import rtmidi
import matplotlib.pyplot as plt
import time
from tools import Metronome

''' 

##############################################################
#### Information #############################################
##############################################################

# MIDI Pack Format

	1. Normal Format
		- MIDI Data : [status, value, velocity, time]
		- MIDI Pack : [[status, value, velocity, time], [...]]

	2. Mido Format 
		- MIDI Data : Message('note_on', channel=0, note=64, velocity=42, time=396)
		- MIDI Pack : MidiFile(type=1, ticks_per_beat=480, tracks=[
								MidiTrack([
									Message('note_on', channel=0, note=64, velocity=42, time=396),
									Message('note_on', channel=0, note=62, velocity=47, time=9)
								])

# Function Include 

	1. read MIDI File
		- read_midi_file(filePath)
		- <class:MIDI>(filePath)

	2. write MIDI File
		- <class:MIDI> add_midi_data(midiData)

	3. receive Realtime MIDI 
		- <class:MIDI> realtime_running()

	4. save MIDI File From MIDI Data
		- <class:MIDI> save_midi_file(filePath)
		- save_midi_file(midiPack, filePath)


'''


class MIDI :

	def __init__(self, tick=480, bpm=120, filePath=None):

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

		return available_ports


	def realtime_running(self, port=0, metronome=False):

		first_received = False

		midi_in = rtmidi.MidiIn()
		available_ports = midi_in.get_ports()

		if available_ports:

			self.midi_pack = receive_midi_realtime(port=port, bpm=self.bpm, metronome=metronome)

			return self.midi_pack

		else:
			print("No MIDI input ports found.")


	def add_midi_data(self, midiData): # MIDI Data : [status, value, velocity, time]

		self.midi_pack.append(midiData)

		return midiData

	def edit_midi_data(self, position, newMidiData):

		self.midi_pack[position] = newMidiData

		return newMidiData

	def save_midi_file(self, filePath):

		mido_pack = convert_midi_pack_to_mido_pack(self.midi_pack, bpm=self.bpm)

		mido_pack.save(filePath)

		return filePath



### Realtime #####################

def receive_midi_realtime(port=0, bpm=None, metronome=False):

	### !!! all receive note is note_on !!! ####

	midi_pack = []

	first_received = False
	midi_in = rtmidi.MidiIn()

	midi_in.open_port(port)

	print("MIDI Receive Running !!!")

	if metronome is True :

		metronome = Metronome(bpm=bpm)
		metronome.start()

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

				metronome.stop()

				break

			print(midi_value)

		time.sleep(0.01)

	print(midi_pack)

	return midi_pack


### Manage MIDI Micro Function #########


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


def convert_time_to_mido_format(time, bpm, tick=480):

	constant = ( tick *  bpm  ) / ( 60 )
	mido_time = round(time*constant)

	return mido_time


def convert_midi_value_to_mido_message(midiValue, bpm=120, tick=480):

	time = midiValue[-1]
	midiValue.pop(-1)

	try:
		mido_message = mido.Message.from_bytes(midiValue)
		mido_time = convert_time_to_mido_format(time, bpm, tick)
		mido_message.time = mido_time 
	except:
		mido_message = None

	return mido_message


def convert_mido_message_to_midi_value(midoMessage):

	midi_value = midoMessage.bytes()
	midi_value.append(midoMessage.time)

	return midi_value


def convert_midi_pack_to_mido_pack(midiPack, bpm=120, tick=480):

	mido_pack = mido.MidiFile()
	mido_track = mido.MidiTrack()

	for midi_value in midiPack :

		mido_message = convert_midi_value_to_mido_message(midi_value, bpm, tick)

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

	# print(read_midi_file("testset120.midi"))

	midi = MIDI(bpm=100)

	midi_pack = midi.realtime_running(metronome=True)
	midi.save_midi_file("testset100.midi")

	# print(convert_midi_pack_to_mido_pack(midi_pack))
	# save_midi_file(midi_pack, 'cannon.mid')

	# receive_midi_realtime()

	# midi.add_midi_data([144,20,50,1])
	# midi.add_midi_data([144,40,50,1])
	# midi.add_midi_data([144,30,50,1])
	# midi.add_midi_data([144,80,50,1])



	# print(midi.midi_pack)

	# midi.edit_midi_data(0,[0,0,0,0])

	# print(midi.midi_pack)




