import os
import shutil

# Define the folder names
folder_names = ["Pdfs", "Images", "Music", "Videos"]

current_directory = os.getcwd()

# Create the folders if they don't exist
for folder_name in folder_names:
    folder_path = os.path.join(current_directory, folder_name)


pdf_contents = []
images_contents = []
mp3_contents = []
videos_contents = []

pdf_folder_name = "Pdfs"
images_folder_name = "Images"
mp3_folder_name = "Music"
videos_folder_name = "Videos"

current_directory = os.getcwd()

pdf_folder_path = os.path.join(current_directory, pdf_folder_name)
images_folder_path = os.path.join(current_directory, images_folder_name)
mp3_folder_path = os.path.join(current_directory, mp3_folder_name)
videos_folder_path = os.path.join(current_directory, videos_folder_name)


if not (os.path.exists(pdf_folder_path) and os.path.exists(images_folder_path) and os.path.exists(mp3_folder_path)):
    os.mkdir(pdf_folder_path)
    os.mkdir(images_folder_path)
    os.mkdir(mp3_folder_path)
    os.mkdir(videos_folder_path)
    print(f"Folder '{pdf_folder_name}' created in {current_directory}")
    print(f"Folder '{images_folder_name}' created in {current_directory}")
    print(f"Folder '{mp3_folder_name}' created in {current_directory}")
    print(f"Folder '{videos_folder_name}' created in {current_directory}")
else:
    print(f"Folder '{pdf_folder_name}' already exists in {current_directory}")
    print(f"Folder '{images_folder_name}' already exists in {current_directory}")
    print(f"Folder '{mp3_folder_name}' already exists in {current_directory}")
    print(f"Folder '{videos_folder_name}' already exists in {current_directory}")

directory_contents = os.listdir(current_directory)

for item in directory_contents:
    if item.endswith(".pdf"):
        pdf_contents.append(item)
    elif item.endswith(".png") or item.endswith(".jpeg") or item.endswith(".jpg"):
        images_contents.append(item)
    elif item.endswith(".mp3"):
        mp3_contents.append(item)
    elif item.endswith(".mp4") or item.endswith(".webm"):
        videos_contents.append(item)



print(pdf_contents, images_contents, mp3_contents)

for pdf_file in pdf_contents:
    shutil.move(os.path.join(current_directory, pdf_file), os.path.join(current_directory, "Pdfs", pdf_file))

for image_file in images_contents:
    shutil.move(os.path.join(current_directory, image_file), os.path.join(current_directory, "Images", image_file))

for mp3_file in mp3_contents:
    shutil.move(os.path.join(current_directory, mp3_file), os.path.join(current_directory, "Music", mp3_file))

for video_file in videos_contents:
    shutil.move(os.path.join(current_directory, video_file), os.path.join(current_directory, "Videos", video_file))
