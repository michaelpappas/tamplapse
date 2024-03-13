import cv2
import os
import re
import argparse

def natural_sort_key(s):
    """Natural sorting key function."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def create_timelapse(input_folder, output_video, fps=24, resolution=(1920, 1080)):
    # Get the list of JPEG files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.jpg')]

    # Sort the files by integer values extracted from their names
    image_files.sort(key=natural_sort_key)

    # Check if there are any image files in the folder
    if not image_files:
        print("No JPEG images found in the input folder.")
        return

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_out = cv2.VideoWriter(output_video, fourcc, fps, resolution)

    # Iterate through each image and add it to the video
    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        frame = cv2.imread(image_path)
        if frame is not None:
            frame = cv2.resize(frame, resolution)
            video_out.write(frame)

    # Release everything when finished
    video_out.release()
    cv2.destroyAllWindows()

    print(f"Timelapse video created: {output_video}")

if __name__ == "__main__":

    input_folder = "images"
    output_video = "3_12.mp4"

    create_timelapse(input_folder, output_video)