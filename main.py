import os
import subprocess
import random
import numpy as np
import moviepy
from moviepy.editor import VideoFileClip, concatenate_videoclips


# import dictionary as text file and convert to list
def words_setup():
    words_raw = open("./source/text/words.txt", "r")
    brainrot_raw = open("./source/text/brainrot.txt", "r")
    words_data = words_raw.read()
    brainrot_data = brainrot_raw.read()
    words_list = words_data.split("\n")
    brainrot_list = brainrot_data.split("\n")
    words_datasize = np.size(words_list)
    print(f"words data size is {words_datasize}")
    brainrot_datasize = np.size(brainrot_list)
    print(f"brainrot data size is {brainrot_datasize}")
    return (words_datasize, words_list, brainrot_datasize, brainrot_list)


# checks if selected video ID is a repeat of a previous search
def visited_checker(id):
    visited_raw = open("./source/visited.txt", "r")
    visited_data = visited_raw.read()
    visited_list = visited_data.split(",")
    if id in visited_list:
        duplicate = True
    else:
        duplicate = False
        os.system(f"echo '{id},' >> ./source/visited.txt")
    return duplicate


# select random word from dictionary
def words_select(words_datasize, words_list, brainrot_datasize, brainrot_list):
    print("chance of brainrot: 25%")

    print("chance of india: 25%")

    print("chance of normal video: 50%")

    print()
    print("-- NOW GENERATING RANDOM CHOICE --")
    print()
    os.system("sleep 3")
    choice = random.randrange(4)
    print("-- CHOICE HAS BEEN MADE --")
    os.system("sleep 1")
    if choice == 0 or choice == 1:
        print()
        print("-------------------------------")
        print("!!!BRAINROT HAS BEEN CHOSEN!!!")
        print("-------------------------------")
        print("choosing random brainrot search term from brainrot list:")
        print()
        word_selection_index = random.randrange(brainrot_datasize)
        print(f"brainrot selection index number is {word_selection_index}")
        word_selected = brainrot_list[word_selection_index]
        print(f"selected brainrot search term is {word_selected}")

    elif choice == 2:
        print()
        print("-------------------------------")
        print("!!!INDIA HAS BEEN CHOSEN!!!")
        print("-------------------------------")
        print()
        word_selected = "#punjabi #india #funny #viral #tiktok"
        print("using searchterm: '#punjabi #india #funny #viral #tiktok'")
    else:
        print()
        print("-------------------------------")
        print("normal video has been chosen")
        print("-------------------------------")

        word_selection_index = random.randrange(words_datasize)
        print(f"word selection index number is {word_selection_index}")
        word_selected = words_list[word_selection_index]
        print(f"selected word is {word_selected}")
    return word_selected


# search youtube for the first two hundred videos with our random keyword we selected, then grabs one of the last ones and returns the metadata
# yt-dlp ytsearch200:"<insert search term here>" --get-id --get-duration --get-title -I 184
def youtube_search(word_selected):
    os.system("sleep 1")
    process = subprocess.Popen(
        [
            "yt-dlp",
            f"ytsearch200:{word_selected}",
            "--get-id",
            "--get-duration",
            "--get-title",
            "-I",
            "190",
            "--match-filter",
            "duration >= 10",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    process.wait()
    stdout, stderr = process.communicate()

    print("Return code:", process.returncode)

    print(f"stderr is: {stderr}")
    print(f"stdout is: {stdout}")
    output_list = stdout.split("\n")
    title = output_list[0]
    id = output_list[1]
    duration = output_list[2]
    print(f"the id is {id}")
    print(f"the duration is {duration}")
    print(f"the title is {title}")
    # ``````````````````````````````````````````````````````````````````
    duplicate = visited_checker(id)
    print(f"duplicate??? -->  {duplicate}")
    if duplicate:
        print(
            "this ID has already been selected in the past, to avoid duplicate clips, we will ignore this id"
        )
        id = 0

    return id, duration


def inc_counter(current_inc):
    print(f"current inc is {current_inc}")
    inc = current_inc
    inc += 1
    return inc


# download random portion of selected video
def youtube_download(id, duration, video_inc_counter):
    video_inc = video_inc_counter

    if id == 0:  # catch duplicate id and prevent download
        pass

    random_time_int = random.randint(1, 3)
    print(f"original video duration is {duration}")
    if ":" in duration:
        print("duration is longer than a minute")
        duration = 60

    else:
        print("duration is shorter than a minute")

    duration_int = int(duration)
    base_time = duration_int // 2
    start_time = base_time - random_time_int
    print(f"video duration should be {random_time_int}")
    print(f"downloading video from 0:{start_time}-0:{base_time}")
    process = subprocess.Popen(
        [
            "yt-dlp",
            f"https://youtube.com/watch?v={id}",
            "--download-sections",
            f"'*00:00:{start_time}-00:00:{base_time}'",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    print(process)
    stdout, stderr = process.communicate()

    # print(f"process = {process}")

    print("Return code:", process.returncode)
    print(stderr)
    output = stdout

    command = f"yt-dlp 'https://youtube.com/watch?v={id}' --download-sections '*00:00:{start_time}-00:00:{base_time}' --force-keyframes-at-cuts -S proto:https -o ./video_raw/{video_inc} --merge-output-format mp4 --remux-video mp4"
    os.system(command)


def movie_assembly():
    # Folder containing video files
    video_folder = "./video_raw"

    # List all video files in the folder
    video_files = [
        f
        for f in os.listdir(video_folder)
        if f.endswith((".mp4", ".mov", ".avi", ".webm", ".mkv", ""))
    ]

    # Dictionary to hold video clips
    video_clips = {}

    # Load each video file into VideoFileClip
    for file_name in video_files:
        file_path = os.path.join(video_folder, file_name)
        if file_name == "2*":
            # Apply subclip to this specific file
            video_clips[file_name] = VideoFileClip(file_path).subclip(50, 60)
        else:
            # Load the full clip
            video_clips[file_name] = VideoFileClip(file_path)

    # Retrieve all clips and concatenate
    clips_to_concatenate = list(video_clips.values())
    final_clip = concatenate_videoclips(
        clips_to_concatenate,
        method="compose",
    )

    # Optionally, write the result to a file
    output_file = "my_concatenation.mp4"
    final_clip.write_videofile(output_file, codec="libx264")

    # Close all clips to free resources
    for clip in video_clips.values():
        clip.close()


def main():
    os.system("rm ./video_raw/*")
    inc = 0
    words_datasize, data_into_list, brainrot_datasize, brainrot_list = words_setup()
    video_qty = int(input("hi. how many videos would you like to get?: "))
    for x in range(0, video_qty):
        inc = inc_counter(inc)
        os.system("sleep 1")
        word_selected = words_select(
            words_datasize, data_into_list, brainrot_datasize, brainrot_list
        )
        try:
            id, duration = youtube_search(word_selected)

            youtube_download(id, duration, inc)
        except IndexError:
            print("oopsie!!! index error... idk why though.. oh well.. moving on")
    movie_assembly()


if __name__ == "__main__":
    main()
