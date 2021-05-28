from pathlib import Path
from langdetect import detect
from text_normalizer import TextProcessor

news_path = Path("/mnt/mldata/data/newspapers/newspapers.txt")
voices_path = Path("/mnt/mldata/data/ASR/news/newspapers.tsv")
min_text_length = 15

tp = TextProcessor()

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
                        sentence_merged = ""
                        for sentence in sentences:
                            if len(sentence) > min_text_length:
                                sentence = tp.normalize(sentence)
                                if len(sentence) + len(sentence_merged) < min_text_length*4:
                                    if sentence_merged == "":
                                        sentence_merged = sentence
                                    else:
                                        sentence_merged = sentence_merged + f'. {sentence}'
                                    continue
                                if sentence_merged == "":
                                    sentence_merged = sentence
                                else:
                                    sentence_merged = sentence_merged + f'. {sentence}'
                                if (i-1) % 10000 == 0:
                                    print(f'newspapers_{i:09}.ogg\t{sentence_merged}')
                                voices.write(f'newspapers_{i:09}.ogg\t{sentence_merged}.\n')
                                sentence_merged = ""
                                i += 1
                except Exception as e:
                    print(sentence)
                    print(e)