from VideoFile import VideoFile
import serial_executions
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

    #------- Task 3 ----------
    threads_executions.parallel_video_downloader(videos,parallel_data_folder,5)
    # threads_executions.parallel_audio_extractor(videos,1)

    # serial_executions.serial_video_downloader(videos,serial_data_folder)
    serial_executions.serial_audio_extractor(videos)

    #-------------------- Task 4 ---------------------
    # threads_executions.parallel_video_downloader_and_logger(videos,'download_log.txt',parallel_data_folder)
    
    #-------------- Task 5: Subtasks -----------------
    #comparing threads, processes and concurrent execution for audio transcriber
    threads_executions.parallel_audio_transcriber(videos)
    # process_executions.parallel_audio_transcriber(videos)
    # serial_executions.serial_audio_transcriber(videos)
    # concurrent_executions.parallel_audio_transcriber(videos)

    threads_executions.parallel_sentiment_analyser(videos)
    threads_executions.parallel_text_translator(videos, 'en', 'es', 'Spanish')
    threads_executions.parallel_emotion_extractor(videos)







