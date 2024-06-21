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
import threading
from typing import Optional

nlp = spacy.load('en_core_web_sm')
nltk.download('punkt')

class VideoFile:

    def __init__(self, url:str) -> None:
        """
        Initialised the VideoFile object with attributes: URL, title, path where the video is downloaded, path of the file with the 
        extracted audio subtitles of the video, path of the text file where the subtitles of the video are stored, path of the file 
        where the translated text of the video is stored, sentiments of the Video.

        Parameters:
            url: The Youtube URL of the video
            
        Returns:
            None
            
        """
        self.url:str = url
        self.title:str = None
        self.filename:str = None
        self.folder_name:str = None
        self.video_path:str = None
        self.audio_path:str = None
        self.subtitles:str = None
        self.text_path:str = None
        self.translated_text_path:str = None
        self.sentiments_path:str = None
        self.emotions_path:str = None
        self.sentiment:tuple = {}
 
 # <-------------------------------- Video Downloading Functions ------------------------------->

    def download_video(self, data_folder:str,semaphore:Optional[threading.Semaphore] = None) -> None:
        """
        Downloads a video from YouTube.

        Parameters:
            data_folder: the folder name where the videos will be stored, each in their own folder.
            semaphore [optional]: to restrict the number of videos to be downloaded at a time.
            
        Returns:
            None

        """
        if(semaphore!=None):
            semaphore.acquire()
        try:
            yt = YouTube(self.url)
            self.title = yt.title
            self.filename = '_'.join(self.title.split()[0:2])
            self.folder_name = data_folder+self.filename
            stream = yt.streams.get_lowest_resolution() 
            print(f"Downloading video titled: {self.title}")
            self.video_path = stream.download(output_path=self.folder_name, filename=self.filename+'.mp4')
            print(f"SUCCESSFULL - Download completed to: {self.video_path}")

        except Exception as e: 
            print(f"UNSUCCESSFUL - failed to complete downloading video from {self.url}")
            print(e)

        finally:
            if(semaphore!=None):
                semaphore.release()

    def download_video_and_log(self, filename:str, data_folder:str, lock:threading.Lock, thread_id:int) -> None:
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
            self.download_video(data_folder) #calls the base download function

            self.log= f'"Timestamp": {time.strftime("%H:%M, %d %b %Y", time.gmtime())}, "URL":"{self.url}", "Download":True, "Thread ID": {thread_id}\n'
            self.save_to_file(filename,'a', self.log)
            print(f"SUCCESSFUL - Thread {thread_id} completed downloading and logging the video {self.title}.")

        except Exception as e: 
            print(f"UNSUCCESSFUL - Thread {thread_id} could not complete downloading and logging the video {self.title}.")
            print(e)

        finally:
            lock.release()
            print(f"DOWNLOADING :: Thread {thread_id} released a lock.")

