import threading
import time

# <-------------------------------- Helper Function ------------------------------->

def parallel_downloader_helper(videos,thread_builder,descriptive_text):
    threads=[]
    start=time.perf_counter()
    for i,video in enumerate(videos):
        thread = thread_builder(video,i)
        threads.append(thread)
        thread.start()
   
    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    end=time.perf_counter()
    print(f'Time took to {descriptive_text} the videos parallel: {round(end-start,2)} second(s)')

# <-------------------------------- Parallel Functions ------------------------------->

def parallel_video_downloader(videos):
    """
    Parameters:
        filepath: the file containing the URLs of youtube videos
    
    Returns:
        urls: A list of strings containing the URLs
    """
    semaphore = threading.Semaphore(5)

    def thread_builder(video,index):
        thread = threading.Thread(target=video.download_video,args=(semaphore,index))
        return thread

    parallel_downloader_helper(videos,thread_builder,'download')


    
def parallel_video_downloader_and_logger(filename,videos):
    """
    Parameters:
    
    Returns:

    """
    lock = threading.Lock()
   
    def thread_builder(video,index):
        thread = threading.Thread(target=video.download_video_and_log,args=(filename,lock,index))
        return thread

    parallel_downloader_helper(videos,thread_builder,'download and log')
  
def parallel_audio_extractor(videos):
    """
    Parameters:
        filepath: the file containing the URLs of youtube videos
    
    Returns:
        urls: A list of strings containing the URLs
    """
    def thread_builder(video,index):
        thread = threading.Thread(target=video.extract_audio,args=[index])
        return thread

    parallel_downloader_helper(videos,thread_builder,'extract audio from')

      
def parallel_audio_transcriber(videos):
    """
    Parameters:
        filepath: the file containing the URLs of youtube videos
    
    Returns:
        urls: A list of strings containing the URLs
    """
    def thread_builder(video,index):
        thread = threading.Thread(target=video.transcribe_audio,args=[index])
        return thread

    parallel_downloader_helper(videos,thread_builder,'transcribe audio from')
      
def parallel_sentiment_analyser(videos):
    """
    Parameters:
        filepath: the file containing the URLs of youtube videos
    
    Returns:
        urls: A list of strings containing the URLs
    """
    def thread_builder(video,index):
        thread = threading.Thread(target=video.sentiment_analysis,args=[index])
        return thread

    parallel_downloader_helper(videos,thread_builder,'perform sentiment analysis on')
      
def parallel_text_translator(videos, lang_from, lang_to, lang_name):
    """
    Parameters:
        filepath: the file containing the URLs of youtube videos
    
    Returns:
        urls: A list of strings containing the URLs
    """
    def thread_builder(video,index):
        thread = threading.Thread(target=video.translate_text,args=(index, lang_from, lang_to, lang_name))
        return thread

    parallel_downloader_helper(videos,thread_builder,f'translate in {lang_name}')
      
def parallel_emotion_extractor(videos):
    """
    Parameters:
        filepath: the file containing the URLs of youtube videos
    
    Returns:
        urls: A list of strings containing the URLs
    """
    def thread_builder(video,index):
        thread = threading.Thread(target=video.translate_text,args=[index])
        return thread

    parallel_downloader_helper(videos,thread_builder,'extract emotion from')