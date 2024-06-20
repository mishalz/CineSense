import moviepy.editor
from pytube import YouTube
import time
import os
import moviepy 
import speech_recognition as sr
from textblob import TextBlob
from deep_translator import GoogleTranslator
import spacy
import nltk
from nrclex import NRCLex

nlp = spacy.load('en_core_web_sm')
nltk.download('punkt')

class VideoFile:

    def __init__(self, url) -> None:
        """
        Initialised the VideoFile object with attributes: URL, title, path where the video is downloaded, path of the file with the extracted audio
        subtitles of the video, path of the text file where the subtitles of the video are stored, path of the file where the translated 
        text of the video is stored, sentiments of the Video.

        Parameters:
            url: The Youtube URL of the video
            
        Returns:
            None
            
        """
        self.url=url
        self.title=None
        self.filename=None
        self.folder_name=None
        self.video_path=None
        self.audio_path=None
        self.subtitles=None
        self.text_path=None
        self.translated_text_path=None
        self.sentiment ={}
 
 # <-------------------------------- Video Downloading Functions ------------------------------->

    def download_video(self,semaphore,thread_id) -> None:
        """
        Downloads a video from YouTube

        Parameters:
            output_folder: the folder name where the 
            
        Returns:
            
        """
        semaphore.acquire()
        print(f"DOWNLOADING :: Thread {thread_id} acquired a lock to download video.") 
        try:
            yt = YouTube(self.url)
            self.title = yt.title
            self.filename = '_'.join(self.title.split()[0:2])
            self.folder_name = 'video_data/'+self.filename
            stream = yt.streams.get_lowest_resolution() 
            print(f"Downloading video titled: {self.title}")
            self.video_path = stream.download(output_path=self.folder_name, filename=self.filename+'.mp4')
            print(f"SUCCESSFULL - Download completed to: {self.video_path}")
        except Exception as e: 
            print(f"UNSUCCESSFUL - Thread {thread_id} could not complete downloading video.")
            print(e)
        finally:
            semaphore.release()
            print(f"DOWNLOADING :: Thread {thread_id} released a lock.")


    def download_video_and_log(self, filename, lock, thread_id) -> None:
        """
        Downloads a video from YouTube and logs the activity in the logger file.

        Parameters:
            filename: The name of the logger file where all the logs are stored.
            lock: The mutex that will be acquired while writting to the logger.
            thread_id: The unique index assigned to the thread.
            
        Returns:
            None
        """
        lock.acquire()
        try:
            print(f"DOWNLOADING :: Thread {thread_id} acquired a lock.")
            self.download_video()

            self.log= f'"Timestamp": {time.strftime("%H:%M, %d %b %Y", time.gmtime())}, "URL":"{self.url}", "Download":True, "Thread ID": {thread_id}\n'
            self.save_to_file(filename,'a', self.log)
            print(f"SUCCESSFUL - Thread {thread_id} completed downloading and logging the video {self.title}.")
        except Exception as e: 
            print(f"UNSUCCESSFUL - Thread {thread_id} could not complete downloading and video {self.title}.")
            print(e)
        finally:
            lock.release()
            print(f"DOWNLOADING :: Thread {thread_id} released a lock.")

