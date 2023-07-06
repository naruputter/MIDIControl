from MIDIManagement import *
import sounddevice as sd

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