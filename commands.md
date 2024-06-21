python3 -m venv venv
source venv/bin/activate
pip3 install moviepy pytube SpeechRecognition TextBlob deep_translator spacy NRCLex
pip3 install -U pip setuptools wheel
python3 -m spacy download en_core_web_sm
