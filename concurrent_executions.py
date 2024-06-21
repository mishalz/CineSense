import time
import concurrent.futures
from VideoFile import VideoFile
from typing import Optional

#defines a helper function to call the transcribe_audio method on each video 
def audio_transcriber_helper(video:VideoFile) -> None:
        video.transcribe_audio()

def parallel_audio_transcriber(videos: list[VideoFile], max_no_of_threads: Optional[int] = None) -> None:
    """
    Transcribes the audios of all VideoFile objects using concurrency for parallelism.

    Parameters:
        videos: the array of VideoFile objects.
        max_no_of_threads [optional]: to define the number of workers that could execute a function at one time.

    Returns:
        None    
    """

    if(max_no_of_threads == None):
        max_no_of_threads = len(videos)
    try:
        start = time.perf_counter()

        with concurrent.futures.ProcessPoolExecutor(max_workers=max_no_of_threads) as executor:
            executor.map(audio_transcriber_helper, videos)

        end = time.perf_counter()
        print(f'Time took to transcribe audios from the videos in parallel [concurrency, processes]: {end - start} second(s)')

    except Exception as e:
        print('Failed to transcribe audios concurrently.')
        print(e)


        