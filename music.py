import note_seq
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.models.shared import sequence_generator_bundle
from magenta.music.sequences_lib import concatenate_sequences
from magenta.music import sequence_proto_to_midi_file
from magenta.music import sequence_generator
from magenta.music import midi_io
import tensorflow.compat.v1 as tf
import os

tf.disable_v2_behavior()

# Load the pre-trained bundle
bundle = sequence_generator_bundle.read_bundle_file('basic_rnn.mag')
generator_map = melody_rnn_sequence_generator.get_generator_map()
melody_rnn = generator_map['basic_rnn'](checkpoint=None, bundle=bundle)
melody_rnn.initialize()
from magenta.music import music_pb2

seed = music_pb2.NoteSequence()
seed.notes.add(pitch=60, start_time=0.0, end_time=0.5, velocity=80)
seed.total_time = 1.0
seed.tempos.add(qpm=120)
from magenta.protobuf import generator_pb2

# Set generation options
generator_options = generator_pb2.GeneratorOptions()
generator_options.generate_sections.add(start_time=seed.total_time, end_time=30)

# Generate the sequence
generated_sequence = melody_rnn.generate(seed, generator_options)

# Save to MIDI
output_path = 'generated_music.mid'
sequence_proto_to_midi_file(generated_sequence, output_path)
print(f"🎶 Music generated and saved to {output_path}")
import pygame

pygame.init()
pygame.mixer.music.load("generated_music.mid")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    continue

