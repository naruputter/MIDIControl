# from MIDIManagement import *
import sounddevice as sd
import mido
import time
import rtmidi

def metronome(bpm):
	
	frequency = 660  
	duration = 0.1 
	sample_rate = 44100 

	t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

	waveform = np.sin(2 * np.pi * frequency * t)

	print(waveform)

	# plt.plot(waveform[0:68])
	# plt.xlabel('Frequency (Hz)')
	# plt.ylabel('Magnitude')
	# plt.show()


	while True :

		start_time = time.time()

		sd.play(waveform, sample_rate)

		end_time = time.time()
		execution_time = end_time - start_time

		time.sleep((60/bpm)-execution_time)


def handle_midi_message(message):
	print(f'Received MIDI message: {message}')


if __name__ == '__main__':

	midiin = rtmidi.MidiIn()
	available_ports = midiin.get_ports()
	# Identify the MIDI input port for your controller and open it
	controller_port = 1  # Replace with the index of your MIDI controller's port
	midiin.open_port(controller_port)

	print(available_ports)
	
	controller_name = "Digital Piano"

	print("MIDI controller opened:", available_ports[1])

	# Start an infinite loop to continuously listen for MIDI messages
	while True:

		message = midiin.get_message()

		if message:

			timestamp = message[1]
			data = message[0]
			print("Received:", data, "Timestamp:", timestamp)
		time.sleep(0.001)
