import torch
import torchaudio
import numpy as np
from pathlib import Path
import soundfile as sf



from hubconf_offline import knn_vc  # Import the knn_vc function from hubconf_offline.py


# knnvc_model = knn_vc(pretrained=True, prematched=True, device='cpu')

# path to 16kHz, single-channel, source waveform
# src_wav_path = './src/src.wav'
# list of paths to all reference waveforms (each must be 16kHz, single-channel) from the target speaker
# ref_wav_paths = ['./ref/ref1.wav', ]

# query_seq = knnvc_model.get_features(src_wav_path)
# print(query_seq.shape)
# matching_set = knnvc_model.get_matching_set(ref_wav_paths)
# print(matching_set.shape)

# out_wav = knnvc_model.match(query_seq, matching_set, topk=4)
# print(out_wav.shape)

# torchaudio.save('./out/out.wav', out_wav[None], 16000)

class TTS(object):
    def __init__(self):
        self.knnvc_model = knn_vc(pretrained=True, prematched=True, device='cpu')
        self.source_file_path = None
        self.reference_file_paths = None
    def convert_to_mono_wav(self, input_file):
        try:
            output_file = input_file
            data, samplerate = sf.read(input_file)
            if len(data.shape) > 1:
                data = np.mean(data, axis=1)
            sf.write(output_file, data, samplerate, subtype='PCM_16')
            print(f"Converted file saved to: {output_file}")
        except Exception as e:
            print(f"Error: {e}")
    def update_source_file(self, source_file_path):
        self.convert_to_mono_wav(input_file = source_file_path)
        self.source_file_path = source_file_path
    def update_reference_files(self, reference_file_paths):
        for i in range(len(reference_file_paths)):
            reference_file_path = reference_file_paths[i]
            self.convert_to_mono_wav(input_file = reference_file_path)
        self.reference_file_paths = reference_file_paths
    def run(self, source_file_path, reference_file_paths, output_name, k = 4, sampling_rate = 16000):
        self.update_source_file(source_file_path)
        self.update_reference_files(reference_file_paths)
        query_seq = self.knnvc_model.get_features(self.source_file_path)
        matching_set = self.knnvc_model.get_matching_set(self.reference_file_paths)
        out_wav = self.knnvc_model.match(query_seq, matching_set, topk=k)
        torchaudio.save(f'./out/{output_name}.wav', out_wav[None], sampling_rate)