# <-------------------------------- Video Analysis Sub Tasks ------------------------------->


    def extract_audio(self,semaphore:Optional[threading.Semaphore] = None) -> None:
        """
        Extracts the audio from the video file and saves it into a .wav file.

        Parameters:
            semaphore [optional]: to restrict the number of audios to be extracted at a time.

        Returns:
            None
        """
        if(semaphore != None):
            semaphore.acquire()
        try:
            self.audio_path = os.path.join(self.folder_name, self.filename + ".wav")

            print(f"SUBTASK 1 :: Starting extraction of the audio from file {self.title}")
            video = moviepy.editor.VideoFileClip(self.video_path)
            video.audio.write_audiofile(self.audio_path)
            print(f"SUBTASK 1 :: extraction completed {self.title}")

        except Exception as e: 
             print(f"UNSUCCESSFUL - failed to extract audio from file {self.title}.")
             print(e)

        finally:
            if(semaphore != None):
                semaphore.release()
     
    def transcribe_audio(self, semaphore:Optional[threading.Semaphore] = None) -> None:
        """
        Extracts the text from the audio file and saves it into a .txt file.

        Parameters:
            semaphore: to restrict the number of audios to be transcribed at a time.
            
        Returns:
            None
            
        """
        if(semaphore != None):
            semaphore.acquire()
        try:
            print(f"SUBTASK 2 :: started transcribing audio from file {self.audio_path} to text")

            recognizer = sr.Recognizer()
            with sr.AudioFile(self.audio_path) as source:
                audio = recognizer.record(source)
            self.subtitles = recognizer.recognize_google(audio)
            self.text_path = os.path.join(self.folder_name, self.filename + ".txt")

            print(f"SUBTASK 2 :: Saving the text to file: {self.text_path}")
            self.save_to_file(self.text_path,'w',self.subtitles)

            print(f"SUCCESSFUL -  completed transcribing audio from file{self.title}.")

        except Exception as e: 
            print(f"UNSUCCESSFUL - failed to not transcribe audio from file {self.title}.")
            print(e)

        finally:
            if(semaphore != None):
                semaphore.release()

    def sentiment_analysis(self,semaphore:Optional[threading.Semaphore] = None) -> None:
        """
        Performs Sentiment Analysis on the video and saves the polarity and subjectivity measure of the content, into a .txt file.

        Parameters:
            semaphore: to restrict the number of audios to be transcribed at a time.
            
        Returns:
            None
            
        """
        if(semaphore != None):
            semaphore.acquire()

        try:
            print(f"SUBTASK 3 :: started sentiment analysis on file {self.title}")

            text_to_analyse = self.get_text_from_file()
            blob = TextBlob(text_to_analyse)
            self.sentiment = blob.sentiment
            sentiments_output = f"Polarity measure of the video {self.title} is: {self.sentiment.polarity}\nSubjectivity measure of the video {self.title} is: {self.sentiment.subjectivity}"
            print(sentiments_output)

            self.sentiments_path = os.path.join(self.folder_name, self.filename + "_sentiments.txt")
            print(f"SUBTASK 3 :: saving the sentiments to file: {self.sentiments_path}")
            self.save_to_file(self.sentiments_path,'w',sentiments_output)

            print(f"SUCCESSFUL - completed sentiment analysis on file {self.title}.")

        except Exception as e: 
            print(f"UNSUCCESSFUL - failed to perform sentiment analysis on file {self.title}.")
            print(e)
        
        finally:
            if(semaphore != None):
                semaphore.release()

    def translate_text(self, lang_from:str, lang_to:str, lang_to_name:str, semaphore:Optional[threading.Semaphore] = None) -> None:
        """
        Translates the transcribed text into a given language and saves it in a .txt file.

        Parameters:
            lang_from: The original language of the text.
            lang_to: The language to translate the text into.
            lang_to_name: The name in English of the language that the text is to be translated into.    
            semaphore: to restrict the number of texts to be translated at a time.

        Returns:
            None
            
        """
        if(semaphore != None):
            semaphore.acquire()
        try:
            print(f"SUBTASK 4 :: started translating the video {self.title} to {lang_to_name}")

            text_to_analyse = self.get_text_from_file()
            text_translated = GoogleTranslator(source=lang_from, target=lang_to).translate(text=text_to_analyse)
            self.translated_text_path = os.path.join(self.folder_name, self.filename + "_"+lang_to_name+".txt")

            print(f"SUBTASK 4 :: saving the translated text to file: {self.translated_text_path}")
            self.save_to_file(self.translated_text_path,'w',text_translated)

            print(f"SUCCESSFUL - completed translation of the video {self.title}.")

        except Exception as e: 
            print(f"UNSUCCESSFUL - failed to translate the video {self.title}.")
            print(e)

        finally:
            if(semaphore != None):
                semaphore.release()
       
    def extract_emotions(self, semaphore:Optional[threading.Semaphore] = None) -> None:
        """
        Extracts the emotions from the transcribed .txt file of the video and saves it in a separate .txt file.

        Parameters:
            semaphore: to restrict the number of videos that are processed at a time, for emotion extraction.    
            
        Returns:
            None
            
        """
        if(semaphore != None):
            semaphore.acquire()        
        try:
            print(f"SUBTASK 5 :: started extracting emotions from the video {self.title}")

            text_to_analyse = self.get_text_from_file()
            doc = nlp(text_to_analyse)
            full_text = ' '.join([sent.text for sent in doc.sents])
            emotion = NRCLex(full_text)
            emotion_output = emotion.affect_frequencies

            print(f"SUBTASK 5 :: Emotions and Frequencies for the video {self.title}: {emotion_output}")
            
            self.emotions_path = os.path.join(self.folder_name, self.filename + "_emotions.txt")
            print(f"SUBTASK 5 :: saving the emotions and frequencies to file: {self.emotions_path}")
            with open(self.emotions_path, "w") as outfile:
                print(emotion_output, file=outfile)
                
        except Exception as e:
            print(f"UNSUCCESSFUL - failed to extract emotions from the video {self.title}.")
            print(e)

        finally:
            if(semaphore != None):
                semaphore.release()
        

# <-------------------------------- Helper Functions ------------------------------->

    def save_to_file(self,filename:str,mode:str,text:str) -> None:
        """
        Writes a given text to a file.

        Parameters:
            filename: Path of the file where the text is to be written.
            mode: the mode in which to open the file.
            text: the text that is to be saved in the file.
            
        Returns:
            None
        """
        with open(filename, mode) as file:
            file.write(text)
        print(f'Text has been written to {filename}')

    def get_text_from_file(self) -> str:
        """
        Retrieves the transcribed text of each video.

        Parameters:
            None
            
        Returns:
            the transcribed text of a video.
        """

        #if the text is not saved in the subtitles attribute of the videofile object then it is retrieved from the text file.
        if(self.subtitles == None):
            if(self.text_path == None):
                raise Exception('Could not find the transcribed text of the video {self.title}') 
            else:
                text_file = open(self.text_path,'r')
                text_to_analyse = text_file.read()
                print(f"Retrieved text from {self.text_path}")
                return text_to_analyse
        else:
            return self.subtitles
