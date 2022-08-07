import pyttsx3
from pydub import AudioSegment
from flask import Flask, request, Response
import tempfile

def init():
  engine = pyttsx3.init()
  voices = engine.getProperty('voices')
  print('Available voices:')
  for voice in voices:
    print(f'Voice: {voice.id}')
  print()
  del engine

def tts(text, rate, voice):
  with tempfile.TemporaryDirectory() as tmpdir:
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.setProperty('voice', voice)
    engine.save_to_file(text, f'{tmpdir}/tts.wav')
    engine.runAndWait()
    del engine
      
    segment = AudioSegment.from_file(f'{tmpdir}/tts.wav')
    with open(f'{tmpdir}/tts.wav', 'wb') as f:
      segment.export(f, format='mp3')

    return open(f'{tmpdir}/tts.wav', 'rb').read()

init()

app = Flask(__name__)
@app.route('/tts', methods=['GET'])
def tts_api():
  text = request.args['text']
  rate = int(request.args.get('rate', '200'))
  voice = request.args.get('voice', 'en-us')
  mp3 = tts(text, rate=rate, voice=voice)
  return Response(mp3, mimetype='audio/mpeg')
