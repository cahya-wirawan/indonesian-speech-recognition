import pandas as pd
from pathlib import Path
from google.cloud import texttospeech

data_dir = Path("../data/commonvoice/id")
output_dir = Path("../data/output")

voice_types = [
    {
        "language_code": "id-ID",
        "name": "id-ID-Wavenet-A",
        "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE
    },
    {
        "language_code": "id-ID",
        "name": "id-ID-Wavenet-C",
        "ssml_gender": texttospeech.SsmlVoiceGender.MALE
    },
]

def synthesize_text(text, file_name, voice_type):
    """Synthesizes speech from the input string of text."""
    path = output_dir/voice_type["name"]
    path.mkdir(parents=True, exist_ok=True)
    file = path/file_name
    if file.exists():
        return
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(voice_type)

    audio_config = texttospeech.AudioConfig({
        "audio_encoding": texttospeech.AudioEncoding.MP3
    })

    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)


    # The response's audio_content is binary.
    with open(path/file_name, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file {file_name}')

def main():
    df = pd.read_csv(data_dir/"validated.tsv", sep='\t', header=0)
    for voice_type in voice_types:
        for i, row in df.iterrows():
            # print(row["path"], row["sentence"])
            synthesize_text(row["sentence"], row["path"], voice_type)

if __name__ == "__main__":
    main()