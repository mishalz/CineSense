import time
import concurrent.futures
from VideoFile import VideoFile

def concurrent_helper(videos: list[VideoFile], video_function: function, descriptive_text: str, max_no_of_threads:int = None):
    if(max_no_of_threads == None):
        max_no_of_threads = len(videos)
    try:
        start = time.perf_counter()

        with concurrent.futures.ProcessPoolExecutor(max_workers=max_no_of_threads) as executor:
            executor.map(video_function, videos)

        end = time.perf_counter()
        print(f'Time took to {descriptive_text} from the videos in parallel [concurrency, processes]: {end - start} second(s)')

    except Exception as e:
        print('Failed to {descriptive_text} concurrently.')
        print(e)


def parallel_audio_extractor(videos: list[VideoFile], max_no_of_threads:int = None) -> None:
    """
    Extracts the audios of all VideoFile objects using concurrency for parallelism.

    Parameters:
        videos: the array of VideoFile objects
        max_no_of_threads [optional]: to define the number of workers that could execute a function at one time.

    Returns:
        None    
    """
    #defines a helper function to call the extract_audio method on each video 
    def extract_audio_helper(video:VideoFile) -> None:
        video.extract_audio()

    concurrent_helper(videos, extract_audio_helper, 'extract audios', max_no_of_threads )

    

def parallel_audio_transcriber(videos: list[VideoFile], max_no_of_threads:int = None) -> None:
    """
    Transcribes the audios of all VideoFile objects using concurrency for parallelism.

    Parameters:
        videos: the array of VideoFile objects.
        max_no_of_threads [optional]: to define the number of workers that could execute a function at one time.

    Returns:
        None    
    """

    #defines a helper function to call the transcribe_audio method on each video 
    def extract_audio_helper(video:VideoFile) -> None:
        video.transcribe_audio()

    concurrent_helper(videos, extract_audio_helper, 'transcribe audios', max_no_of_threads )


        