# <-------------------------------- Video Analysis Functions ------------------------------->


    def extract_audio(self,thread_id,semaphore) -> None:
        """
        Extracts the audio from the video file and saves it into a .wav file.

        Parameters:
            None

        Returns:
            None
        """
        semaphore.acquire()
        try:
            self.audio_path = os.path.join(self.folder_name, self.filename + ".wav")
            print(f"SUBTASK 1 :: Thread {thread_id} started extracting audio from file {self.title}")
            video = moviepy.editor.VideoFileClip(self.video_path)
            video.audio.write_audiofile(self.audio_path)
            print(f"SUBTASK 1 :: Extraction completed {self.title}")
            print(f"SUCCESSFUL - Thread {thread_id} completed extracting audio from file{self.title}.")
        except Exception as e: 
             print(f"UNSUCCESSFUL - Thread {thread_id} could not extract audio from file {self.title}.")
             print(e)
        finally:
            print(f"SUBTASK 1 :: Thread {thread_id} released a lock.")
            semaphore.release()
     
    def transcribe_audio(self,thread_id,semaphore) -> None:
        """
        Extracts the text from the audio file and saves it into a .txt file.

        Parameters:
            None    
            
        Returns:
            None
            
        """
        semaphore.acquire()
        try:
            print(f"SUBTASK 2 :: Thread {thread_id} started transcribing audio from file {self.audio_path} to text")
            recognizer = sr.Recognizer()
            with sr.AudioFile(self.audio_path) as source:
                audio = recognizer.record(source)
            self.subtitles = recognizer.recognize_google(audio)
            self.text_path = os.path.join(self.folder_name, self.filename + ".txt")
            print(f"SUBTASK 2 :: Saving the text to file: {self.text_path}")
            self.save_to_file(self.text_path,'w',self.subtitles)
            print(f"SUCCESSFUL - Thread {thread_id} completed transcribing audio from file{self.title}.")
        except Exception as e: 
            print(f"UNSUCCESSFUL - Thread {thread_id} could not transcribe audio from file {self.title}.")
            print(e)
        finally:
            print(f"SUBTASK 2 :: Thread {thread_id} released a lock.")
            semaphore.release()   

    def sentiment_analysis(self,thread_id,semaphore) -> None:
        """
        Performs Sentiment Analysis on the video and prints out the polarity and subjectivity measure of the content.

        Parameters:
            None    
            
        Returns:
            None
            
        """
        semaphore.acquire()
        try:
            print(f"SUBTASK 3 :: Thread {thread_id} started sentiment analysis on file {self.title}")
            text_to_analyse = self.get_text_from_file()
            blob = TextBlob(text_to_analyse)
            self.sentiment = blob.sentiment
            print(f"Polarity measure of the video {self.title} is: {self.sentiment.polarity}")
            print(f"Subjectivity measure of the video {self.title} is: {self.sentiment.subjectivity}")
            print(f"SUCCESSFUL - Thread {thread_id} completed sentiment analysis on file {self.title}.")

        except Exception as e: 
            print(f"UNSUCCESSFUL - Thread {thread_id} could not perform sentiment analysis on file {self.title}.")
            print(e)
        
        finally:
            print(f"SUBTASK 3 :: Thread {thread_id} released a lock.")
            semaphore.release() 

    def translate_text(self, thread_id, lang_from, lang_to, lang_to_name, semaphore) -> None:
        """
        Translates the transcribed text into a given language.

        Parameters:
            lang_from: The original language of the text.
            lang_to: The language to translate the text into.
            lang_to_name: The name in English of the language that the text is to be translated into.    
            
        Returns:
            None
            
        """
        print(f"SUBTASK 4 :: Thread {thread_id} started translating the video {self.title} to {lang_to_name}")
        semaphore.acquire()
        try:
            text_to_analyse = self.get_text_from_file()
            text_translated = GoogleTranslator(source=lang_from, target=lang_to).translate(text=text_to_analyse)
            self.translated_text_path = os.path.join(self.folder_name, self.filename + "_"+lang_to_name+".txt")
            print(f"SUBTASK 4 :: Thread {thread_id} Saving the translated text to file: {self.translated_text_path}")
            self.save_to_file(self.translated_text_path,'w',text_translated)
            print(f"SUCCESSFUL - Thread {thread_id} completed translation of the video {self.title}.")
        except Exception as e: 
            print(f"UNSUCCESSFUL - Thread {thread_id} could not translate the video {self.title}.")
            print(e)
        finally:
            print(f"SUBTASK 4 :: Thread {thread_id} released a lock.")
            semaphore.release() 
       
    def extract_emotions(self, thread_id, semaphore) -> None:
        """
        Translates the transcribed text into a given language.

        Parameters:
            lang_from: The original language of the text.
            lang_to: The language to translate the text into.
            lang_to_name: The name in English of the language that the text is to be translated into.    
            
        Returns:
            None
            
        """
        semaphore.acquire()
        print(f"SUBTASK 5 :: Thread {thread_id} started extracting emotions from the video {self.title}")
        try:
            text_to_analyse = self.get_text_from_file()
            doc = nlp(text_to_analyse)
            full_text = ' '.join([sent.text for sent in doc.sents])
            emotion = NRCLex(full_text)
            print(f"SUBTASK 5 :: Emotions and Frequencies for the video {self.title}: {emotion.affect_frequencies}")
        except Exception as e:
            print(f"UNSUCCESSFUL - Thread {thread_id} could not extract emotions from the video {self.title}.")
            print(e)
        finally:
            print(f"SUBTASK 5 :: Thread {thread_id} released a lock.")
            semaphore.release() 
        


# <-------------------------------- Helper Functions ------------------------------->

    def save_to_file(self,filename,mode,text) -> None:
        """
        Parameters:
            
            
        Returns:
            
        """
        with open(filename, mode) as file:
            file.write(text)
        print(f'Text has been written to {filename}')


    def get_text_from_file(self) -> str:
        if(self.subtitles == None):
            if(self.text_path == None):
                raise Exception('Could not find the transcribes text of the video {self.title}') 
            else:
                text_file = open(self.text_path,'r')
                text_to_analyse = text_file.read()
                print(f"Retrieved text from {self.text_path}")
                return text_to_analyse
        else:
            return self.subtitles

    def to_string(self) -> None:
        print(f"Video Details: \n\tURL: {self.url}\n\tTitle: {self.title}\n\tVideo path: {self.video_path} path: {self.audio_path}\n\tText file path: {self.text_path}\n\tSentiments of the video: {self.sentiment}")
