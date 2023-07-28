import numpy as np
import time
import sounddevice as sd
import threading

class Metronome:

	def __init__(self, bpm):

		self.bpm = bpm
		self.sample_rate = 44100 

		frequency = 660  
		duration = 0.1 

		t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)

		self.count_waveform = np.sin(2 * np.pi * frequency*2 * t)
		self.waveform = np.sin(2 * np.pi * frequency * t)

		self.play_thread = None
		self.stop_event = threading.Event()

		
	def start_metronome(self):

		time_to_tick = int((60/self.bpm)*100)
		start_time = time.time()

		check_point_time = 0
		tick_count = 1

		print(f"start metronome {self.bpm}")

		## first tick ##############

		sd.play(self.count_waveform, self.sample_rate)
		tick_count += 1

		while not self.stop_event.is_set() :

			now_time = int((time.time() - start_time)*100) 

			if now_time != check_point_time :

				if tick_count <= 4 :

					if (now_time%time_to_tick) == 0 :

						sd.play(self.count_waveform, self.sample_rate)
						tick_count += 1

				else:

					if (now_time%time_to_tick) == 0 :

						sd.play(self.waveform, self.sample_rate)
						tick_count += 1

			check_point_time = now_time

	def start(self):

		self.play_thread = threading.Thread(target=self.start_metronome)
		self.play_thread.start()

	def stop(self):

		self.stop_event.set()  # Set the stop_event to signal the thread to stop
		self.play_thread.join()
		self.play_thread = None


### Raw Function ####

def metronome(bpm=120):
	
	frequency = 660  
	duration = 0.1 
	sample_rate = 44100 

	t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

	count_waveform = np.sin(2 * np.pi * frequency*2 * t)
	waveform = np.sin(2 * np.pi * frequency * t)

	time_to_tick = int((60/bpm)*100)
	start_time = time.time()

	check_point_time = 0
	tick_count = 1

	print(f"start metronome {bpm}")

	while True :

		now_time = int((time.time() - start_time)*100) 

		if now_time != check_point_time :

			if tick_count <= 4 :

				if now_time == 0 :

					sd.play(count_waveform, sample_rate)
					tick_count += 1

				elif (now_time%time_to_tick) == 0 :

					sd.play(count_waveform, sample_rate)
					tick_count += 1

			else:

				if (now_time%time_to_tick) == 0 :

					sd.play(waveform, sample_rate)
					tick_count += 1

		check_point_time = now_time



if __name__ == '__main__':
	# metronome()
	print("555")
	metronome = Metronome(bpm=120)

	now = time.time()

	print(now - time.time())

	metronome.start()

	time.sleep(5)

	metronome.stop()