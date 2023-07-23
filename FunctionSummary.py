from MIDIManagement import *

def midi_info():

	midi_info = MIDIInfo(filePath='file/midi.mid')
	print(midi_info.midi_tracks)
	# print(midi_info.midi_info)
	# print(midi_info.message_list(byte=True))
	# print(midi_info.meta_message_list())
	# print(midi_info.note_message_list())
	# print(midi_info.summary_note_name())

	return midi_info

def midi_write():

	midi_write = MIDIWrite()
	# print(midi_write.add_message(status='note_on', note=57, velocity=57, time=300))
	# print(midi_write.midi_tracks)
	# print(midi_write.save_midi_file(path='file/test.midi'))

	tracks = midi_write.midi_tracks

	midi_write = MIDIWrite(Tracks=tracks)

	# print(midi_write.add_message( control=64, value=64, time=400))
	# print(midi_write.midi_tracks)
	# print(midi_write.save_midi_file(path='file/test.midi'))


def midi_receive():

	midi_receive = MIDIReceive()

	# print(midi_receive.bpm)
	# print(midi_receive.port_name)
	# print(midi_receive.get_input_port())
	# print(midi_receive.set_input_port('putter Bus 1'))
	# print(midi_receive.port_name)
	print(midi_receive.receive_running())



if __name__ == '__main__':
	
	# midi_info()
	# midi_write()
	midi_receive()
