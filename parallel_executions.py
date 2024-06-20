import threading
import time
import multiprocessing
import concurrent.futures

# <-------------------------------- Helper Function ------------------------------->

def parallel_downloader_helper(videos,thread_builder,descriptive_text) -> None:
    """
    A helper function that creates threads/process for each video and joins them.

    Parameters:
        videos: the array of VideoFile objects
        thread_builder: a function that is passed that is called to get a customised thread.
        descriptive_text: to print out the specific functionality of the function that calls this helper function.
    
    Returns:
        None
    """

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
    print(f'Time took to {descriptive_text} the videos in parallel: {round(end-start,2)} second(s)')

# <-------------------------------- Parallel Functions ------------------------------->

def parallel_video_downloader(videos, data_folder, max_no_of_threads = None) -> None:
    """
    Downloads an array of videos provided, using threads.

    Parameters:
        videos: the array of VideoFile objects
        data_folder: the folder name where all videos are to be downloaded.
        max_no_of_threads [optional]: to define the number of threads that could execute a function at one time.
    
    Returns:
        None    
    """

    #if the max_no_of_threads are not defined, it is creates as many threads as there are videos in the array.
    if(max_no_of_threads == None):
        max_no_of_threads = len(videos)

    semaphore = threading.Semaphore(max_no_of_threads)

    def thread_builder(video,_):
        thread = threading.Thread(target=video.download_video,args=(data_folder,semaphore))
        return thread

    #calling the helper function by passing it the thread_builder function.
    parallel_downloader_helper(videos,thread_builder,'download')


def parallel_video_downloader_and_logger(videos, filename, data_folder) -> None:
    """
    Downloads an array of videos provided, using threads and logs the details in the logger file.

    Parameters:        
        videos: the array of VideoFile objects
        filename: the path of the logger file
        data_folder: the folder name where all videos are to be downloaded.
    
    Returns:
        None
    """

    #using a mutex instead of a sempahore since only one thread should be able to access the logger file at a time.
    lock = threading.Lock()
   
    def thread_builder(video,index):
        thread = threading.Thread(target=video.download_video_and_log,args=(filename,data_folder, lock,index))
        return thread

    parallel_downloader_helper(videos,thread_builder,'download and log')
  

def parallel_audio_extractor_with_threads(videos,max_no_of_threads = None) -> None:
    """
    Extracts the audios of all VideoFile objects using threads for parallelism.

    Parameters:
        videos: the array of VideoFile objects
        max_no_of_threads [optional]: to define the number of threads that could execute a function at one time.

    Returns:
        None    
    """

    if(max_no_of_threads == None):
        max_no_of_threads = len(videos)

    semaphore = threading.Semaphore(max_no_of_threads)

    def thread_builder(video,_):
        thread = threading.Thread(target=video.extract_audio,args=[semaphore])
        return thread

    parallel_downloader_helper(videos,thread_builder,'extract audio from [using threads]')


def parallel_audio_extractor_with_processes(videos) -> None:
    """
    Extracts the audios of all VideoFile objects using processes for parallelism.

    Parameters:
        videos: the array of VideoFile objects

    Returns:
        None    
    """
    
    #defines a process builder instead of the thread builder
    def process_builder(video,_):
        process = multiprocessing.Process(target=video.extract_audio)
        return process

    parallel_downloader_helper(videos,process_builder,'extract audio from [using processes]')

def parallel_audio_extractor_with_concurrency(videos) -> None:
    """
    Extracts the audios of all VideoFile objects using concurrency for parallelism.

    Parameters:
        videos: the array of VideoFile objects

    Returns:
        None    
    """

    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(parallel_audio_extractor_with_concurrency_helper, videos)
    end = time.perf_counter()
    print(f'Time took to extract audio from [using concurrency] the videos in parallel: {end - start} second(s)')

def parallel_audio_extractor_with_concurrency_helper(video) -> None:
    """
    Calls the extract_audio method on a VideoFile object.

    Parameters:
        video: a VideoFile object

    Returns:
        None    
    """
    video.extract_audio()

def parallel_audio_transcriber(videos,max_no_of_threads=None) -> None:
    """
    Transcribes the audios of all VideoFile objects using threads for parallelism.

    Parameters:
        videos: the array of VideoFile objects.
        max_no_of_threads [optional]: to define the number of threads that could execute a function at one time.

    Returns:
        None    
    """
    if(max_no_of_threads == None):
        max_no_of_threads = len(videos)

    semaphore = threading.Semaphore(max_no_of_threads)
    
    def thread_builder(video,_):
        thread = threading.Thread(target=video.transcribe_audio,args=[semaphore])
        return thread

    parallel_downloader_helper(videos,thread_builder,'transcribe audio from')
      
def parallel_sentiment_analyser(videos, max_no_of_threads = None) -> None:
    """
    Performs sentiment analysis on all VideoFile objects using threads for parallelism.

    Parameters:
        videos: the array of VideoFile objects.
        max_no_of_threads [optional]: to define the number of threads that could execute a function at one time.

    Returns:
        None    
    """

    if(max_no_of_threads == None):
        max_no_of_threads = len(videos)

    semaphore = threading.Semaphore(max_no_of_threads)

    def thread_builder(video,index):
        thread = threading.Thread(target=video.sentiment_analysis,args=[semaphore])
        return thread

    parallel_downloader_helper(videos,thread_builder,'perform sentiment analysis on')
      
def parallel_text_translator(videos, lang_from, lang_to, lang_name, max_no_of_threads=None) -> None:
    """
    Translates the transcribed text of all VideoFile objects using threads for parallelism.

    Parameters:
        videos: the array of VideoFile objects.
        lang_from: The original language of the text.
        lang_to: The language to translate the text into.
        lang_to_name: The name in English of the language that the text is to be translated into.  
        max_no_of_threads [optional]: to define the number of threads that could execute a function at one time.

    Returns:
        None    
    """
    if(max_no_of_threads == None):
        max_no_of_threads = len(videos)
    
    semaphore = threading.Semaphore(max_no_of_threads)

    def thread_builder(video,index):
        thread = threading.Thread(target=video.translate_text,args=( lang_from, lang_to, lang_name,semaphore))
        return thread

    parallel_downloader_helper(videos,thread_builder,f'translate in {lang_name}')
      
def parallel_emotion_extractor(videos, max_no_of_threads = None) -> None:
    """
    Extracts the emotions of all VideoFile objects using threads for parallelism.

    Parameters:
        videos: the array of VideoFile objects.
        max_no_of_threads [optional]: to define the number of threads that could execute a function at one time.

    Returns:
        None    
    """
    if(max_no_of_threads == None):
        max_no_of_threads = len(videos)

    semaphore = threading.Semaphore(max_no_of_threads)

    def thread_builder(video,_):
        thread = threading.Thread(target=video.extract_emotions,args=[semaphore])
        return thread

    parallel_downloader_helper(videos,thread_builder,'extract emotion from')