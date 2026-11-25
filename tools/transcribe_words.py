import sys,subprocess,numpy as np
from faster_whisper import WhisperModel
m=WhisperModel("small",compute_type="int8")
a=np.frombuffer(subprocess.run(["ffmpeg","-v","0","-i",sys.argv[1],"-f","s16le","-ac","1","-ar","16000","-"],capture_output=True).stdout,np.int16).astype(np.float32)/32768
segs,_=m.transcribe(a,language="fr",word_timestamps=True)
for s in segs:
    print(" ".join(f"{w.word.strip()}@{w.start:.2f}" for w in s.words))
