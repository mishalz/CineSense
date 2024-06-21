from VideoFile import VideoFile
import multiprocessing
import time

def parallel_audio_extractor(videos: list[VideoFile], max_no_of_threads:int = None) -> None:
    """
    Extracts the audios of all VideoFile objects using processes for parallelism.

    Parameters:
        videos: the array of VideoFile objects

    Returns:
        None    
    """
    #defines a process helper function to call the extract_audio method on each video 
    def process_helper(video:VideoFile,_):
        video.extract_audio()

    if(max_no_of_threads == None):
        max_no_of_threads = len(videos)

    start=time.perf_counter()

    with multiprocessing.Pool(processes=max_no_of_threads) as process_pool:
        process_pool.map(process_helper, videos)

    end=time.perf_counter()
    print(f'Time took to extract audios from the videos in parallel [processes]: {round(end-start,2)} second(s)')
    

    

