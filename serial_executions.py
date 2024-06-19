import time

def serial_video_downloader(videos):
    """
    Parameters:
        filepath: the file containing the URLs of youtube videos
    
    Returns:
        urls: A list of strings containing the URLs
    """
    start=time.perf_counter()
    for video in videos:
        video.download_video()
    end=time.perf_counter()
    print(f'Time took to download the videos serially: {round(end-start,2)} second(s)')
