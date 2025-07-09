import glob
import numpy as np
from music21 import converter, instrument, note, chord, stream
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dropout, Dense
from tensorflow.keras.utils import to_categorical

def load_midi(midi_folder='midi_songs/*.mid'):
    notes = []
    for file in glob.glob(midi_folder):
        print(f'Parsing {file}')
        midi = converter.parse(file)
        parts = instrument.partitionByInstrument(midi)
        notes_to_parse = parts.parts[0].recurse() if parts else midi.flat.notes
        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))
    return notes

def prepare_sequences(notes, seq_length=50):
    pitchnames = sorted(set(notes))
    note2int = {n: i for i, n in enumerate(pitchnames)}
    int2note = {i: n for n, i in note2int.items()}

    network_input = []
    network_output = []
    for i in range(len(notes) - seq_length):
        seq_in = notes[i : i + seq_length]
        seq_out = notes[i + seq_length]
        network_input.append([note2int[n] for n in seq_in])
        network_output.append(note2int[seq_out])

    n_patterns = len(network_input)
    print(f'Total patterns: {n_patterns}')

    X = np.array(network_input)
    y = to_categorical(network_output, num_classes=len(pitchnames))

    return X, y, note2int, int2note, len(pitchnames)

def build_model(vocab_size, seq_length=50):
    model = Sequential()
    model.add(Embedding(input_dim=vocab_size, output_dim=100, input_length=seq_length))
    model.add(LSTM(256, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(256))
    model.add(Dense(vocab_size, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    model.summary()
    return model

def generate_notes(model, network_input, int2note, vocab_size, length=200):
    start = np.random.randint(0, len(network_input)-1)
    pattern = network_input[start].tolist()
    output_notes = []

    for _ in range(length):
        prediction_input = np.array(pattern)[None, :]
        prediction = model.predict(prediction_input, verbose=0)[0]
        index = np.argmax(prediction)
        result = int2note[index]
        output_notes.append(result)

        pattern.append(index)
        pattern = pattern[1:]

    return output_notes

def create_midi(prediction_output, filename='generated.mid'):
    offset = 0
    output_notes = []
    for pattern in prediction_output:
        if ('.' in pattern) or pattern.isdigit():
            notes_in_chord = pattern.split('.')
            chord_notes = [note.Note(int(n)) for n in notes_in_chord]
            new_chord = chord.Chord(chord_notes)
            new_chord.offset = offset
            output_notes.append(new_chord)
        else:
            new_note = note.Note(pattern)
            new_note.offset = offset
            output_notes.append(new_note)
        offset += 0.5

    midi_stream = stream.Stream(output_notes)
    midi_stream.write('midi', fp=filename)
    print(f'Wrote {filename}')

if __name__ == '__main__':
    notes = load_midi()
    X, y, note2int, int2note, vocab_size = prepare_sequences(notes)

    model = build_model(vocab_size)
    model.fit(X, y, epochs=50, batch_size=64)

    generated = generate_notes(model, X, int2note, vocab_size)
    create_midi(generated)