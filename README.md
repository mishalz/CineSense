# CineSense - A Big Data Analysis Course Project
🎥 Welcome to CineSense

CineSense is an innovative video-processing startup that extracts valuable insights from social media video content. It uses advanced natural language processing (NLP) and computer vision techniques to analyse the sentiments and emotions of videos. This analysis is crucial for businesses seeking to understand their audience, improve customer experiences, and make data-driven decisions.

On your first day at CineSense as a data engineer, you were assigned a critical project: find the best strategy to download and analyse videos. CineSense uses YouTube videos posted by its target audience. Each video must be analysed, and results should be extracted and shared with customers. Usual tasks include extracting video, audio, text transcripts, sentiments and emotions. Since you are paired with a customer from Madrid, you will also need to transcribe videos in Spanish.

## Programming Paradigm
The project uses the Object-Oriented Paradigm. It works around a VideoFile class that contains all the attributes and methods to download and process a video. The following diagram showcases all the specifications of the VideoFile class.<img width="821" alt="Screenshot 2024-12-25 at 20 52 12" src="https://github.com/user-attachments/assets/edf31704-bb83-489c-9bd3-84c689fd34cc" />

The attributes of the class are further explained below:
1. url: The YouTube URL of the video.
2. title: The title of the YouTube video.
3. filename: The first two words of the title of the video joined with a “_” which is used to
then name all the files for the video.
4. folder_name: The folder path where the files corresponding to the video is stored.
5. video_path: The full relative path of the video file that is downloaded.
6. audio_path: The full relative path of the audio that is extracted from the video.
7. subtitles: The transcribed text of the video.
8. text_path: The full relative path of the transcribed text file of the video.
9. translated_text_path: The full relative path of the translated transcribed file of the
video.
 
10. sentiments_path: The full relative path of the text file where the output of the sentiment analysis on the video is stored.
11. sentiments: The tuple that stores the measures of the polarity and subjectivity of the video.
12. emotions_path: The full relative path of the text file where the extracted emotions of the video are stored.

## Project Components

The project is divided into two components, video downloading and video processing. This section briefly discusses the considerations while approaching the solution of each component, time and space complexities and comparison between serial and parallel execution.

### Video Downloading
The process of creating a solution for this component started by creating a function for one video to be downloaded, for this the “download_video” method was added in the VideoFile class.
It takes the url of the VideoFile object which was saved as an attribute when the object is instantiated. It also takes the folder name as a parameter; this is done to achieve flexibility while testing. After the video is downloaded, its path is stored as another attribute of the object.

After the completion of the class method, 2 functions were written to download videos: one for serial execution and the other for parallel, in the files “serial_executions.py” and “thread_executions.py” respectively. The parallel execution makes use of threads to achieve this parallelism. This is because downloading videos from their respective URLs is an I/O bound task and therefore, threads are a more resource-eYicient solution. To apply the limit of downloading only 5 videos at a time, a semaphore is used.

#### Complexities of serial execution
- Time complexity: O(n) - since it uses a loop to download each video one after the other.
- Space complexity: O(1) - since it does not take up extra space and updates the VideoFile objects passed in the arguments.
- 
#### Complexities of parallel execution
- Time complexity: It is not a suitable measure for tasks performed in parallel, but as an estimate if there is a thread for each video, the time complexity would theoretically become O(1).
- Space complexity: O(1) - since it does not take up extra space and updates the VideoFile objects passed in the arguments.
  
#### Comparing time taken by the serial and parallel execution
The following screenshots display the time it took for a set of 11 videos to be downloaded by the project, using the two approaches.<img width="797" alt="Screenshot 2024-12-25 at 21 01 51" src="https://github.com/user-attachments/assets/5f58eee8-2906-4562-bfa3-f958e0fe68ee" />

This comparison shows that the parallel execution took 1/3rd of the time of the serial execution.

## Video Processing
The approach taken for building each subtask has been uniform, a method is added to the VideoFile class for each subtask. Then, according to the choice of serial and diYerent types of parallel executions, additional script is written in the ‘serial_executions.py’, ‘threads_executions.py’, ‘process_executions.py’ and ‘concurrent_executions.py’ files.

One important consideration while choosing amongst the executions has been that each serial or parallel execution of a subtask is given the same array of VideoFile objects each of which are then updated by the class methods. This means that even for more CPU intensive tasks, using processes is not an option because it does not share memory and are not able to successfully update the VideoFile objects to ensure the current working of the next subtasks. Therefore, threads have been used to achieve parallelism throughout the project unless specified otherwise below.

1. Extract audio: A serial execution for this task is preferred over parallel executions. It is due to a pattern that was noticed: when multiple threads start extracting audios from different videos, if one has finished, the ones preceding it were noted to be terminated with impartial extraction. Therefore, it seemed more appropriate to extract audio from one video after another, since the time taken by the serial approaches was also less than the one taken by the parallel execution. This can be seen in the screenshots attached below.

### Parallel Execution
<img width="778" alt="Screenshot 2024-12-25 at 21 02 44" src="https://github.com/user-attachments/assets/c3d19f4f-6ae8-4705-9889-d41f6faba718" />

  
  ### Serial Execution
<img width="753" alt="Screenshot 2024-12-25 at 21 02 56" src="https://github.com/user-attachments/assets/2d86cc81-d15b-4af6-9016-e3062a4733d6" />

  However, if the project increases in scale, this decision might change.
  
2. TranscribeAudio – Analysing thread, process, concurrent and serial execution:
    The reason for choosing this subtask for the comparison was that it took the most time and seemed more CPU-intensive than other subtasks.
This can also be proved by the fact that execution using processes or asynchronous processes took less time than threads. However, as discussed above, since each execution alters the same shared variable, processes do not work correctly, and therefore threads is considered as the most viable option.

3. SentimentsAnalysis: Threads are used for executing this function due to the reason explained above, and there are no additional considerations or alterations to be discussed.
   
4. Text Translation: The solution for this subtask uses a Python library called the ‘deep_translator’ which provides an API to use the google translate feature. It is simple and straightforward and poses no incompatibility error with other libraries.
   
5. Emotion Extraction: The solution for emotion extraction used the spacy library which threw an error of incompatibility with some version of the NumPy library, this was solved by installing the spacy library without explicitly installing the NumPy library.

## Folder Structure

The project is organised as shown below.
• The download_log file is the logger file created in task 4. It was written in append
mode and therefore records various sets of running the project and downloading
videos.
• The video_data is the folder where all the files from the downloading and
processing components are stored. Each video has its own folder. The screenshot below only displays the respective folders for two videos, but the same structure is followed for all videos. Each subtask in the processing part adds a file to the video’s folder.
• The video_urls.txt is the file that stores all the URLs for the videos.
• The commands.md contains the commands that were followed to run the project
with a virtual environment.
<img width="722" alt="Screenshot 2024-12-25 at 21 03 47" src="https://github.com/user-attachments/assets/6b0f1fa1-892f-4e56-9d49-9cc0e7948708" />


## Environment Configurations
A virtual environment was created to isolate the libraries required for the project, this was done to avoid any clash with already existing libraries and to resolve the incompatibility issues between diYerent versions of diYerent libraries.
