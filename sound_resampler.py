import sys
from pathlib import Path
import torchaudio

"""
The script resample sound files to 16KHz and save it as ogg files. 

"""

if len(sys.argv) != 3:
    print(sys.argv[0], "<source directory> <destination directory>")
    exit(1)

src_dir = Path(sys.argv[1])
dst_dir = Path(sys.argv[2])
dst_sample_rate = 16_000

for path in Path(src_dir).rglob('*'):
    if path.suffix in [".mp3", ".ogg", ".wav"]:
        print(path.name)
        data, src_sample_rate = torchaudio.load(path)
        resampler = torchaudio.transforms.Resample(src_sample_rate, dst_sample_rate)
        data = resampler(data)
        dst_path = Path(str(path.parent).replace(str(src_dir), str(dst_dir)))
        dst_path.mkdir(parents=True, exist_ok=True)
        dst_path = dst_path/f'{path.stem}.ogg'
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        torchaudio.save(str(dst_path), data, dst_sample_rate)