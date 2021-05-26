from pathlib import Path
from langdetect import detect

news_path = Path("/mnt/mldata/data/newspapers/newspapers.txt")
voices_path = Path("/mnt/mldata/data/ASR/news/newspapers.tsv")
min_text_length = 15

with open(news_path, "r") as news:
    i = 1
    with open(voices_path, "w") as voices:
        voices.write(f'path\tsentence\n')
        for line in news:
            if line != "\n" and len(line) > min_text_length:
                line = line.strip()
                try:
                    lang = detect(line)
                    if lang == "id":
                        sentences = line.split(". ")
                        for sentence in sentences:
                            if len(sentence) > min_text_length:
                                if (i-1) % 10000 == 0:
                                    print(f'{i:012}.ogg\t{sentence}')
                                voices.write(f'{i:012}.ogg\t{sentence}\n')
                                i += 1
                except Exception as e:
                    print(e)