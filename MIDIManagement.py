import rtmidi
import mido
import time
import os
import json
import numpy as np



NOTE_PER_12 = { 0:'C', 1:'C#', 2:'D', 3:'Eb', 4:'E', 5:'F',	6:'F#',	7:'G',	8:'Ab',	9:'A', 10:'Bb', 11:'B' }
NOTE_NAME_LIST = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']



def list_to_json_count(data_list): # Count Duplicate Value In List By Convert To JSON Format

	json_count = {}

	for data in data_list :
		json_count[data] = 0

	return json_count


class MIDIInfo: # Read And Analyte MIDI Message 

	def __init__(self, filePath):

		self.midi_info = mido.MidiFile(filePath)
		self.midi_tracks = self.midi_info.tracks[0]


	def message_list(self, byte=False): # Get MIDI Message for List 

		midi_message_list = []

		for midi_message in self.midi_info :

			if byte :

				midi_message_list.append(midi_message.bytes())

			elif not byte :

				midi_message_list.append(midi_message)

		return midi_message_list


	def meta_message_list(self, byte=False): # Get Header Message for List 

		midi_message_list = []

		for midi_message in self.midi_info :

			if isinstance(midi_message, mido.MetaMessage):

				if byte :

					midi_message_list.append(midi_message.bytes())

				elif not byte :

					midi_message_list.append(midi_message)

		return midi_message_list


	def note_message_list(self, status=None, byte=False): # Get Only Note Message List ( note_on | note_off | None = Both )

		midi_message_list = []

		for midi_message in self.midi_info :

			if status is not None :

				if midi_message.type == status:

					if byte :

						midi_message_list.append(midi_message.bytes())

					elif not byte :

						midi_message_list.append(midi_message)

			elif status is None :

				if midi_message.type == 'note_on' or midi_message.type == 'note_off':

					if byte :

						midi_message_list.append(midi_message.bytes())

					elif not byte :

						midi_message_list.append(midi_message)


		return midi_message_list


	################ Function #########################################


	def summary_note_name(self): # Summary 12 Note To JSON

		summary_note_name_json = list_to_json_count(NOTE_NAME_LIST)

		message_note_on_list = self.note_message_list(status='note_on')

		for message in message_note_on_list :

			note_name = NOTE_PER_12[message.note%12]

			if note_name in summary_note_name_json :

				summary_note_name_json[note_name] += 1

		return summary_note_name_json


class MIDIWrite : # Create MIDI Tracks Or Set And Use MidiSet To Save File


	def __init__(self, Tracks=None): # If Have [ Mido ] Tracks Can Add To Tracks

		self.midi_set = mido.MidiFile() 

		if Tracks :
			self.midi_tracks = Tracks

		elif Tracks is None :
			self.midi_tracks = mido.MidiTrack() 


	def tracks(self): # Get Only Tracks Information ( Mido Format )

		return self.midi_tracks


	def add_message(self, status=None, note=None, control=None, velocity=None, value=None, time=None, message=None): 

		# Add Message To Mido Tracks 1. Add By Parameter 2. Add Mido Message ( message )

		if message is None :

			if status and note and velocity and time :

				message = mido.Message(status, note=note, velocity=velocity, time=time)

			elif control and value and time :

				message = mido.Message('control_change', control=control, value=value, time=time)

			else:

				return None

			self.midi_tracks.append(message)

		elif message is not None :

			self.midi_tracks.append(message)

		self.midi_set.tracks.append(self.midi_tracks)

		return message


	def save_midi_file(self, path): # Save Midi Set To .mid Or midi. File

		self.midi_set.tracks.append(self.midi_tracks)
		self.midi_set.save(path)


class MIDIReceive: # Receive Midi Message From MIDIController Real-Time For Create File Or Analytic

	def __init__(self, portName=None, BPM=120) :

		self.bpm = BPM
		self.port_name = portName
		self.input_port = mido.open_input(portName)
		self.midi_set = mido.MidiFile()
		self.midi_tracks = mido.MidiTrack()

	def get_input_port(self): # Gat All Input Midi Port

		all_input_ports_name = mido.get_input_names()

		return all_input_ports_name

	def set_input_port(self, port_name): # Change Input Midi Port

		self.port_name = port_name
		self.input_port = mido.open_input(self.port_name)

		return f' {self.port_name} connect ! '

	def receive_running(self, save_path=None): # Receive Midi Real-Time

		start_running_time = time.time()

		try:
			for message in self.input_port:

				try :
					if message.note == 21 :
						break 
				except :
					pass

				byte_message = message.bytes()

				current_time = time.time() 
				elapsed_time = current_time - start_running_time 

				message.time = int(elapsed_time*(self.bpm*10)) 

				print("Message:", message)

				self.midi_tracks.append(message)

		except KeyboardInterrupt:
			input_port.close()

		return self.midi_tracks

	def save_midi_file(self, path): # Save Midi Set To .mid Or midi. File

		self.midi_set.tracks.append(self.midi_tracks)
		self.midi_set.save(path)


