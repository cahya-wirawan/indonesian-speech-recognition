from pathlib import Path
import librosa
import soundfile as sf

"""
The script convert the ogg files from opus subtype to with vorbis ogg. 
"""

root_dir = Path("/mnt/mldata/data/ASR/news/test")
src_dir = root_dir/"src"
dst_dir = root_dir/"dst"

for path in Path(src_dir).rglob('*.ogg'):
    print(path.name)
    data, sample_rate = librosa.load(path, sr=16000)
    dst_path = Path(str(path).replace(str(src_dir), str(dst_dir)))
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(dst_path, data, sample_rate)