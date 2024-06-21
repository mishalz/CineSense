from VideoFile import VideoFile
from serial_executions import serial_video_downloader,serial_audio_extractor
import process_executions
import threads_executions
import concurrent_executions


def read_urls(filepath):
    """
    Reads the file of urls and returns a list of urls

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

    #----------------- Task 2 ----------------------
    urls = read_urls('video_urls.txt')
    videos=[]
    for url in urls:
        videos.append(VideoFile(url))
    
    parallel_data_folder = 'video_data/'
    serial_data_folder = 'serial_video_data/'

    #------- Task 3 and Task 5: Comparison ----------
    threads_executions.parallel_video_downloader(videos,parallel_data_folder,5)
    threads_executions.parallel_audio_extractor(videos,1)
    # process_executions.parallel_audio_extractor(videos)
    # concurrent_executions.parallel_audio_extractor(videos)

    # serial_video_downloader(videos,serial_data_folder)
    # serial_audio_extractor(videos)

    #-------------------- Task 4 ---------------------
    # parallel_video_downloader_and_logger(videos,'download_log.txt',parallel_data_folder)
    
    #-------------- Task 5: Subtasks -----------------
    concurrent_executions.parallel_audio_transcriber(videos)
    # parallel_audio_transcriber_with_processes(videos)

    # parallel_sentiment_analyser(videos)
    # parallel_text_translator(videos,'en','es','Spanish')
    # parallel_emotion_extractor(videos)






