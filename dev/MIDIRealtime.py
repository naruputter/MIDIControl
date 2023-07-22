import rtmidi
import time
import os
import json
import numpy as np


class MIDIReceive: # Receive Midi Message From MIDIController Real-Time For Create File Or Analytic

	def __init__(self, portName=None, BPM=120) :

		self.bpm = BPM
		self.port_name = portName

	def receive_running(self): # Receive Midi Real-Time

		track_list = []

		midiin = rtmidi.MidiIn()
		midiin.open_port(1)

		firtTime = True

		start_timestamp = time.time()

		while True:

			message = midiin.get_message()

			if message:

				if firtTime is True :

					firtTime = False
					timestamp = time.time() - start_timestamp 

				else:

					timestamp = message[1]

				data = message[0]
				data.append(timestamp)
				print(data)
				track_list.append(data)

				time.sleep(0.001)

				if message[0][1] == 21:

					break

		return track_list


if __name__ == '__main__':
	

	midi = MIDIReceive()

	print(midi.receive_running())


