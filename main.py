from VideoFile import VideoFile
from parallel_executions import parallel_video_downloader, parallel_video_downloader_and_logger, parallel_audio_extractor, parallel_audio_transcriber, parallel_text_translator, parallel_emotion_extractor,parallel_sentiment_analyser
from serial_executions import serial_video_downloader
from pathlib import Path

#Task 2
def read_urls(filepath):
    """
    Parameters:
        filepath: the file containing the URLs of youtube videos
    
    Returns:
        urls: A list of strings containing the URLs
    """
    file = open(filepath, "r")
    urls=[]
    for line in file:
        urls.append(line)
    file.close()
    return urls


if __name__=="__main__":


    # urls = read_urls('video_urls.txt')
    # serial_video_downloader(urls,video_output_folder)
    #parallel_video_downloader(urls)


    #Task 4
    # urls = read_urls('video_urls.txt')
    # filename = "download_log.txt"
    # parallel_video_downloader_and_logger(filename,urls)

    #Task 5
    urls = read_urls('video_urls.txt')
    videos=[]
    for url in urls:
        videos.append(VideoFile(url))
    
    parallel_video_downloader(videos,5)
    parallel_audio_extractor(videos,1)
    parallel_audio_transcriber(videos)
    parallel_sentiment_analyser(videos)
    parallel_text_translator(videos, 'en','es','Spanish')
    parallel_emotion_extractor(videos)


    # for video in videos:
        # video.to_string()



