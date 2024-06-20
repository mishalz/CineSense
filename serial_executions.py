import time

def serial_video_downloader(videos, data_folder) -> None:
    """
    Downloads an array of videos provided, one after another.

    Parameters:
        videos: the array of VideoFile objects
        data_folder: the folder name where all videos are to be downloaded.
    
    Returns:
        None    
    """
    start=time.perf_counter()

    for video in videos:
        video.download_video(data_folder)

    end=time.perf_counter()

    print(f'Time took to download the videos serially: {round(end-start,2)} second(s)')

def serial_audio_extractor(videos) -> None:
    """
    Extracts audios from an array of VideoFile objects provided, one after another.

    Parameters:
        videos: the array of VideoFile objects
    
    Returns:
        None    
    """
    start=time.perf_counter()

    for video in videos:
        video.extract_audio()

    end=time.perf_counter()
    
    print(f'Time took to extract audios from the videos serially: {round(end-start,2)} second(s)')