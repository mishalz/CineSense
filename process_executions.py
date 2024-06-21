from VideoFile import VideoFile
import multiprocessing
import time
from typing import Optional

#defines a process helper function to call the extract_audio method on each video 
def audio_transcriber_helper(video:VideoFile):
        video.transcribe_audio()

def parallel_audio_transcriber(videos: list[VideoFile], max_no_of_threads:Optional[int] = None) -> None:
    """
    Transcribe the audios of all VideoFile objects using processes for parallelism.

    Parameters:
        videos: the array of VideoFile objects
        max_no_of_threads [optional]: to define the number of processes that could execute a function at one time.


    Returns:
        None    
    """

    if(max_no_of_threads == None):
        max_no_of_threads = len(videos)

    start=time.perf_counter()

    with multiprocessing.Pool(processes=max_no_of_threads) as process_pool:
        process_pool.map(audio_transcriber_helper, videos)

    end=time.perf_counter()
    print(f'Time took to transcribe audios from the videos in parallel [processes]: {round(end-start,2)} second(s)')
    



