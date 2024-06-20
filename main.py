from VideoFile import VideoFile
from parallel_executions import parallel_video_downloader, parallel_video_downloader_and_logger, parallel_audio_extractor_with_processes, parallel_audio_extractor_with_concurrency, parallel_audio_extractor_with_threads, parallel_audio_transcriber, parallel_text_translator, parallel_emotion_extractor,parallel_sentiment_analyser
from serial_executions import serial_video_downloader,serial_audio_extractor

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
    parallel_video_downloader(videos,parallel_data_folder,5)
    parallel_audio_extractor_with_threads(videos,1)
    # parallel_audio_extractor_with_processes(videos)
    # parallel_audio_extractor_with_concurrency(videos)

    # serial_video_downloader(videos,serial_data_folder)
    # serial_audio_extractor(videos)

    #-------------------- Task 4 ---------------------
    parallel_video_downloader_and_logger(videos,'download_log.txt',parallel_data_folder)
    
    #-------------- Task 5: Subtasks -----------------
    parallel_audio_transcriber(videos)
    parallel_sentiment_analyser(videos)
    parallel_text_translator(videos,'en','es','Spanish')
    parallel_emotion_extractor(videos)






