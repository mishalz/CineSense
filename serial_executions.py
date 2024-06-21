import time
from VideoFile import VideoFile

def serial_video_downloader(videos:list[VideoFile], data_folder:str) -> None:
    """
    Downloads an array of videos provided, one after another.

    Parameters:
        videos: the array of videos to be downloaded
        data_folder: the folder name where all videos are to be downloaded.
    
    Returns:
        None    
    """
    start=time.perf_counter()

    for video in videos:
        video.download_video(data_folder)

    end=time.perf_counter()

    print(f'Time took to download the videos serially: {round(end-start,2)} second(s)')

def serial_audio_extractor(videos: list[VideoFile]) -> None:
    """
    Extracts audios from an array of VideoFile objects provided, one after another.

    Parameters:
        videos: the array of videos from which to extract audios
    
    Returns:
        None    
    """
    start=time.perf_counter()

    for video in videos:
        video.extract_audio()

    end=time.perf_counter()
    
    print(f'Time took to extract audios from the videos serially: {round(end-start,2)} second(s)')

def serial_audio_transcriber(videos: list[VideoFile]) -> None:
    """
    Transcribers audios from an array of VideoFile objects provided, one after another.

    Parameters:
        videos: the array of videos that are to be transcribed
    
    Returns:
        None    
    """
    start=time.perf_counter()

    for video in videos:
        video.transcribe_audio()

    end=time.perf_counter()
    
    print(f'Time took to transcribe audios from the videos serially: {round(end-start,2)} second(s)')